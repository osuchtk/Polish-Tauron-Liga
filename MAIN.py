from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

from pobranieStatystyk import prepareCSV_newSystem, prepareCSV_oldSystem, getStats
from linkiZawodniczki_Zdjecia import getLastname_PhotoLinks
from pobieranieLinkowDoMeczow import getMatchesLinks

# początek pomiaru czasu w celach statystycznych
czasPoczatek = time.time()

# pobranie nazwisk zawodniczek i linków do zdjęć
getLastname_PhotoLinks()

########################################################################################################################
### ODZYSKANIE LINKÓW Z PLIKÓW TEKSTOWYCH ##############################################################################
########################################################################################################################
links = []
# photoLinks = []
# with open('matchLinks2020_2021.txt', 'r') as f:
#     for link in f:
#         links.append(link)
links = getMatchesLinks()


########################################################################################################################
### PRZYGOTOWANIE NAGŁÓWKÓW DO PLIKU ZE STATYSTYKAMI ###################################################################
########################################################################################################################
starySystemNazwaPliku = "statystyki_SEZONY_STARE.csv"
nowySystemNazwaPliku = "statystyki_SEZONY_NOWE.csv"

prepareCSV_oldSystem(starySystemNazwaPliku)
prepareCSV_newSystem(nowySystemNazwaPliku)

########################################################################################################################
### ITERACJA PO LINKACH Z PLIKU ########################################################################################
########################################################################################################################
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
            statystykiZespol1.to_csv('CSV/' + nowySystemNazwaPliku, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
            statystykiZespol2.to_csv('CSV/' + nowySystemNazwaPliku, mode='a', index=False, encoding='windows-1250', sep=";", header = False)

        except AttributeError:
            pass

    # pobranie statystyk dla starego systemu
    else:
        statystykiZespol1 = getStats(0, soup, "old")
        statystykiZespol2 = getStats(1, soup, "old")

        # zapisanie statystyk do pliku
        try:
            statystykiZespol1.to_csv('CSV/' + starySystemNazwaPliku, mode='a', index=False, encoding='windows-1250', sep=";", header = False)
            statystykiZespol2.to_csv('CSV/' + starySystemNazwaPliku, mode='a', index=False, encoding='windows-1250', sep=";", header = False)

        except AttributeError:
            pass

    if index % 20 == 1:
        print("Pobranie statystyk meczowych...", index, "/", len(links))

# koniec pomiaru czasu w celach statystycznych
czasKoniec = time.time()
czas = czasKoniec - czasPoczatek
print("Czas wykonywania: ", czas, 'sekund')
