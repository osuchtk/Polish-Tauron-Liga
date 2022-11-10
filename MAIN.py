import time
import pandas as pd

from getLinksToPlayers import getPlayers
from getLinksToMatches import getMatchesLinks
from usefulFunctions import makeCSVFolder, playerLinksList, matchesLinksList, standingsLinksList,\
    teamsSquadInSeasonLinksList, prepareCSV_matchesInfo, prepareCSV_playersList, prepareCSV_newSystem,\
    prepareCSV_oldSystem, prepareCSV_standings, prepareCSV_ClubSquadList
from scrapStatistics import scrapStatiscics
from getPlayerInfo import getInformationsAboutPlayers
from getStandings import getStandings
from mariadbController import connectToDatabase, readCSVFiles, createTablePlayerList, createTableMatchesInfo, \
    createTableStatsOld, createTableStatsNew, createTableStandings
from getPlayerInfo import getInformationsAboutPlayers
from getSquadsInSeason import getSquads

# początek pomiaru czasu
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# stworzenie folderu na pliki csv
#makeCSVFolder()

# deklaracja nazw plików przekazywanych do stworzenia
getSquadListFilename = "teamsSquads"
#getPlayersFilename = "playerList"
getPlayerInfoFilename = "playerInfo"
oldSystemFileName = "stats_OLD_SEASONS"
newSystemFileName = "stats_NEW_SEASONS"
standingsFileName = "standings"
matchesInfoFileName = "matchesInfo"

# pobranie stron z linkami do składów zespołów
teamsSquadsLinksURLs = teamsSquadInSeasonLinksList(start, end)

# pobranie stron z linkami do profilów zawodniczek
playerListLinksURLs = playerLinksList(start, end)

# pobranie stron do wszystkich meczów w sezonie
matchesListLinksURLs = matchesLinksList(start, end)


# pobieranie informacji o składzie zespołu w danym sezonie
prepareCSV_ClubSquadList(getSquadListFilename)
getSquads(teamsSquadsLinksURLs, getSquadListFilename)

# pobranie informacji o zawodniczkach
#prepareCSV_playersList(getPlayersFilename)
players = getPlayers(playerListLinksURLs)
informations = getInformationsAboutPlayers(players)

players = pd.DataFrame.join(informations, "Nazwisko", "left")
players.to_csv('CSV/' + getPlayerInfoFilename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)


# pobranie linków do wszystkich meczy w zadanym przedziale czasowym
links = getMatchesLinks(matchesListLinksURLs)


# przygotowanie nagłówków do pliku ze statystykami
prepareCSV_matchesInfo(matchesInfoFileName)
prepareCSV_oldSystem(oldSystemFileName)
prepareCSV_newSystem(newSystemFileName)

# bezpośrednie pobieranie statystyk meczowych
stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName, matchesInfoFileName)

# pobranie danych odnośnie klasyfikacji zespołów na koniec sezonów
prepareCSV_standings(standingsFileName)
standingsLinksURLs = standingsLinksList(start, end)
getStandings(standingsLinksURLs, standingsFileName)


# zapisanie plików do bazy danych
#conn, cur = connectToDatabase()
#playerList, statsOld, statsNew, standings, matchesInfo = readCSVFiles()
#createTablePlayerList(conn, cur, playerList)
# createTableStatsOld(conn, cur, statsOld)
# createTableStatsNew(conn, cur, statsNew)
# createTableStandings(conn, cur, standings)
# createTableMatchesInfo(conn, cur, matchesInfo)


# koniec pomiaru czasu
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print("\nCzas wykonywania: ", timeTotal, 'sekund')
