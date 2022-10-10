import glob
import os


def szukajKlubuPoNazwiskuISezonie(zawodniczka, sezon):
    # stworzenie listy plików
    listaPlikow = []
    os.chdir("D:/Naukowe/WI_ZUT/Praca Inżynierska/sklady/" + sezon)
    for file in glob.glob("*.txt"):
        listaPlikow.append(file)

    # szukanie zawodniczki w plikach
    # nazwisko dodawane do listy, aby obsłużyć przypadek kiedy zawodniczka zmieniła klub w trakcie sezonu
    druzyny = []
    for plik in listaPlikow:
        obecnyPlik = open(plik, "r", encoding="utf8")

        idx = 0

        for line in obecnyPlik:
            idx += 1

            if zawodniczka in line:
                druzyny.append(plik[:-4].replace("-", " "))

        obecnyPlik.close()

    return druzyny
