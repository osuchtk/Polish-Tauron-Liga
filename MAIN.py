import time

from getLinksToPlayersPhotos import getLastnamePhotoLinks
from getLinksToMatches import getMatchesLinks
from usefulFunctions import playerListLinks, matchesListLinks,\
    prepareCSV_surnamePhotos, prepareCSV_newSystem, prepareCSV_oldSystem
from scrapStatistics import scrapStatiscics

# początek pomiaru czasu w celach statystycznych
timeStart = time.time()

# deklaracja przedziału czasowego dla którego pobierane są dane
start = 2018
end = 2021

# deklaracja nzaw plików przekazywanych do funkcji
lastnamePhotosFilename = "nazwisko_zdjecie"
oldSystemFileName = "statystyki_SEZONY_STARE"
newSystemFileName = "statystyki_SEZONY_NOWE"

# pobranie stron z linkami do profilów zawodniczek
playerListLinksURLs = playerListLinks(start, end)

# pobranie stron do wszystkich meczów w sezonie
matchesListLinksURLs = matchesListLinks(start, end)


# pobranie nazwisk zawodniczek i linków do zdjęć
prepareCSV_surnamePhotos(lastnamePhotosFilename)
getLastnamePhotoLinks(playerListLinksURLs, lastnamePhotosFilename)

# pobranie linków do wszystkich meczy w zadanym przedziale czasowym
links = getMatchesLinks(matchesListLinksURLs)


# przygotowanie nagłówków do pliku ze statystykami
prepareCSV_oldSystem(oldSystemFileName)
prepareCSV_newSystem(newSystemFileName)

# bezpośrednie pobieranie statystyk i ich zapis do plików
stats = scrapStatiscics(links, newSystemFileName, oldSystemFileName)


# koniec pomiaru czasu w celach statystycznych
timeEnd = time.time()
czas = timeEnd - timeStart
print("Czas wykonywania: ", czas, 'sekund')
