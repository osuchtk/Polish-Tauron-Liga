########################################################################################################################
### POBRANIE INFORMACJI O ZAWODNICZKACH ################################################################################
########################################################################################################################
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


def getInformations(dataframe, filename):
    playersPhotoLink = dataframe[1]
    playersProfileLink = dataframe[3]

    nameList = []
    clubList = []
    birthDateList = []
    positionList = []
    heightList = []
    weightList = []
    rangeList = []
    linkList = []
    photoList = []
    seasonList = []

    for index, link in enumerate(playersProfileLink):
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        # pobranie informacji o nazwisku i klubie
        name = str(soup.select(".playername")).split(">")[1].split("<")[0]
        club = str(soup.select(".playerteamname")).split("<", 6)[3].split(">")[1]

        # pobranie danych o dacie urodzenia i pozycji
        birthDate = str(soup.select(".datainfo.small")[0]).split("<", 4)[2].split(">")[1]
        position = str(soup.select(".datainfo.small")[1]).split("<", 4)[2].split(">")[1]

        # pobranie danych o wzroście, wadze i zasięgu ataku
        height = str(soup.select(".datainfo.text-center")[0]).split("<", 4)[2].split(">")[1]
        weight = str(soup.select(".datainfo.text-center")[1]).split("<", 4)[2].split(">")[1]
        range = str(soup.select(".datainfo.text-center")[2]).split("<", 4)[2].split(">")[1]

        # dodanie wartości sezonu
        try:
            season = str(soup.select(".btn.btn-default.listlike")).split("Sezon")[1].split("<")[0]
        except IndexError:
            season = str(soup.select(".btn.btn-default.dropdown-toggle.form-control")).split("Sezon")[1].split("<")[0]

        # dodanie danych do list
        nameList.append(name)
        clubList.append(club)
        birthDateList.append(birthDate)
        positionList.append(position)
        heightList.append(height)
        weightList.append(weight)
        rangeList.append(range)
        linkList.append(link)
        photoList.append(playersPhotoLink[index])
        seasonList.append(season)

    data = pd.DataFrame(data=[nameList, clubList, birthDateList, positionList, heightList, weightList,
                              rangeList, linkList, photoList, seasonList])
    data = data.T
    data.fillna(0, inplace=True)
    data.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)

    print("Pobrano podstawowe informacje na temat zawodniczek.")

