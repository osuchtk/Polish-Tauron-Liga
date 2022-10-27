import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

def getMatches(searachURLsList, filename):
    team1List = []
    team2List = []
    result1List = []
    result2List = []
    matchDateList = []
    keyList = []
    seasonList = []

    for index, i in enumerate(searachURLsList):
        i = i.rstrip('\n')
        searchURL = "https://www.tauronliga.pl/" + i
        page = urlopen(searchURL)
        soup = BeautifulSoup(page, "lxml")

        # tworzenie unikalnego klucza z daty spotkania, drużyn oraz wyniku
        team1 = str(soup.select(".col-xs-4.col-sm-3.tablecell")[0]).split(">", 5)[3].split("<")[0]
        team2 = str(soup.select(".col-xs-4.col-sm-3.tablecell")[1]).split(">", 5)[3].split("<")[0]

        resultGeneral = soup.select('.gameresult')[-1].text.replace('\n', '')
        result1 = resultGeneral[0]
        result2 = resultGeneral[-1]

        matchDate = soup.select('.date')[-1].text[:-7]
        matchDate = matchDate.replace("\r", "")
        matchDate = matchDate.replace("\n", "")
        matchDate = matchDate.replace("\t", "")

        key = matchDate[:-7] + team1 + "-" + result1 + ":" + result2 + "-" + team2
        key = key.replace("\r", "")
        key = key.replace("\n", "")
        key = key.replace("\t", "")

        # dodanie wartości sezonu
        season = matchDate.split(',')[0].split('.', 2)[2]
        seasonValue = str(season) + "/" + str(int(season) + 1)

        team1List.append(team1)
        team2List.append(team2)
        result1List.append(result1)
        result2List.append(result2)
        matchDateList.append(matchDate)
        keyList.append(key)
        seasonList.append(seasonValue)

        print(index, "/", len(searachURLsList))

    data = pd.DataFrame(data=[team1List, team2List, result1List, result2List, matchDateList, keyList, seasonList])
    data = data.T
    data.fillna(0, inplace=True)
    data.to_csv('CSV/' + filename + '.csv', mode='a', index=False, encoding='windows-1250', sep=";", header=False)


