########################################################################################################################
### PLIK Z FUNKCJAMI ###################################################################################################
########################################################################################################################
import pandas as pd
import os
import shutil

from bs4 import BeautifulSoup
from urllib.request import urlopen

########################################################################################################################
# PRZYGOTOWANIE LINKÓW DO POBIERANIA DANYCH
# lista linków do pobierania list zawodniczek
def playerLinksList(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/statsPlayers/tournament_1/{}.html?memo=%7B%22players%22%3A%7B%22"
                          "mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D".format(year))

    return searchURLs


# lista linków do pobierania meczów w sezonie
def matchesLinksList(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/games/tour/{}.html".format(year))

    return searchURLs


# linki do końcowych klasyfikacji sezonów
def standingsLinksList(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/table/tour/{}.html".format(year))

    return searchURLs


# linki do zespołów grających w danym sezonie
def teamsInSeasonLinksList(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/teams/tour/{}.html".format(year))

    linksList = []
    for link in searchURLs:
        page = urlopen(link)
        soup = BeautifulSoup(page, "lxml")

        clubsLinks = soup.select(".col-sm-6.col-md-6.col-lg-4")

        for club in clubsLinks:
            clubLink = "https://www.tauronliga.pl" + str(club).split("href")[1].split('"')[1]

            linksList.append(clubLink)

    return linksList

########################################################################################################################
# NAGŁÓWKI DO PLIKÓW CSV
# nagłówki do pliku z informacjami o meczach
def prepareCSV_matchesInfo(filename):
    df = pd.DataFrame(columns=["Druzyna Home", "Druzyna Away", "Wynik Home", "Wynik Away", "Lokalizacja", "Data meczu",
                               "Klucz", "Sezon"])

    # try:
    #    print("Stworzono szkielet pliku CSV z informacjami o meczach.")
    return df.to_csv('CSV/' + filename + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)


# nagłówki do plików z bezpośrednimi statystykami
def prepareCSV_newSystem(filename):
    df = pd.DataFrame(columns = ["I", "II", "III", "IV", "V", "GS", # Set
                                 "suma", "BP", "z-s", # Punkty
                                 "Liczba", "błędy zagrywka", "as", "eff%", # Zagrywka
                                 "liczba", "błędy przyjęcie", "poz%", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "błędy atak", "blok", "Pkt", "skut%", "eff%1", # Atak
                                 "pkt", "wyblok", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania", "Sezon", "Faza", "Kolejka" # Inne
                                 ])

    #try:
    #    print("Stworzono szkielet pliku CSV ze statystykami w nowym systemie.")
    return df.to_csv('CSV/' + filename + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV ze statystykami w starym systemie.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


def prepareCSV_oldSystem(fileName):
    df = pd.DataFrame(columns = ["I", "II", "III", "IV", "V", "Punkty", # punkty - sety
                                 "Liczba", "as", "błędy zagrywka", "Asy na set", # Zagrywka
                                 "liczba", "błędy przyjęcie", "Neg", "Poz", "poz%", "Perf", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "błędy atak", "blok", "Perf1", "% perf", # Atak
                                 "pkt", "Pkt na set", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania", "Sezon", "Faza", "Kolejka" # Inne
                                 ])

    #try:
    #    print("Stworzono szkielet pliku CSV ze statystykami w starym systemie.")
    return df.to_csv('CSV/' + fileName + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV ze statystykami w starym systemie.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


def prepareCSV_standings(filename):
    df = pd.DataFrame(columns = ["Pozycja", "Klub", "Sezon", "Logo"])

    #try:
    #    print("Stworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    return df.to_csv('CSV/' + filename + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


def prepareCSV_ClubSquadList(filename):
    df = pd.DataFrame(columns = ["Nazwisko", "Klub", "Sezon"])

    #try:
    #    print("Stworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    return df.to_csv('CSV/' + filename + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


########################################################################################################################
# TWORZENIE FOLDERU NA CSVKI
def makeCSVFolder():
    try:
        os.mkdir("./CSV")
    except FileExistsError:
        shutil.rmtree("./CSV")
        os.mkdir("./CSV")

