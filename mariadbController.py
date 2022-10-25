import mariadb
import sys
import pandas as pd
import mariaDBCredentials

def connectToDatabase():
    # próba zalogowania do MariaDB
    try:
        conn = mariadb.connect(
            user = mariaDBCredentials.user,
            password = mariaDBCredentials.password,
            host = mariaDBCredentials.host,
            port = mariaDBCredentials.port,
            database = "sys"
        )
    except mariadb.Error:
        print("Błąd łączenia z bazą danych")
        sys.exit(1)

    cur = conn.cursor()

    # utworzenie odpowiedniej bazy
    try:
        cur.execute("CREATE DATABASE SIATKOWKA")
    except mariadb.ProgrammingError:
        pass

    # zalogowanie do nowo utworzonej bazy danych
    try:
        conn = mariadb.connect(
            user = mariaDBCredentials.user,
            password = mariaDBCredentials.password,
            host = mariaDBCredentials.host,
            port = mariaDBCredentials.port,
            database = "siatkowka"
        )

    except mariadb.Error:
        print("Błąd łączenia z bazą danych")
        sys.exit(1)

    cur = conn.cursor()

    return conn, cur


def readCSVFiles():
    # wczytanie plików do zapisania do bazy danych
    playerListData = pd.read_csv("./CSV/playerList.csv", sep = ';', low_memory = False, encoding='windows-1250')
    playerInfoData = pd.read_csv("./CSV/playerInfo.csv", sep = ';', low_memory = False, encoding='windows-1250')
    statsOld = pd.read_csv("./CSV/stats_OLD_SEASONS.csv", sep = ';', low_memory = False, encoding='windows-1250')
    statsNew = pd.read_csv("./CSV/stats_NEW_SEASONS.csv", sep = ';', low_memory = False, encoding='windows-1250')

    return playerListData, playerInfoData, statsOld, statsNew


def createTablePlayrList(conn, cur, playerListData):
    # tworzenie tabeli na podstawie pliku playerList
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE playerList (Nazwisko VARCHAR(255) NOT NULL, Zdjęcie VARCHAR(255) NOT NULL,"
                    "Sezon VARCHAR(20) NOT NULL, Profil VARCHAR(255) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in playerListData.iterrows():
        cur.execute("INSERT INTO siatkowka.playerList VALUES (%s, %s, %s, %s)", tuple(row))
        conn.commit()

    print("Załadowano do bazy danych plik playerList.")


def createTablePlayrInfo(conn, cur, playerInfoData):
    # tworzenie tabeli na podstawie pliku playerInfo
    try:
        # utworzenie tabeli z odpowiednimi kolumnami
        cur.execute("CREATE TABLE playerInfo (Klub VARCHAR(255) NOT NULL, `Data urodzenia` VARCHAR(20) NOT NULL,"
                    "Pozycja VARCHAR(20) NOT NULL, Wzrost VARCHAR(10) NULL, Waga VARCHAR(10) NULL,"
                    "Zasieg VARCHAR(10) NULL, Profil VARCHAR(255) NOT NULL)")

    except mariadb.OperationalError:
        pass

    # zapisanie danych do bazy danych
    for _, row in playerInfoData.iterrows():
        cur.execute("INSERT INTO siatkowka.playerInfo VALUES (%s, %s, %s, %s, %s, %s, %s)", tuple(row))
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
                    "`Nazwisko` VARCHAR (255) NOT NULL, `Klub` VARCHAR(255) NOT NULL, `Klucz` VARCHAR(255) NOT NULL,"
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
                    "`Liczba atakow` INT, `Bledy atak` INT, `Blok` INT, `Punkty z ataku` INT, `Skutecznosc ataku %` INT,"
                    "`Efektywnosc ataku` INT,"
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


#cur.execute("DROP DATABASE SIATKOWKA")
