import pandas as pd
import os

########################################################################################################################
### PRZYGOTOWANIE NAGŁÓWKÓW DO PLIKU ZE STATYSTYKAMI ###################################################################
########################################################################################################################
# zwracany jest plik CSV, który posiada zdefiniowane nagłówki



########################################################################################################################
### POBRANIE TABEL ZE STATYSTYKAMI #####################################################################################
########################################################################################################################
# funkcja przyjmuje indeks (0, 1) - jest to indeks tabeli zespołu który nas interesuje: 0 -> pierwszy od góry, 1 - drugi od góry
# funkcja przyjmuje link do danego spotkania
# funkcja przyjmuje wartość string: "new" lub "old", który określa system tworzenia statystyk
# zwracany jest wypełniony dataframe dla jednego z klubów, które rozgrywały dany mecz
def getStats(index, soup, systemVersion):
    data = []

    # tworzenie unikalnego klucza z daty spotkania, drużyn oraz wyniku
    # iteracja po linkach w danym meczu
    teams = []
    for match in soup.findAll('a'):
        if "/teams/id/" in str(match.get('href')):
            teams.append(match.text)

    team1 = teams[0]
    team2 = teams[3]

    resultGeneral = soup.select('.gameresult')[-1].text.replace('\n', '')
    result1 = resultGeneral[0]
    result2 = resultGeneral[-1]

    matchDate = soup.select('.date')[-1].text

    key = matchDate[:-7] + team1 + "-" + result1 + ":" + result2 + "-" + team2

    ####################################################################################################################
    # BEZPOŚREDNIE STATYSTYKI

    # nowy system statystyk wprowadzony od sezonu 2020/2021
    if systemVersion == "new":
        try:
            statsTeam1 = soup.select(".rs-standings-table")[index]

            # zbieranie nagłówków
            for columnName in statsTeam1.find_all('th'):
                title = columnName.text.replace('\n', '').replace('\xa0', '')
                data.append(title)

            # if w celu obsłużenia przypadku kiedy był rozgrywany złoty set
            # przycięcie liczby nagłówków w celu pominięcia pustych komórek i obszarów gry (przycięcie od początku)
            # umieszczenie nazwisk w osobnej liście
            if "GS" in data:
                headers = data[8:33]
                surnames = data[33:]
            else:
                headers = data[8:32]
                surnames = data[32:]

            # przypisanie nagłówków do kolumn
            df = pd.DataFrame(columns=headers)
            allData = pd.DataFrame(columns=headers)
            #
            # dodanie indeksów do powtarzających się nagłówków
            temp = pd.Series(df.columns)
            df.columns = df.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)
            #
            temp = pd.Series(allData.columns)
            allData.columns = allData.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)

            for j in statsTeam1.find_all('tr')[2:-1]:
                row_data = j.find_all('td')
                row = [k.text for k in row_data]
                length = len(df)
                df.loc[length] = row
                allData.loc[length] = row

            # do dataframe'u, który nie posiada kolumny "Złoty set" jest dodawana ta kolumna z daną "-", która oznacza,
            # że Złoty Set nie był rozgrywany
            if "GS" not in allData.columns:
                allData.insert(5, "GS", "-")

            # przygotowanie list na statystyki spoza tabeli
            clubList = []
            keyList = []
            matchDateList = []
            for i in range(len(allData)):
                clubList.append(team1)
                keyList.append(key)
                matchDateList.append(matchDate)

            # dodanie do statystyk surnames zawodniczki, klubu oraz daty spotkania
            allData.insert(len(allData.columns), 'Nazwisko', surnames)
            allData.insert(len(allData.columns), 'Klub', clubList)
            allData.insert(len(allData.columns), 'Klucz', keyList)
            allData.insert(len(allData.columns), 'Data Spotkania', matchDateList)

            return allData

        except IndexError:
            print("Mecz bez statystyk. " + key)


    # stary system statystyk przez sezonem 2020/2021
    if systemVersion == "old":
        try:
            statsTeam1 = soup.select(".rs-standings-table")[index]

            # zbieranie nagłówków
            for columnName in statsTeam1.find_all('th'):
                title = columnName.text.replace('\n', '').replace('\xa0', '')
                data.append(title)

            # if w celu obsłużenia przypadku kiedy był rozgrywany złoty set
            # przycięcie liczby nagłówków w celu pominięcia pustych komórek i obszarów gry (przycięcie od początku)
            # umieszczenie nazwisk w osobnej liście
            headers = data[7:31]
            surnames = data[31:]

            # przypisanie nagłówków do kolumn
            df = pd.DataFrame(columns=headers)
            allData = pd.DataFrame(columns=headers)
            #
            # dodanie indeksów do powtarzających się nagłówków
            temp = pd.Series(df.columns)
            df.columns = df.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)
            #
            temp = pd.Series(allData.columns)
            allData.columns = allData.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)

            for j in statsTeam1.find_all('tr')[2:-1]:
                row_data = j.find_all('td')
                row = [k.text for k in row_data]
                length = len(df)
                df.loc[length] = row
                allData.loc[length] = row

            # przygotowanie list na statystyki spoza tabeli
            clubList = []
            keyList = []
            matchDateList = []
            for i in range(len(allData)):
                clubList.append(team1)
                keyList.append(key)
                matchDateList.append(matchDate)

            # dodanie do statystyk surnames zawodniczki, klubu oraz daty spotkania
            allData.insert(len(allData.columns), 'Nazwisko', surnames)
            allData.insert(len(allData.columns), 'Klub', clubList)
            allData.insert(len(allData.columns), 'Klucz', keyList)
            allData.insert(len(allData.columns), 'Data Spotkania', matchDateList)

            return allData

        except IndexError:
            print("Mecz bez statystyk. " + key)
