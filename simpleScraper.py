import requests
import selenium
import urllib3
from bs4 import BeautifulSoup
from time import time


def get_age(data):
    return data.find(class_="noprint ForceAgeToShow").get_text().split('(age\xa0')[1][:-1]


def get_date_of_birth(data):
    return data.find(class_="infobox-data").get_text().split('(age')[0]


def get_place_and_country_of_birth(data):
    split = data.find(class_="infobox-data birthplace").get_text().split(', ')
    return split[0], split[1]


def get_positions_from_data(data):
    return data.find(class_="infobox-data role").get_text().split(', ')


def get_national_team(data):
    return data.findAll(class_="infobox-data infobox-data-a")[-1].get_text()


def get_appearances_and_goals(data, club):
    As = data.findAll(class_="infobox-data infobox-data-a")
    Bs = data.findAll(class_="infobox-data infobox-data-b")
    Cs = data.findAll(class_="infobox-data infobox-data-c")

    index = None
    for i in range(len(As)):
        print(As[i].get_text())
        if As[i].get_text() == club:
            print(i)
            index = int(i)

    return int(Bs[index].get_text()), int(Cs[index].get_text()[2:-1])


#
# for url in url_file.readlines():
# headers = { "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,
# image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', "user-agent": 'Mozilla/5.0 (
# X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36' } page = requests.get(
# url, headers=headers) soup = BeautifulSoup(page.content, 'html.parser') if page.status_code < 400:

url_file = open('João Cancelo - Wikipedia.html', 'r')
page = url_file.read()
soup = BeautifulSoup(page, 'html.parser')
age = get_age(soup)
name = soup.find(class_="infobox-title fn").get_text()
full_name = soup.find(class_="infobox-data nickname").get_text()
date_of_birth = get_date_of_birth(soup)
place_of_birth, country_of_birth = get_place_and_country_of_birth(soup)
positions = get_positions_from_data(soup)
current_club = soup.find(class_="infobox-data org").get_text()
national_team = get_national_team(soup)
appearances, goals = get_appearances_and_goals(soup, current_club)
player_id = None
