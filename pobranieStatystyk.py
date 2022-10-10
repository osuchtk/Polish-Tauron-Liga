import pandas as pd
import os

########################################################################################################################
### PRZYGOTOWANIE NAGŁÓWKÓW DO PLIKU ZE STATYSTYKAMI ###################################################################
########################################################################################################################
# zwracany jest plik CSV, który posiada zdefiniowane nagłówki
def prepareCSV_newSystem(nazwaPliku):
    df = pd.DataFrame(columns = ["I", "II", "III", "IV", "V", "GS", # Set
                                 "suma", "BP", "z-s", # Punkty
                                 "Liczba", "bł", "as", "eff%", # Zagrywka
                                 "liczba", "bł1", "poz%", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "bł2", "blok", "Pkt", "skut%", "eff%1", # Atak
                                 "pkt", "wyblok", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania" # Inne
                                 ])

    #try:
    #    print("Stworzono szkielet pliku CSV ze statystykami w nowym systemie.")
    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV ze statystykami w starym systemie.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


def prepareCSV_oldSystem(nazwaPliku):
    df = pd.DataFrame(columns = ["I", "II", "III", "IV", "V", "Punkty", # punkty - sety
                                 "Liczba", "as", "bł", "Asy na set", # Zagrywka
                                 "liczba", "bł1", "Neg", "Poz", "poz%", "Perf", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "bł2", "blok", "Perf1", "% perf", # Atak
                                 "pkt", "Pkt na set", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania" # Inne
                                 ])

    #try:
    #    print("Stworzono szkielet pliku CSV ze statystykami w starym systemie.")
    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV ze statystykami w starym systemie.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)



########################################################################################################################
### POBRANIE TABEL ZE STATYSTYKAMI #####################################################################################
########################################################################################################################
# funkcja przyjmuje indeks (0, 1) - jest to indeks tabeli zespołu który nas interesuje: 0 -> pierwszy od góry, 1 - drugi od góry
# funkcja przyjmuje link do danego spotkania
# funkcja przyjmuje wartość string: "new" lub "old", który określa system tworzenia statystyk
# zwracany jest wypełniony dataframe dla jednego z klubów, które rozgrywały dany mecz
def getStats(indeks, soup, system):
    dane = []
    allData = pd.DataFrame()

    # tworzenie unikalnego klucza z daty spotkania, drużyn oraz wyniku
    # iteracja po linkach w danym meczu
    druzyny = []
    for mecz in soup.findAll('a'):
        if "/teams/id/" in str(mecz.get('href')):
            druzyny.append(mecz.text)

    druzyna1 = druzyny[0]
    druzyna2 = druzyny[3]

    wynikOgolny = soup.select('.gameresult')[-1].text.replace('\n', '')
    wynik1 = wynikOgolny[0]
    wynik2 = wynikOgolny[-1]

    dataSpotkania = soup.select('.date')[-1].text

    klucz = dataSpotkania[:-7] + druzyna1 + "-" + wynik1 + ":" + wynik2 + "-" + druzyna2

    ####################################################################################################################
    # BEZPOŚREDNIE STATYSTYKI

    # nowy system statystyk wprowadzony od sezonu 2020/2021
    if system == "new":
        try:
            statystykiDruzyna1 = soup.select(".rs-standings-table")[indeks]

            # zbieranie nagłówków
            for columnName in statystykiDruzyna1.find_all('th'):
                title = columnName.text.replace('\n', '').replace('\xa0', '')
                dane.append(title)

            # if w celu obsłużenia przypadku kiedy był rozgrywany złoty set
            # przycięcie liczby nagłówków w celu pominięcia pustych komórek i obszarów gry (przycięcie od początku)
            # umieszczenie nazwisk w osobnej liście
            if "GS" in dane:
                naglowki = dane[8:33]
                nazwiska = dane[33:]
            else:
                naglowki = dane[8:32]
                nazwiska = dane[32:]

            # przypisanie nagłówków do kolumn
            df = pd.DataFrame(columns=naglowki)
            allData = pd.DataFrame(columns=naglowki)
            #
            # dodanie indeksów do powtarzających się nagłówków
            temp = pd.Series(df.columns)
            df.columns = df.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)
            #
            temp = pd.Series(allData.columns)
            allData.columns = allData.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)

            for j in statystykiDruzyna1.find_all('tr')[2:-1]:
                row_data = j.find_all('td')
                row = [k.text for k in row_data]
                length = len(df)
                df.loc[length] = row
                allData.loc[length] = row

            # do dataframe'u, który nie posiada kolumny "Złoty set" jest dodawana ta kolumna z daną "-", która oznacza,
            # że Złoty Set nie był rozgrywany
            if "GS" not in allData.columns:
                allData.insert(5, "GS", "-")

            klubLista = []
            kluczLista = []
            dataSpotkaniaLista = []
            for i in range(len(allData)):
                klubLista.append(druzyna1)
                kluczLista.append(klucz)
                dataSpotkaniaLista.append(dataSpotkania)

            # dodanie do statystyk nazwiska zawodniczki, klubu oraz daty spotkania
            allData.insert(len(allData.columns), 'Nazwisko', nazwiska)
            allData.insert(len(allData.columns), 'Klub', klubLista)
            allData.insert(len(allData.columns), 'Klucz', kluczLista)
            allData.insert(len(allData.columns), 'Data Spotkania', dataSpotkaniaLista)

            return allData

        except IndexError:
            print("Mecz bez statystyk. " + klucz)


    # stary system statystyk przez sezonem 2020/2021
    if system == "old":
        try:
            statystykiDruzyna1 = soup.select(".rs-standings-table")[indeks]

            # zbieranie nagłówków
            for columnName in statystykiDruzyna1.find_all('th'):
                title = columnName.text.replace('\n', '').replace('\xa0', '')
                dane.append(title)

            # if w celu obsłużenia przypadku kiedy był rozgrywany złoty set
            # przycięcie liczby nagłówków w celu pominięcia pustych komórek i obszarów gry (przycięcie od początku)
            # umieszczenie nazwisk w osobnej liście
            naglowki = dane[7:31]
            nazwiska = dane[31:]

            # przypisanie nagłówków do kolumn
            df = pd.DataFrame(columns=naglowki)
            allData = pd.DataFrame(columns=naglowki)
            #
            # dodanie indeksów do powtarzających się nagłówków
            temp = pd.Series(df.columns)
            df.columns = df.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)
            #
            temp = pd.Series(allData.columns)
            allData.columns = allData.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)

            for j in statystykiDruzyna1.find_all('tr')[2:-1]:
                row_data = j.find_all('td')
                row = [k.text for k in row_data]
                length = len(df)
                df.loc[length] = row
                allData.loc[length] = row

            klubLista = []
            kluczLista = []
            dataSpotkaniaLista = []
            for i in range(len(allData)):
                klubLista.append(druzyna1)
                kluczLista.append(klucz)
                dataSpotkaniaLista.append(dataSpotkania)

            # dodanie do statystyk nazwiska zawodniczki, klubu oraz daty spotkania
            allData.insert(len(allData.columns), 'Nazwisko', nazwiska)
            allData.insert(len(allData.columns), 'Klub', klubLista)
            allData.insert(len(allData.columns), 'Klucz', kluczLista)
            allData.insert(len(allData.columns), 'Data Spotkania', dataSpotkaniaLista)

            return allData

        except IndexError:
            print("Mecz bez statystyk. " + klucz)
