import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen


def getSquads(linksList, filename):
    allDataAppended = []

    for link in linksList:
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        teamSquad = soup.select(".table.alignmiddle.table-striped")[0]

        headers = []
        for columnName in teamSquad.find_all('th'):
            title = columnName.text.replace('\n', '').replace('\xa0', '')
            headers.append(title)
        headers.insert(0, "temp")

        df = pd.DataFrame(columns = headers)
        allData = pd.DataFrame(columns = headers)

        for j in teamSquad.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [k.text for k in row_data]
            length = len(df)
            df.loc[length] = row
            allData.loc[length] = row

        teamNameList = []
        seasonList = []

        teamName = soup.find("h1").text
        season = str(link).split("/")[7].split(".")[0]
        seasonValue = str(season + "/" + str(int(season) + 1))

        for player in range(len(allData)):
            teamNameList.append(teamName)
            seasonList.append(seasonValue)


        allData.insert(len(allData.columns), "Klub", teamNameList)
        allData.insert(len(allData.columns), "Sezon", seasonList)

        allData.replace("Imię i nazwisko", "Nazwisko")
        del allData["temp"]
        del allData["Numer"]
        del allData["Pozycja"]

        allDataAppended.append(allData)

    #return allData
    allDataFinalDf = pd.concat(allDataAppended)

    print("Pobrano informacje o składach zespołów w sezonach.")
    allDataFinalDf.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";",
                          header=False)

