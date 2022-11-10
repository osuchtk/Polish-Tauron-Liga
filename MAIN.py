import time

from getLinksToPlayers import getPlayers
from getLinksToMatches import getMatchesLinks
from usefulFunctions import makeCSVFolder, playerListLinks, matchesListLinks, standingsLinks,\
    prepareCSV_matchesInfo, prepareCSV_players, prepareCSV_newSystem, prepareCSV_oldSystem, prepareCSV_standings
from scrapStatistics import scrapStatiscics
from getPlayerInfo import getInformations
from getStandings import getStandings
from mariadbController import connectToDatabase, readCSVFiles, createTablePlayrList, createTableMatchesInfo, \
    createTableStatsOld, createTableStatsNew, createTableStandings

# początek pomiaru czasu
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# stworzenie folderu na pliki csv
#makeCSVFolder()

# deklaracja nazw plików przekazywanych do stworzenia
getPlayersFilename = "playerList"
getPlayerInfoFilename = "playerInfo"
oldSystemFileName = "stats_OLD_SEASONS"
newSystemFileName = "stats_NEW_SEASONS"
standingsFileName = "standings"
matchesInfoFileName = "matchesInfo"
#
# pobranie stron z linkami do profilów zawodniczek
playerListLinksURLs = playerListLinks(start, end)
#
# pobranie stron do wszystkich meczów w sezonie
# matchesListLinksURLs = matchesListLinks(start, end)
#
#
# pobranie informacji o zawodniczkach
prepareCSV_players(getPlayersFilename)
players = getPlayers(playerListLinksURLs, getPlayersFilename)
#
#
# pobranie linków do wszystkich meczy w zadanym przedziale czasowym
# links = getMatchesLinks(matchesListLinksURLs)
#
#
# przygotowanie nagłówków do pliku ze statystykami
# prepareCSV_matchesInfo(matchesInfoFileName)
# prepareCSV_oldSystem(oldSystemFileName)
# prepareCSV_newSystem(newSystemFileName)
#
# bezpośrednie pobieranie statystyk meczowych
# stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName, matchesInfoFileName)
#
# pobranie danych odnośnie klasyfikacji zespołów na koniec sezonów
# prepareCSV_standings(standingsFileName)
# standingsLinksURLs = standingsLinks(start, end)
# getStandings(standingsLinksURLs, standingsFileName)


# zapisanie plików do bazy danych
conn, cur = connectToDatabase()
playerList, statsOld, statsNew, standings, matchesInfo = readCSVFiles()
createTablePlayrList(conn, cur, playerList)
# createTableStatsOld(conn, cur, statsOld)
# createTableStatsNew(conn, cur, statsNew)
# createTableStandings(conn, cur, standings)
# createTableMatchesInfo(conn, cur, matchesInfo)


# koniec pomiaru czasu
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print("\nCzas wykonywania: ", timeTotal, 'sekund')
