from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter

########################################################################################################################
### POBRANIE LINKÓW DO WSZYSTKICH MECZÓW SEZONU 2020/2021 I 2021/2022 ##################################################
########################################################################################################################
# zwracana jest lista z linkami, które prowadzą do poszczególnych meczów
def getMatchesLinks(searchURL):
    links = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/games/id/" in str(link.get('href')) and "#stats" not in str(link.get('href')):
                if "11020" not in str(link.get('href')) and "11021" not in str(link.get('href')):
                    links.append("ga" + str(link['href']).lstrip("https://www.tauronliga.pl"))
                if "1102023" in str(link.get('href')):
                    links.append("ga" + str(link['href']).lstrip("https://www.tauronliga.pl"))

    # wybranie unikalnych wartości
    links = Counter(links)
    #print(len(links))

    # ZAPISANIE LINKÓW DO PLIKU TEKSTOWEGO W CELU WERYFIKACJI
    # with open('txtWCeluWeryfikacji/matchLinks_2_SEZONY.txt', 'w') as f:
    #     for link in links:
    #         f.write(str(link))
    #         f.write("\n")

    print("Pobrano linki do wszystkich meczów zadanego przedziału.\nPobrano łącznie ", len(links), " linków do meczy.")
    return links
