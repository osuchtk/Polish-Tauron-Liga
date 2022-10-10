from urllib.request import urlopen
from bs4 import BeautifulSoup

from getStatistics import getStats


def scrapStatiscics(links, newSystemFileName, oldSystemFileName):
    for index, i in enumerate(links):
        i = i.rstrip('\n')
        searchURL = "https://www.tauronliga.pl/" + i
        page = urlopen(searchURL)

        soup = BeautifulSoup(page, "lxml")

        # pobranie statystyk dla nowego systemu
        if 'tour/2020' in i or 'tour/2021' in i:
            statystykiZespol1 = getStats(0, soup, "new")
            statystykiZespol2 = getStats(1, soup, "new")

            # zapisanie statystyk do pliku
            try:
                statystykiZespol1.to_csv('CSV/' + newSystemFileName, mode='a', index=False, encoding='windows-1250',
                                         sep=";", header=False)
                statystykiZespol2.to_csv('CSV/' + newSystemFileName, mode='a', index=False, encoding='windows-1250',
                                         sep=";", header=False)

            except AttributeError:
                pass

        # pobranie statystyk dla starego systemu
        else:
            statystykiZespol1 = getStats(0, soup, "old")
            statystykiZespol2 = getStats(1, soup, "old")

            # zapisanie statystyk do pliku
            try:
                statystykiZespol1.to_csv('CSV/' + oldSystemFileName, mode='a', index=False, encoding='windows-1250',
                                         sep=";", header=False)
                statystykiZespol2.to_csv('CSV/' + oldSystemFileName, mode='a', index=False, encoding='windows-1250',
                                         sep=";", header=False)

            except AttributeError:
                pass

        if index % 20 == 1:
            print("Pobranie statystyk meczowych...", index, "/", len(links))