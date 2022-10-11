########################################################################################################################
### POBRANIE NAZWISK, ZDJĘĆ I LINKÓW DO PROFILI ZAWODNICZEK ############################################################
########################################################################################################################
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def getPlayers(searchURL, filename):
    linksAll = []
    photoLinks = []
    playernameList = []
    playerProfileList = []
    season = []
    for i in searchURL:
        page = urlopen(i)
        soup = BeautifulSoup(page, "lxml")

        # przeszukiwanie wszystkich linków na stronie w celu znalezienia tych, które spełniają kryteria
        for id, link in enumerate(soup.findAll('a')):
            if "/statsPlayers/id/" in str(link.get('href')):
                # if id % 2 == 0:
                linksAll.append(link)

                if id % 2 != 0:
                    seasonValue = str(i[52:56]) + "/" + str(int(i[52:56]) + 1)
                    season.append(seasonValue)

    for link in linksAll:
        if "img-responsive" in str(link):
            imgData = str(link).split('"', 11)
            photoLinks.append(imgData[9])
            playernameList.append(imgData[3])
            profileLink = "https://www.tauronliga.pl/players/id/" + str(link).split('"', 11)[1].split("/")[3]
            playerProfileList.append(profileLink)


    data = pd.DataFrame(data = [playernameList, photoLinks, season, playerProfileList])
    data = data.T
    data.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header = False)


    # ZAPISANIE LINKÓW DO PLIKÓW TEKSTOWYCH W CELU WERYFIKACJI
    # with open('txtWCeluWeryfikacji/links.txt', 'w') as f:
    #     for link in linksAll:
    #         f.write(str(link))
    #         f.write("\n")
    #
    # with open('txtWCeluWeryfikacji/photoLinks.txt', 'w') as f:
    #     for link in photoLinks:
    #         f.write(str(link))
    #         f.write("\n")

    print("Pobrano nazwiska zawodniczek, linki do indywidualnych profilów zawodniczek oraz zdjęć.")
    return data
