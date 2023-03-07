import time
import pandas as pd

from getLinksToPlayers import getPlayers
from getLinksToMatches import getMatchesLinks
from usefulFunctions import makeCSVFolder, playerLinksList, matchesLinksList, standingsLinksList,\
    teamsInSeasonLinksList, prepareCSV_matchesInfo, prepareCSV_newSystem, prepareCSV_oldSystem,\
    prepareCSV_standings, prepareCSV_combinedStats, prepareCSV_clubInfo
from scrapStatistics import scrapStatiscics
from getPlayerInfo import getInformationsAboutPlayers
from getStandings import getStandings
from mariadbController import connectToDatabase, readCSVFiles, createTablePlayerInfo, createTableMatchesInfo, \
    createTableStatsOld, createTableStatsNew, createTableStandings, createTableStatsCombined, createTableClubInfo
from combineStatistics import combineStats
from getInfoAboutTeam import getInfo


# początek pomiaru czasu
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2013
end = 2021

# stworzenie folderu na pliki csv
#makeCSVFolder()

# deklaracja nazw plików przekazywanych do stworzenia
getClubInfoFilename = "clubInfoTest"
getPlayerInfoFilename = "playerInfo"
oldSystemFileName = "stats_OLD_SEASONS"
newSystemFileName = "stats_NEW_SEASONS"
standingsFileName = "standings"
matchesInfoFileName = "matchesInfo"
combinedStats = "combinedStats"

# pobranie stron z linkami do składów zespołów
teamsSquadsLinksURLs = teamsInSeasonLinksList(start, end)

# pobranie stron z linkami do profilów zawodniczek
playerListLinksURLs = playerLinksList(start, end)

# pobranie stron do wszystkich meczów w sezonie
matchesListLinksURLs = matchesLinksList(start, end)


# przygotowanie plików csv
# prepareCSV_matchesInfo(matchesInfoFileName)
# prepareCSV_oldSystem(oldSystemFileName)
# prepareCSV_newSystem(newSystemFileName)
# prepareCSV_standings(standingsFileName)
# prepareCSV_combinedStats(combinedStats)
prepareCSV_clubInfo(getClubInfoFilename)


# pobranie informacji o klubie
getInfo(teamsSquadsLinksURLs, getClubInfoFilename)

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

# bezpośrednie pobieranie statystyk meczowych
stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName, matchesInfoFileName)

# ujednolicanie statystyk
combineStats(oldSystemFileName, newSystemFileName, combinedStats)

# pobranie danych odnośnie klasyfikacji zespołów na koniec sezonów
standingsLinksURLs = standingsLinksList(start, end)
getStandings(standingsLinksURLs, standingsFileName)


# zapisanie plików do bazy danych
conn, cur = connectToDatabase()
playerInfo, statsOld, statsNew, standings, matchesInfo, clubInfo, combinedStatistics = \
    readCSVFiles(getClubInfoFilename, getPlayerInfoFilename, oldSystemFileName, newSystemFileName, standingsFileName,
                 matchesInfoFileName, combinedStats)
createTablePlayerInfo(conn, cur, playerInfo)
createTableStatsOld(conn, cur, statsOld)
createTableStatsNew(conn, cur, statsNew)
createTableStandings(conn, cur, standings)
createTableMatchesInfo(conn, cur, matchesInfo)
createTableStatsCombined(conn, cur, combinedStatistics)
createTableClubInfo(conn, cur, clubInfo)


# koniec pomiaru czasu
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print("\nCzas wykonywania: ", timeTotal, 'sekund')
