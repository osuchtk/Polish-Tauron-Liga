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


