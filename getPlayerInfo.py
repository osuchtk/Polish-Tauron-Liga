########################################################################################################################
### POBRANIE INFORMACJI O ZAWODNICZKACH ################################################################################
########################################################################################################################
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd


def getInformationsAboutPlayers(dataframe):
    linksList = dataframe[2]

    nameList = []
    birthDateList = []
    positionList = []
    heightList = []
    weightList = []
    rangeList = []

    for index, link in enumerate(linksList):
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        # pobranie danych o nazwisku, dacie urodzenia i pozycji
        name = soup.find("h1").text
        birthDate = str(soup.select(".datainfo.small")[0]).split("<", 4)[2].split(">")[1]
        position = str(soup.select(".datainfo.small")[1]).split("<", 4)[2].split(">")[1]

        # pobranie danych o wzroście, wadze i zasięgu ataku
        height = str(soup.select(".datainfo.text-center")[0]).split("<", 4)[2].split(">")[1]
        weight = str(soup.select(".datainfo.text-center")[1]).split("<", 4)[2].split(">")[1]
        range = str(soup.select(".datainfo.text-center")[2]).split("<", 4)[2].split(">")[1]

        nameList.append(name)
        birthDateList.append(birthDate)
        positionList.append(position)
        heightList.append(height)
        weightList.append(weight)
        rangeList.append(range)

    data = pd.DataFrame(columns = ["Nazwisko", "Data urodzenia", "Pozycja", "Wzrost", "Waga", "Zasięg"],
                        data = [nameList, birthDateList, positionList, heightList, weightList, rangeList])
    #data.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)
    #return nameList, birthDateList, heightList, weightList, rangeList
    print("Pobrano informacje na temat zawodniczek.")
    return data
