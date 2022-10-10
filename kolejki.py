from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import Counter

searchURL = "https://www.tauronliga.pl/games/tour/2021.html"
page = urlopen(searchURL)
soup = BeautifulSoup(page, "lxml")

h3 = []
date = []
for header2 in soup.findAll("h2"):
    for header3 in soup.findAll("h3"):
        #h3.append(header2.text)
        if "Mecz o" in header2.text:
            tempText = header2.text

            if "Kolejka" in header3.text or "Termin" in header3.text:
                h3.append(tempText + header3.text)

        if "Kolejka" in header3.text or "Termin" in header3.text:
            h3.append(header3.text)
        # for counter in soup.findAll("div"):
        #     date.append(counter)

pagecontent = soup.select(".filtr-zawartosc")
dataSpotkania = []

for i in range(len(pagecontent)):
    text = pagecontent[i].find_all('div', class_ = "date khanded")
    if i == 0 or i == 16:
        dataSpotkania.append(text)

dataSpotkania2 = soup.select('.date')[-1].text

print(h3)
print(date)
