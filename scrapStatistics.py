from urllib.request import urlopen
from bs4 import BeautifulSoup

from getStatistics import getStats


def scrapStatiscics(searchURLsList, newSystemFileName, oldSystemFileName, matchesInfoFileName):
    for index, i in enumerate(searchURLsList):
        searchURL = "https://www.tauronliga.pl" + i
        page = urlopen(searchURL)
        soup = BeautifulSoup(page, "lxml")

        value = str(i).split("/")[5].split(".")[0]
        # pobranie statystyk dla nowego systemu
        if int(value) > 2019:
            statsTeam1 = getStats(0, soup, "new", searchURL, matchesInfoFileName)
            statsTeam2 = getStats(1, soup, "new", searchURL, matchesInfoFileName)

            # zapisanie statystyk do pliku
            try:
                statsTeam1.to_csv('CSV/' + newSystemFileName + '.csv', mode='a', index=False,
                                  encoding='windows-1250', sep=";", header=False)
                statsTeam2.to_csv('CSV/' + newSystemFileName + '.csv', mode='a', index=False,
                                  encoding='windows-1250', sep=";", header=False)

            except AttributeError:
                pass

        # pobranie statystyk dla starego systemu
        else:
            statsTeam1 = getStats(0, soup, "old", searchURL, matchesInfoFileName)
            statsTeam2 = getStats(1, soup, "old", searchURL, matchesInfoFileName)

            # zapisanie statystyk do pliku
            try:
                statsTeam1.to_csv('CSV/' + oldSystemFileName + '.csv', mode='a', index=False,
                                  encoding='windows-1250', sep=";", header=False)
                statsTeam2.to_csv('CSV/' + oldSystemFileName + '.csv', mode='a', index=False,
                                  encoding='windows-1250', sep=";", header=False)

            except AttributeError:
                pass

        # wypisywanie postępów pobierania statystyk
        if index % 20 == 1:
            print("Pobieranie statystyk meczowych...", index, "/", len(searchURLsList))
