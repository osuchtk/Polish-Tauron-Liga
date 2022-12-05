########################################################################################################################
# KONTORLA BAZY DANYCH #################################################################################################
########################################################################################################################
import mariadb
import sys
import pandas as pd
import mariaDBCredentials


def connectToDatabase():
    # próba zalogowania do MariaDB
    try:
        conn = mariadb.connect(
            user=mariaDBCredentials.user,
            password=mariaDBCredentials.password,
            host=mariaDBCredentials.host,
            port=mariaDBCredentials.port,
            database="sys"
        )
    except mariadb.Error:
        print("Błąd łączenia z bazą danych")
        sys.exit(1)

    cur = conn.cursor()

    # utworzenie odpowiedniej bazy
    try:
        cur.execute("CREATE DATABASE SIATKOWKA COLLATE = 'utf8mb3_general_ci'")
    except mariadb.ProgrammingError:
        pass

    # zalogowanie do nowo utworzonej bazy danych
    try:
        conn = mariadb.connect(
            user=mariaDBCredentials.user,
            password=mariaDBCredentials.password,
            host=mariaDBCredentials.host,
            port=mariaDBCredentials.port,
            database="siatkowka"
        )

    except mariadb.Error:
        print("Błąd łączenia z bazą danych")
        sys.exit(1)

    cur = conn.cursor()

    return conn, cur


def readCSVFiles(SquadListFilename, PlayerInfoFilename, oldSystemFileName, newSystemFileName, standingsFileName,
                 matchesInfoFileName, combinedStats):
    # wczytanie plików do zapisania do bazy danych
    playerInfo = pd.read_csv("./CSV/" + PlayerInfoFilename + ".csv", sep=';', low_memory=False,
                             encoding='windows-1250')
    statsOld = pd.read_csv("./CSV/" + oldSystemFileName + ".csv", sep=';', low_memory=False,
                           encoding='windows-1250')
    statsNew = pd.read_csv("./CSV/" + newSystemFileName + ".csv", sep=';', low_memory=False,
                           encoding='windows-1250')
    standings = pd.read_csv("./CSV/" + standingsFileName + ".csv", sep=';', low_memory=False,
                            encoding='windows-1250')
    matchesInfo = pd.read_csv("./CSV/" + matchesInfoFileName + ".csv", sep=';', low_memory=False,
                              encoding='windows-1250')
    teamSquads = pd.read_csv("./CSV/" + SquadListFilename + ".csv", sep=';', low_memory=False,
                             encoding='windows-1250')
    combinedStats = pd.read_csv("./CSV/" + combinedStats + ".csv", sep=';', low_memory=False,
                                encoding='windows-1250')

    return playerInfo, statsOld, statsNew, standings, matchesInfo, teamSquads, combinedStats


