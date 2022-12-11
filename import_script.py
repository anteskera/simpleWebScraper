import psycopg2
from uuid import UUID
from datetime import datetime

host = 'localhost'
db_db = 'ci_task'
db_user = 'postgres'
db_password = '123'


def get_positions_from_data(data):
    comma_split = data.split(',')
    slash_split = data.split('/')

    position_split = slash_split if len(slash_split) >= len(comma_split) else comma_split
    result = position_split[0].strip()
    for pos in position_split[1:]:
        result = result + ', ' + pos.strip()
    return result


def formatted_date(unformatted):
    split_date = unformatted.split('.')
    day = split_date[0]
    month = split_date[1]
    year = split_date[2]
    if len(day) < 2:
        day = '0' + day
    if len(month) < 2:
        month = '0' + month

    return year + '-' + month + '-' + day


def get_conn():
    return psycopg2.connect(host=host,
                            database=db_db,
                            user=db_user,
                            password=db_password)


csv_file = open('playersData.csv', 'r')
tup = []


# Name;Full name;Date of birth;Age;City of birth;Country of birth;Position;Current club;National_team;Dead;No
# data;PlayerID;URL


for line in csv_file.readlines()[1:]:
    split = line.split(';')

    try:

        date = datetime.strptime(formatted_date(split[2]), '%Y-%m-%d')
        date = date.strftime("%Y-%m-%d")
        age = int(split[3])
        positions = get_positions_from_data(split[6])

        tup.append((split[0], split[1], date, age, split[4].upper(), split[5].upper(), positions.upper(),
                    split[7].upper(), split[8].upper(), split[11], split[12].upper()))

    except (ValueError, IndexError) as e:
        print(e)
        print(line)
        continue

conn = get_conn()
cur = conn.cursor()

cur.executemany("INSERT INTO player (name, full_name, date_of_birth, age, city_of_birth, "
                "country_of_birth, positions, current_club, national_team, id, url)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                "ON CONFLICT (url) DO UPDATE SET "
                "(name, full_name, date_of_birth, age, city_of_birth, positions, country_of_birth, current_club, "
                "national_team, id, url) = "
                "(EXCLUDED.name, EXCLUDED.full_name, EXCLUDED.date_of_birth, EXCLUDED.age, "
                "EXCLUDED.city_of_birth, EXCLUDED.positions, EXCLUDED.country_of_birth, EXCLUDED.current_club, "
                "EXCLUDED.national_team, EXCLUDED.id, EXCLUDED.url)", tup)
conn.commit()
cur.close()
conn.close()
