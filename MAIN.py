# from bs4 import BeautifulSoup
# from urllib.request import urlopen
import time

from getStatistics import prepareCSV_newSystem, prepareCSV_oldSystem, getStats
from getLinksToPlayersPhotos import getLastnamePhotoLinks
from getLinksToMatches import getMatchesLinks
from usefulFunctions import playerListLinks, matchesListLinks
from scrapStatistics import scrapStatiscics

# początek pomiaru czasu w celach statystycznych
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# stworzenie zakresu lat i odpowiednich linków
playerListLinksURLs = playerListLinks(start, end)

# pobranie linków do wszystkich meczów w sezonie
matchesListLinksURLs = matchesListLinks(start, end)

# pobranie nazwisk zawodniczek i linków do zdjęć
getLastnamePhotoLinks(playerListLinksURLs)

########################################################################################################################
### ODZYSKANIE LINKÓW Z PLIKÓW TEKSTOWYCH ##############################################################################
########################################################################################################################
#links = []
# photoLinks = []
# with open('matchLinks2020_2021.txt', 'r') as f:
#     for link in f:
#         links.append(link)
links = getMatchesLinks(matchesListLinksURLs)


########################################################################################################################
### PRZYGOTOWANIE NAGŁÓWKÓW DO PLIKU ZE STATYSTYKAMI ###################################################################
########################################################################################################################
oldSystemFileName = "statystyki_SEZONY_STARE.csv"
newSystemFileName = "statystyki_SEZONY_NOWE.csv"

prepareCSV_oldSystem(oldSystemFileName)
prepareCSV_newSystem(newSystemFileName)

########################################################################################################################
### ITERACJA PO LINKACH Z PLIKU ########################################################################################
########################################################################################################################
stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName)


# for index, i in enumerate(links):
#     i = i.rstrip('\n')
#     searchURL = "https://www.tauronliga.pl/" + i
#     page = urlopen(searchURL)
#
#     soup = BeautifulSoup(page, "lxml")
#
#     # pobranie statystyk dla nowego systemu
#     if 'tour/2020' in i or 'tour/2021' in i:
#         statystykiZespol1 = getStats(0, soup, "new")
#         statystykiZespol2 = getStats(1, soup, "new")
#
#         # zapisanie statystyk do pliku
#         try:
#             statystykiZespol1.to_csv('CSV/' + newSystemFileName, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
#             statystykiZespol2.to_csv('CSV/' + newSystemFileName, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
#
#         except AttributeError:
#             pass
#
#     # pobranie statystyk dla starego systemu
#     else:
#         statystykiZespol1 = getStats(0, soup, "old")
#         statystykiZespol2 = getStats(1, soup, "old")
#
#         # zapisanie statystyk do pliku
#         try:
#             statystykiZespol1.to_csv('CSV/' + oldSystemFileName, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
#             statystykiZespol2.to_csv('CSV/' + oldSystemFileName, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
#
#         except AttributeError:
#             pass
#
#     if index % 20 == 1:
#         print("Pobranie statystyk meczowych...", index, "/", len(links))

# koniec pomiaru czasu w celach statystycznych
timeEnd = time.time()
czas = timeEnd - timeStart
print("Czas wykonywania: ", czas, 'sekund')
