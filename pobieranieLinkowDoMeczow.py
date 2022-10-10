from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter

########################################################################################################################
### POBRANIE LINKÓW DO WSZYSTKICH MECZÓW SEZONU 2020/2021 I 2021/2022 ##################################################
########################################################################################################################
# zwracana jest lista z linkami, które prowadzą do poszczególnych meczów
def getMatchesLinks():
    searchURL2021_2022 = "https://www.tauronliga.pl/games/tour/2021.html"
    searchURL2020_2021 = "https://www.tauronliga.pl/games/tour/2020.html"
    searchURL2019_2020 = "https://www.tauronliga.pl/games/tour/2019.html"
    searchURL2018_2019 = "https://www.tauronliga.pl/games/tour/2018.html"
    searchURL = [searchURL2018_2019, searchURL2019_2020, searchURL2020_2021, searchURL2021_2022]

    linki = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/games/id/" in str(link.get('href')) and "#stats" not in str(link.get('href')):
                if "11020" not in str(link.get('href')) and "11021" not in str(link.get('href')):
                    linki.append("ga" + str(link['href']).lstrip("https://www.tauronliga.pl"))
                if "1102023" in str(link.get('href')):
                    linki.append("ga" + str(link['href']).lstrip("https://www.tauronliga.pl"))

    # wybranie unikalnych wartości
    linki = Counter(linki)
    #print(len(linki))

    # ZAPISANIE LINKÓW DO PLIKU TEKSTOWEGO W CELU WERYFIKACJI
    with open('txtWCeluWeryfikacji/matchLinks_2_SEZONY.txt', 'w') as f:
        for link in linki:
            f.write(str(link))
            f.write("\n")

    print("Pobrano linki do wszystkich meczów sezonów 2020/2021 i 2021/2022.\nPobrano łącznie ", len(linki), " linków.")
    return linki