def createTablePlayerInfo(conn, cur, playerInfoData):
    # tworzenie tabeli na podstawie pliku playerInfo
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE playerInfo (Nazwisko VARCHAR(255) NOT NULL, Zdjęcie VARCHAR(255) NOT NULL,"
                    "Profil VARCHAR(255) NOT NULL, `Data urodzenia` VARCHAR(15) NOT NULL, Pozycja VARCHAR(20) NOT NULL,"
                    "Wzrost VARCHAR(5) NOT NULL, Waga VARCHAR(5) NOT NULL, Zasięg VARCHAR(5) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in playerInfoData.iterrows():
        cur.execute("INSERT INTO siatkowka.playerInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik playerInfo.")


def createTableStatsOld(conn, cur, statsOld):
    # tworzenie tabeli na podstawie starych statystyk
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE statsOld (`I` VARCHAR(5), `II` VARCHAR(5), `III` VARCHAR(5), `IV` VARCHAR(5),"
                    "`V` VARCHAR(5), `Punkty` INT,"
                    "`Liczba zagrywek` INT, `As` INT, `Bledy zagrywki` INT, `Asy na set` INT,"
                    "`Liczba przyjec zgrywki` INT, `Bledy przyjecie` INT, `Przyjecie negatywne` INT,"
                    "`Przyjecie pozytywne` INT, `Przyjecie pozytywne %` INT, `Przyjecie perfekcyjne` INT,"
                    "`Przyjecie perfekcyjne %` INT,"
                    "`Liczba atakow` INT, `Bledy atak` INT, `Blok` INT, `Atak perfekcyjny` INT,"
                    "`Atak perfekcyjny %` INT,"
                    "`Blok punkty` INT, `Pkt na set` INT,"
                    "`Nazwisko` VARCHAR(255) NOT NULL, `Klub` VARCHAR(255) NOT NULL, `Klucz` VARCHAR(255) NOT NULL,"
                    "`Data spotkania` VARCHAR(20) NOT NULL, `Sezon` VARCHAR(20) NOT NULL,"
                    "`Faza` VARCHAR(15) NOT NULL, `Kolejka` VARCHAR(5) NOT NULL)")
    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in statsOld.iterrows():
        cur.execute("INSERT INTO siatkowka.statsOld VALUES (%s, %s, %s, %s, %s, %d,"
                    "%d, %d, %d, %d,"
                    "%d, %d, %d, %d, %d, %d, %d,"
                    "%d, %d, %d, %d, %d,"
                    "%d, %d,"
                    "%s, %s, %s, %s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik ze starym systemem statystyk.")


def createTableStatsNew(conn, cur, statsNew):
    # tworzenie tabeli na podstawie nowych statystyk
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE statsNew (`I` VARCHAR(5), `II` VARCHAR(5), `III` VARCHAR(5), `IV` VARCHAR(5),"
                    " `V` VARCHAR(5), `GS` VARCHAR(2),"
                    "`Suma` INT, `BP` INT, `z-s` INT,"
                    "`Liczba zagrywek` INT, `Bledy zagrywki` INT, `As` INT, `Efektywność zagrywki %%` INT,"
                    "`Liczba przyjec zgrywki` INT, `Bledy przyjecie` INT, `Przyjecie pozytywne %` INT,"
                    "`Przyjecie perfekcyjne` INT,"
                    "`Liczba atakow` INT, `Bledy atak` INT, `Blok` INT, `Punkty z ataku` INT,"
                    "`Skutecznosc ataku %` INT, `Efektywnosc ataku` INT,"
                    "`Punkty w bloku` INT, `Wyblok` INT,"
                    "`Nazwisko` VARCHAR(255) NOT NULL, `Klub` VARCHAR(255) NOT NULL, `Klucz` VARCHAR(255) NOT NULL,"
                    "`Data spotkania` VARCHAR(20) NOT NULL, `Sezon` VARCHAR(20) NOT NULL,"
                    "`Faza` VARCHAR(15) NOT NULL, `Kolejka` VARCHAR(5) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in statsNew.iterrows():
        cur.execute("INSERT INTO siatkowka.statsNew VALUES (%s, %s, %s, %s, %s, %s,"
                    "%d, %d, %d,"
                    "%d, %d, %d, %d,"
                    "%d, %d, %d, %d,"
                    "%d, %d, %d, %d, %d, %d,"
                    "%d, %d,"
                    "%s, %s, %s, %s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik z nowym systemem statystyk.")


def createTableStandings(conn, cur, standings):
    # tworzenie tabeli na podstawie pliku standings
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE standings (Pozycja VARCHAR(3) NOT NULL, Klub VARCHAR(255) NOT NULL,"
                    "Sezon VARCHAR(20) NOT NULL, Logo VARCHAR(255) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in standings.iterrows():
        cur.execute("INSERT INTO siatkowka.standings VALUES (%s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik standings.")


def createTableMatchesInfo(conn, cur, matchesInfoData):
    # tworzenie tabeli na podstawie pliku matchesInfo
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE matchesInfo (`Druzyna A` VARCHAR(255) NOT NULL, `Druzyna B` VARCHAR(255) NOT NULL,"
                    "`Wynik A` VARCHAR(5) NOT NULL, `Wynik B` VARCHAR(5) NOT NULL, Lokalizacja VARCHAR(5) NOT NULL,"
                    "`Data meczu` VARCHAR(50) NOT NULL, Klucz VARCHAR(255) NOT NULL, Sezon VARCHAR(20) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in matchesInfoData.iterrows():
        cur.execute("INSERT INTO siatkowka.matchesInfo VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik matchesInfo.")


# do usunięcia
def createTableSquadsInfo(conn, cur, squads):
    # tworzenie tabeli na podstawie pliku matchesInfo
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE teamsSquads (Nazwisko VARCHAR(255) NOT NULL, Klub VARCHAR(255) NOT NULL,"
                    "Sezon VARCHAR(255) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in squads.iterrows():
        cur.execute("INSERT INTO siatkowka.teamsSquads VALUES (%s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik teamsSquads.")


def createTableStatsCombined(conn, cur, combinedStats):
    # tworzenie tabeli na podstawie nowych statystyk
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE combinedStats (`I` VARCHAR(5), `II` VARCHAR(5), `III` VARCHAR(5), `IV` VARCHAR(5),"
                    " `V` VARCHAR(5), `GS` VARCHAR(2), `Suma punktow` INT,"
                    "`Liczba zagrywek` INT, `Bledy zagrywki` INT, `As` INT,"
                    "`Liczba przyjec` INT, `Bledy przyjecie` INT, `Przyjecie pozytywne %` INT,"
                    "`Przyjecie perfekcyjne %` INT,"
                    "`Liczba atakow` INT, `Bledy atak` INT, `Atak zablokowany` INT, `Punkty z ataku` INT, "
                    "`Skutecznosc ataku %` INT,"
                    "`Punkty w bloku` INT,"
                    "`Nazwisko` VARCHAR(255) NOT NULL, `Klub` VARCHAR(255) NOT NULL, `Klucz` VARCHAR(255) NOT NULL,"
                    "`Data spotkania` VARCHAR(20) NOT NULL, `Sezon` VARCHAR(20) NOT NULL,"
                    "`Faza` VARCHAR(15) NOT NULL, `Kolejka` VARCHAR(5) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in combinedStats.iterrows():
        cur.execute("INSERT INTO siatkowka.combinedStats VALUES (%s, %s, %s, %s, %s, %s, %d,"
                    "%d, %d, %d,"
                    "%d, %d, %d, %d,"
                    "%d, %d, %d, %d, %d,"
                    "%d,"
                    "%s, %s, %s, %s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik z poączonymi statystykami.")
