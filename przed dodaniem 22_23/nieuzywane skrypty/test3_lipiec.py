from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import time
import numpy as np

from playedInTeam_function import szukajKlubuPoNazwiskuISezonie
########################################################################################################################
### ODZYSKANIE LINKÓW Z PLIKÓW TEKSTOWYCH ##############################################################################
########################################################################################################################
links = []
photoLinks = []
with open('links.txt', 'r') as f:
    for link in f:
        links.append(link)

with open('photoLinks.txt', 'r') as f:
    for link in f:
        photoLinks.append(link)

# print(links)
# print(photoLinks)

# STRUKTURA PLIKU
# wszystkie statystyki | nazwisko | klub (!!!) | sezon


data = []
# allData = pd.DataFrame(columns=["Rozegrane mecze", "Sety", "Punkty",
#                                 "Suma zagrywka", "As zagrywka", "Błąd zagrywka", "Asy na set zagrywka"
#                                 "Suma przyjęcie", "Błąd przyjęcie", "Negatywne przyjęcie", "Perfekcyjne przyjęcie", "% perfekcyjnego przyjęcia",
#                                 "Suma atak", "Błąd atak", "Blok atak", "Perfekcyjny atak", "% perfekcyjnego ataku",
#                                 "Punkty blok", "Punkty na set blok"])

allData = pd.DataFrame()
########################################################################################################################
### ITERACJA PO ZAWODNICZKACH I POBRANIE STATYSTYK #####################################################################
########################################################################################################################
for i in links[0:1]:
    i = i.rstrip('\n')
    searchURL = "https://www.tauronliga.pl" + i
    page = urlopen(searchURL)

    soup = BeautifulSoup(page, "lxml")

    #print(soup)

    # nazwisko i sezon się przyda do pliku ze statystykami
    nazwisko = soup.find("h1")

    przyciskSezon = soup.findAll("button", class_ = "btn btn-default dropdown-toggle form-control")
    sezon = [i.text for i in soup.findAll("button", class_ = "btn btn-default dropdown-toggle form-control")]
    sezon = sezon[0].replace("/", "-").replace("\n", "").lstrip("Sezon ")

    table = soup.select(".rs-standings-table")[1]
    #print(table)

    for columnName in table.find_all('th'):
        title = columnName.text
        data.append(title)

    df = pd.DataFrame(columns=data[7:]) # + ["Nazwisko", "Sezon", "Klub"]
    allData = pd.DataFrame(columns=data[7:])
    #
    temp = pd.Series(df.columns)
    df.columns = df.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)
    #
    temp = pd.Series(allData.columns)
    allData.columns = allData.columns + temp.groupby(temp).cumcount().replace(0, '').astype(str)

    #temp = table.find_all('tr')[5:-2]
    for i in table.find_all('tr')[5:-2]:
        row_data = i.find_all('td')
        row = [j.text for j in row_data]
        length = len(df)
        df.loc[length] = row
        allData.loc[length] = row

    nazwiskoLista = []
    klubLista = []
    sezonLista = []
    for i in range(len(allData)):
        nazwiskoLista.append(nazwisko.text)
        klubLista.append(szukajKlubuPoNazwiskuISezonie(nazwisko.text, sezon))
        sezonLista.append(sezon.replace("-", "/"))

    allData.insert(len(allData.columns), 'Nazwisko', nazwiskoLista)
    allData.insert(len(allData.columns), 'Klub', klubLista)
    allData.insert(len(allData.columns), "Sezon", sezonLista)

    print(allData)






