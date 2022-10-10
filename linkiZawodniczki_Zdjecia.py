import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

########################################################################################################################
### POBRANIE LINKÓW DO WSZYSTKICH ZAWODNICZEK SEZONÓW 2020/2021 I 2021/2022 I ZDJĘĆ ####################################
########################################################################################################################
def getLastname_PhotoLinks():
    searchURL2021_2022 = "https://www.tauronliga.pl/statsPlayers/tournament_1/2021.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D"
    searchURL2020_2021 = "https://www.tauronliga.pl/statsPlayers/tournament_1/2020.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D"
    searchURL2019_2020 = "https://www.tauronliga.pl/statsPlayers/tournament_1/2019.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D"
    searchURL2018_2019 = "https://www.tauronliga.pl/statsPlayers/tournament_1/2018.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D"
    searchURL = [searchURL2018_2019, searchURL2019_2020, searchURL2020_2021, searchURL2021_2022]

    linki = []
    photoLinks = []
    nazwiskoLista = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/statsPlayers/id/" in str(link.get('href')):
                try:
                    if id % 2 == 0:
                        linki.append(link['href'])
                    else:
                        photo = link.find('img')['src']
                        photoLinks.append(photo)
                        nazwisko = link.find('img')['alt']
                        nazwiskoLista.append(nazwisko)
                except TypeError:
                    photoLinks.append("ebebeb")

    df = pd.DataFrame(data = [nazwiskoLista, photoLinks])
    df.to_csv('CSV/nazwisko_zdjecie.csv', mode='a', index=False, encoding='windows-1250', sep=";", header = False)
    # print(len(links))
    # print(len(photoLinks))

    # ZAPISANIE LINKÓW DO PLIKÓW TEKSTOWYCH W CELU WERYFIKACJI
    with open('txtWCeluWeryfikacji/links.txt', 'w') as f:
        for link in linki:
            f.write(str(link))
            f.write("\n")

    with open('txtWCeluWeryfikacji/photoLinks.txt', 'w') as f:
        for link in photoLinks:
            f.write(str(link))
            f.write("\n")

    print("Pobrano linki do indywidualnych profilów zawodniczek.\nStworzono plik z nazwiskami oraz linkami do zdjęć.")
