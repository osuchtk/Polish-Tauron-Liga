import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

########################################################################################################################
### POBRANIE LINKÓW DO WSZYSTKICH ZAWODNICZEK SEZONÓW 2020/2021 I 2021/2022 I ZDJĘĆ ####################################
########################################################################################################################
def getLastnamePhotoLinks(searchURL, filename):
    links = []
    photoLinks = []
    playernameList = []
    season = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/statsPlayers/id/" in str(link.get('href')):
                if id % 2 == 0:
                    links.append(link['href'])
                else:
                    try:
                        photo = link.find('img')['src']
                        photoLinks.append(photo)
                        surname = link.find('img')['alt']
                        playernameList.append(surname)
                    except TypeError:
                        photoLinks.append("//img.women.siatkarskaliga.pl/player_400.png")

                    seasonValue = str(i[52:56]) + "/" + str(int(i[52:56]) + 1)
                    season.append(seasonValue)

    df = pd.DataFrame(data = [playernameList, photoLinks, season])
    df = df.T
    df.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header = False)


    # ZAPISANIE LINKÓW DO PLIKÓW TEKSTOWYCH W CELU WERYFIKACJI
    with open('txtWCeluWeryfikacji/links.txt', 'w') as f:
        for link in links:
            f.write(str(link))
            f.write("\n")

    with open('txtWCeluWeryfikacji/photoLinks.txt', 'w') as f:
        for link in photoLinks:
            f.write(str(link))
            f.write("\n")

    print("Pobrano linki do indywidualnych profilów zawodniczek.\nStworzono plik z nazwiskami oraz linkami do zdjęć.")
