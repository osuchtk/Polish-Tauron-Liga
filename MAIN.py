import time
import pandas as pd

from getLinksToPlayers import getPlayers
from getLinksToMatches import getMatchesLinks
from usefulFunctions import makeCSVFolder, playerLinksList, matchesLinksList, standingsLinksList,\
    teamsSquadInSeasonLinksList, prepareCSV_matchesInfo, prepareCSV_newSystem, prepareCSV_oldSystem,\
    prepareCSV_standings, prepareCSV_ClubSquadList
from scrapStatistics import scrapStatiscics
from getPlayerInfo import getInformationsAboutPlayers
from getStandings import getStandings
from mariadbController import connectToDatabase, readCSVFiles, createTablePlayerInfo, createTableMatchesInfo, \
    createTableStatsOld, createTableStatsNew, createTableStandings, createTableSquadsInfo
from getSquadsInSeason import getSquads


# początek pomiaru czasu
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# stworzenie folderu na pliki csv
makeCSVFolder()

# deklaracja nazw plików przekazywanych do stworzenia
getSquadListFilename = "teamsSquads"
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
players = getPlayers(playerListLinksURLs)
informations = getInformationsAboutPlayers(players)

playersInformations = pd.merge(players, informations, "left", "Nazwisko")
playersInformations.drop_duplicates(inplace = True)
playersInformations.columns = ["Nazwisko", "Zdjęcie", "Profil", "Data urodzenia", "Pozycja", "Wzrost", "Waga", "Zasięg"]
playersInformations.to_csv('CSV/' + getPlayerInfoFilename + '.csv', mode='a', index=False, encoding='windows-1250',
                           sep=";", header=False)


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
conn, cur = connectToDatabase()
playerInfo, statsOld, statsNew, standings, matchesInfo, teamSquads = readCSVFiles()
createTablePlayerInfo(conn, cur, playerInfo)
createTableStatsOld(conn, cur, statsOld)
createTableStatsNew(conn, cur, statsNew)
createTableStandings(conn, cur, standings)
createTableMatchesInfo(conn, cur, matchesInfo)
createTableSquadsInfo(conn, cur, teamSquads)


# koniec pomiaru czasu
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print("\nCzas wykonywania: ", timeTotal, 'sekund')
