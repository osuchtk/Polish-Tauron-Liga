import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen


def getInfo(linksList, filename):
    allDataAppended = []

    for link in linksList:
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        # informacje o klubie
        teamName = soup.find("h1").text
        season = str(link).split("/")[7].split(".")[0]
        seasonValue = str(season + "/" + str(int(season) + 1))
        try:
            clubAddress = str(soup).split("Adres:")[1].split("<")[1].split(">")[1]
        except IndexError:
            clubAddress = ""

        try:
            ceo = str(soup).split("Prezes")[1].split(":")[1].split("<")[0]
        except IndexError:
            ceo = ""

        try:
            viceCeo = str(soup).split("Wiceprezes:")[1].split("<")[0]
        except IndexError:
            viceCeo = ""

        try:
            teamManager = str(soup).split("Menedżer drużyny:")[1].split("<")[0]
        except IndexError:
            #teamManager = str(soup).split("Manager ")[1].split(":")[1].split("<")[0]
            teamManager = ""
        #except:
        #    teamManager = ""

        try:
            firstCoach = str(soup).split("Pierwszy trener:")[1].split(">")[1].split("<")[0]
        except IndexError:
            firstCoach = ""

        try:
            secondCoach = str(soup).split("Drugi trener:")[1].split(">")[1].split("<")[0]
        except IndexError:
            secondCoach = ""

        infoDataframe = pd.DataFrame(data=[teamName, seasonValue, clubAddress, ceo, viceCeo, teamManager, firstCoach,
                                           secondCoach]).transpose()
        infoDataframe.replace("\r", "")
        infoDataframe.replace("\n", "")
        infoDataframe.replace("\t", "")
        infoDataframe.replace("\xa0", "")

        allDataAppended.append(infoDataframe)

    allDataFinalDf = pd.concat(allDataAppended)
    allDataFinalDf.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";",
                          header=False)
    print("Pobrano podstawowe informacje o zespołach.")