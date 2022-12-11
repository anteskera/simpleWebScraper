import re
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2

host = 'localhost'
db_db = 'ci_task'
db_user = 'postgres'
db_password = '123'


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


def get_age(data):
    try:
        return data.find(class_="noprint ForceAgeToShow").get_text().split('(age\xa0')[1][:-1]
    except AttributeError:
        return 0


def get_date_of_birth(data):
    return remove_bracelets_from_string(data.find(class_="bday").get_text())


def remove_bracelets_from_string(string):
    return re.sub("[\(\[].*?[\)\]]", "", string).upper().strip()


def get_place_and_country_of_birth(data):
    data_find = data.find(class_="infobox-data birthplace")
    split = data_find.get_text().split(', ') if data_find else []
    if len(split) == 0:
        return "", ""
    elif len(split) < 2:
        return "", split[0]
    return remove_bracelets_from_string(split[0]), remove_bracelets_from_string(split[1])


def get_positions_from_data(data):
    comma_split = data.find(class_="infobox-data role").get_text().split(',')
    slash_split = data.find(class_="infobox-data role").get_text().split('/')
    position_split = slash_split if len(slash_split) >= len(comma_split) else comma_split
    result = position_split[0].strip()
    for pos in position_split[1:]:
        result = result + ', ' + pos.strip()
    return remove_bracelets_from_string(result)


def get_national_team_and_apps(data):
    try:
        return remove_bracelets_from_string(data.findAll(class_="infobox-data infobox-data-a")[-1].get_text()), \
               int(remove_bracelets_from_string(data.findAll(class_="infobox-data infobox-data-b")[-1].get_text()))
    except ValueError:
        return "", 0


def get_appearances_and_goals(data, club):
    try:
        As = data.findAll(class_="infobox-data infobox-data-a")
        Bs = data.findAll(class_="infobox-data infobox-data-b")
        Cs = data.findAll(class_="infobox-data infobox-data-c")

        index = None
        for i in range(len(As)):
            if remove_bracelets_from_string(As[i].get_text()) == club.strip():
                index = int(i)

        return int(Bs[index].get_text()), int(Cs[index].get_text()[2:-1])
    except (TypeError, TypeError, ValueError):
        return 0, 0


url_file = open(sys.argv[1], 'r')
unable_to_scrape = []
unable_to_open = []
tup = []
for player_url in url_file.readlines():
    page = urlopen(player_url)
    if page.status < 400:
        try:
            content = page.read().decode("utf-8")
            soup = BeautifulSoup(content, 'html.parser')
            age = get_age(soup)
            name = remove_bracelets_from_string(soup.find(class_="infobox-title fn").get_text())
            find_name = soup.find(class_="infobox-data nickname")
            full_name = remove_bracelets_from_string(find_name.get_text() if find_name
                                                     else soup.find(class_="infobox-title fn").get_text())
            date_of_birth = get_date_of_birth(soup)
            place_of_birth, country_of_birth = get_place_and_country_of_birth(soup)
            positions = get_positions_from_data(soup)
            find_club = soup.find(class_="infobox-data org")
            current_club = remove_bracelets_from_string(find_club.get_text() if find_club else "")
            national_team, national_team_appearances = get_national_team_and_apps(soup)
            appearances, goals = get_appearances_and_goals(soup, current_club)
            scraping_time = datetime.now()

            player = (age, name.strip(), full_name.strip(),
                      date_of_birth, place_of_birth.strip(),
                      positions, current_club.strip(),
                      national_team.strip(), appearances, scraping_time,
                      country_of_birth.strip(), player_url, national_team_appearances, goals)

            tup.append(player)
        except (AttributeError, IndexError, ValueError) as e:
            unable_to_scrape.append(player_url)
    else:
        unable_to_open.append(player_url)

conn = get_conn()
cur = conn.cursor()


cur.executemany("INSERT INTO player (age,name, full_name, date_of_birth, city_of_birth, positions, "
                "current_club, national_team, current_appearances, scraping_timestamp, country_of_birth, url, "
                "national_team_apps, current_goals) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (url) DO UPDATE SET "
                "(age, name, full_name, date_of_birth, city_of_birth, positions, current_club, "
                "national_team, current_appearances, scraping_timestamp, country_of_birth, national_team_apps, "
                "current_goals, last_modified) = "
                "(EXCLUDED.age, EXCLUDED.name, EXCLUDED.full_name, EXCLUDED.date_of_birth, EXCLUDED.city_of_birth, "
                "EXCLUDED.positions, EXCLUDED.current_club, EXCLUDED.national_team, EXCLUDED.current_appearances, "
                "EXCLUDED.scraping_timestamp, EXCLUDED.country_of_birth, EXCLUDED.national_team_apps, "
                "EXCLUDED.current_goals, EXCLUDED.last_modified)", tup)
conn.commit()
cur.close()
conn.close()

print(unable_to_scrape)
print(unable_to_open)
