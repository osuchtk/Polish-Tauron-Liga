########################################################################################################################
### POBRANIE LINKÓW DO MECZÓW Z ZADANYCH SEZONÓW #######################################################################
########################################################################################################################
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter

# zwracana jest lista z linkami, które prowadzą do poszczególnych meczów
def getMatchesLinks(searchURL):
    links = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/games/id/" in str(link.get('href')) and "#stats" not in str(link.get('href')):
                if "tauronliga" not in link['href']:
                    links.append(link['href'])

    # wybranie unikalnych wartości
    links = list(Counter(links))

    print("Pobrano linki do wszystkich meczów zadanego przedziału.\nPobrano łącznie ", len(links), " linków do meczy.")
    return links
