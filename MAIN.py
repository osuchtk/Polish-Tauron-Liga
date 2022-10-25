import time

from getLinksToPlayers import getPlayers
from getLinksToMatches import getMatchesLinks
from usefulFunctions import makeCSVFolder, playerListLinks, matchesListLinks, prepareCSV_playerInfo,\
    prepareCSV_players, prepareCSV_newSystem, prepareCSV_oldSystem
from scrapStatistics import scrapStatiscics
from getPlayerInfo import getInformations
from mariadbController import connectToDatabase, readCSVFiles, createTablePlayrList, createTablePlayrInfo,\
    createTableStatsOld, createTableStatsNew

# początek pomiaru czasu w celach statystycznych
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# stworzenie folderu na pliki csv
makeCSVFolder()

# deklaracja nazw plików przekazywanych do stworzenia
getPlayersFilename = "playerList"
getPlayerInfoFilename = "playerInfo"
oldSystemFileName = "stats_OLD_SEASONS"
newSystemFileName = "stats_NEW_SEASONS"

# pobranie stron z linkami do profilów zawodniczek
playerListLinksURLs = playerListLinks(start, end)

# pobranie stron do wszystkich meczów w sezonie
matchesListLinksURLs = matchesListLinks(start, end)


# pobranie nazwisk zawodniczek, linków do zdjęć i profilów
prepareCSV_players(getPlayersFilename)
players = getPlayers(playerListLinksURLs, getPlayersFilename)

# pobranie informacji o zawodniczkach
prepareCSV_playerInfo(getPlayerInfoFilename)
getInformations(players, getPlayerInfoFilename)


# pobranie linków do wszystkich meczy w zadanym przedziale czasowym
links = getMatchesLinks(matchesListLinksURLs)


# przygotowanie nagłówków do pliku ze statystykami
prepareCSV_oldSystem(oldSystemFileName)
prepareCSV_newSystem(newSystemFileName)

# bezpośrednie pobieranie statystyk meczowych
stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName)


# zapisanie plików do bazy danych
conn, cur = connectToDatabase()
playerList, playerInfo, statsOld, statsNew = readCSVFiles()
createTablePlayrList(conn, cur, playerList)
createTablePlayrInfo(conn, cur, playerInfo)
createTableStatsOld(conn, cur, statsOld)
createTableStatsNew(conn, cur, statsNew)


# koniec pomiaru czasu w celach statystycznych
timeEnd = time.time()
timeTotal = timeEnd - timeStart
print("\nCzas wykonywania: ", timeTotal, 'sekund')
