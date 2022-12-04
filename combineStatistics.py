import pandas as pd
import numpy as np


def combineStats(oldFilename, newFilename, filenameToSave):
    oldStats = pd.read_csv("./CSV/" + oldFilename + ".csv", encoding='windows-1250', sep=";")
    newStats = pd.read_csv("./CSV/" + newFilename + ".csv", encoding='windows-1250', sep=";")

    oldStats.insert(5, "GS", "-")

    # sety i punkty
    firstSet = np.concatenate((oldStats["I"], newStats["I"]))
    secondSet = np.concatenate((oldStats["II"], newStats["II"]))
    thirdSet = np.concatenate((oldStats["III"], newStats["III"]))
    fourthSet = np.concatenate((oldStats["IV"], newStats["IV"]))
    fifthSet = np.concatenate((oldStats["V"], newStats["V"]))
    goldSet = np.concatenate((oldStats["GS"], newStats["GS"]))
    points = np.concatenate((oldStats["Punkty"], newStats["suma"]))
    # zagrywka
    serveNo = np.concatenate((oldStats["Liczba"], newStats["Liczba"]))
    serveError = np.concatenate((oldStats["błędy zagrywka"], newStats["błędy zagrywka"]))
    serveAce = np.concatenate((oldStats["as"], newStats["as"]))
    # przyjęcie
    receptionsNo = np.concatenate((oldStats["liczba"], newStats["liczba"]))
    receptionsErrors = np.concatenate((oldStats["błędy przyjęcie"], newStats["błędy przyjęcie"]))
    receptionsPositivePercent = np.concatenate((oldStats["poz%"], newStats["poz%"]))
    receptionsPerfectPercent = np.concatenate((oldStats["perf%"], newStats["perf%"]))
    # atak
    attacksNo = np.concatenate((oldStats["liczba1"], newStats["liczba1"]))
    attacksError = np.concatenate((oldStats["błędy atak"], newStats["błędy atak"]))
    attacksBlocked = np.concatenate((oldStats["blok"], newStats["blok"]))
    attacksPoints = np.concatenate((oldStats["Perf1"], newStats["Pkt"]))
    attacksEffectivenessPercent = np.concatenate((oldStats["% perf"], newStats["skut%"]))
    # blok
    blockPoints = np.concatenate((oldStats["pkt"], newStats["pkt"]))
    # pozostałe
    name = np.concatenate((oldStats["Nazwisko"], newStats["Nazwisko"]))
    club = np.concatenate((oldStats["Klub"], newStats["Klub"]))
    key = np.concatenate((oldStats["Klucz"], newStats["Klucz"]))
    matchDate = np.concatenate((oldStats["Data spotkania"], newStats["Data spotkania"]))
    season = np.concatenate((oldStats["Sezon"], newStats["Sezon"]))
    phase = np.concatenate((oldStats["Faza"], newStats["Faza"]))
    round = np.concatenate((oldStats["Kolejka"], newStats["Kolejka"]))

    statsArray = np.vstack((firstSet, secondSet, thirdSet, fourthSet, fifthSet, goldSet, points, # sety i punkty
                            serveNo, serveError, serveAce, #zagrywka
                            receptionsNo, receptionsErrors, receptionsPositivePercent, receptionsPerfectPercent, # przyjęcie
                            attacksNo, attacksError, attacksBlocked, attacksPoints, attacksEffectivenessPercent, # atak
                            blockPoints, # blok
                            name, club, key, matchDate, season, phase, round # pozostałe
                            )).T
    statsDataframe = pd.DataFrame(statsArray)
    statsDataframe.to_csv('CSV/' + filenameToSave + '.csv', mode='a', index=False, encoding='windows-1250', sep=";",
                          header=False)
