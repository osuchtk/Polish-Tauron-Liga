########################################################################################################################
### PLIK Z FUNKCJAMI ###################################################################################################
########################################################################################################################
import pandas as pd

# lista linków do pobierania list zawodniczek
def playerListLinks(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/statsPlayers/tournament_1/{}.html?memo=%7B%22players%22%3A%7B%22mainFilter%22%3A%22letter%22%2C%22subFilter%22%3A%22all%22%7D%7D".format(year))

    return searchURLs


# lista linków do pobierania meczów w sezonie
def matchesListLinks(start, end):
    period = range(start, end + 1, 1)
    period = list(period)

    searchURLs = []
    for year in period:
        searchURLs.append("https://www.tauronliga.pl/games/tour/{}.html".format(year))

    return searchURLs


# nagłówki do pliku z nazwiskami i linkami do zdjęć zawodniczek
def prepareCSV_surnamePhotos(filename):
    df = pd.DataFrame(columns = ["Nazwisko", "Link", "Sezon"])

    #try:
    #    print("Stworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    return df.to_csv('CSV/' + filename + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV z nazwiskami i linkami do zdjęć.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)


# nagłówki do plików z bezpośrednimi statystykami
def prepareCSV_newSystem(filename):
    df = pd.DataFrame(columns = ["I", "II", "III", "IV", "V", "GS", # Set
                                 "suma", "BP", "z-s", # Punkty
                                 "Liczba", "bł", "as", "eff%", # Zagrywka
                                 "liczba", "bł1", "poz%", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "bł2", "blok", "Pkt", "skut%", "eff%1", # Atak
                                 "pkt", "wyblok", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania", "Sezon"# Inne
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
                                 "Liczba", "as", "bł", "Asy na set", # Zagrywka
                                 "liczba", "bł1", "Neg", "Poz", "poz%", "Perf", "perf%", # Przyjęcie zagrywki
                                 "liczba1", "bł2", "blok", "Perf1", "% perf", # Atak
                                 "pkt", "Pkt na set", # Blok
                                 "Nazwisko", "Klub", "Klucz", "Data spotkania", "Sezon" # Inne
                                 ])

    #try:
    #    print("Stworzono szkielet pliku CSV ze statystykami w starym systemie.")
    return df.to_csv('CSV/' + fileName + '.csv', mode='x', index=False, encoding='windows-1250', sep=";", header=True)

    #except FileExistsError:
    #    print("Plik istnieje. Usuwam\nStworzono szkielet pliku CSV ze statystykami w starym systemie.")
    #    os.remove("D:/Naukowe/WI_ZUT/Praca Inżynierska/CSV/" + nazwaPliku + ".csv")
    #    return df.to_csv('CSV/' + nazwaPliku, mode='x', index=False, encoding='windows-1250', sep=";", header=True)




