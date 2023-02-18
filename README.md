# Polish-Tauron-Liga
Projekt inżynierski - Analiza i wizualizacja statystyk siatkarskich / Engineering project - analysis and visualization of volleyball statistics

My main goal was to download and visualize volleyball statistics. In order to do this I scraped data from Tauron Liga websites. I used data about players, team standings and typical match statictics. All informations is saved in csv files and then uploaded to my local  MariaDB database. In Power BI I connect to my database and prepare visualization.

##List of scripts

usefulFunctions - creating headers for csv files and folders
getLinkToMatches - gather links to all matches in season
getLinksToPlayers - gather list of players in season, their photos and profile link
getInfoAboutTeam - gather informations about  club, e.g. coach, management, etc.
getPlayerInfo - scraping informations about position, date of birth, etc using link to profile
getStatistics - scraping tables with match statistics
scrapStatistics - wrapper for getStatictisc, which contains info about new or old statictisc system 
combineStatistics - combine new and old statistics system so Power BI can handle it
getStandings - gather informations about clubs standings at the end of the season
mariabdController - read and upload files to database 
MAIN - wrapper for all functions


## Report
Report containts 3 main pages, but each is prepared in two colours. First page describes club, second informations and staticstics about plyers and third contains informations about specific match.

![Klub1](https://user-images.githubusercontent.com/56642926/219860225-15dcc646-f755-4612-962f-9d0daaf3cf51.png)
![Zawodniczka1](https://user-images.githubusercontent.com/56642926/219860410-f1b85d2f-fbfb-461e-ae8f-83b03ba3c1ac.png)
![Mecz1](https://user-images.githubusercontent.com/56642926/219860467-83ce4e4b-51d1-42a5-87b9-5ba9b2c2e2f6.png)
