########################################################################################################################
### POBRANIE POZYCJI KLUBÓW NA KONIEC SEZONÓW ##########################################################################
########################################################################################################################
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def getStandings(searchURL, filename):
    for link in searchURL:
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        # listy na miejsca i logo klubów
        clubNamesStandindList = []
        standingNumberList = []
        clubLogoLinkList = []
        seasonList = []

        # sezon
        season = str(link).split("/")[5].split(".")[0]
        seasonValue = str(season) + "/" + str(int(season) + 1)

        # miejsca z podium
        firtsPlace = soup.select(".podium-name")[0].text
        firtsPlacePhotoLink = str(soup.select(".podium-logo")[0]).split("src")[1].split('"')[1]

        secondPlace = soup.select(".podium-name")[1].text
        secondPlacePhotoLink = str(soup.select(".podium-logo")[1]).split("src")[1].split('"')[1]

        thirdPlace = soup.select(".podium-name")[2].text
        thirdPlacePhotoLink = str(soup.select(".podium-logo")[2]).split("src")[1].split('"')[1]

        clubNamesStandindList.append(firtsPlace)
        clubNamesStandindList.append(secondPlace)
        clubNamesStandindList.append(thirdPlace)

        clubLogoLinkList.append(firtsPlacePhotoLink)
        clubLogoLinkList.append(secondPlacePhotoLink)
        clubLogoLinkList.append(thirdPlacePhotoLink)

        # miejsca spoza podium
        furtherPlaces = soup.select(".row.podium-list")

        for place in furtherPlaces:
            placeNumber = str(place).split("src")[0].split("span")[1].split(">")[1].split("<")[0]
            clubName = str(place).split("src")[1].split(">")[5].split("<")[0]
            clubLogoLink = str(place).split("src")[1].split('"')[1]

            clubNamesStandindList.append(clubName)
            clubLogoLinkList.append(clubLogoLink)

        # utworzenie listy z numerami miejsc
        for index, _ in enumerate(clubNamesStandindList):
            standingNumberList.append(index + 1)
            seasonList.append(seasonValue)

        data = pd.DataFrame(data = [standingNumberList, clubNamesStandindList, seasonList, clubLogoLinkList])
        data = data.T
        data.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)

    print("Zakończono pobieranie pozycji zespołów na koniec sezonów.")

