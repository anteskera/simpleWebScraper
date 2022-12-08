import psycopg2
from uuid import UUID
from datetime import datetime

host = 'localhost'
db_db = 'ci_task'
db_user = 'postgres'
db_password = '123'


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
# datume u format YYYY-MM-DD uuid provjerit s is_valid_uuid


for line in csv_file.readlines()[1:]:
    split = line.split(';')

    try:

        date = datetime.strptime(formatted_date(split[2]), '%Y-%m-%d')
        date = date.strftime("%Y-%m-%d")
        age = int(split[3])

        tup.append((split[0], split[1], date, age, split[4],
                    split[5], split[6], split[7], split[8], split[11], split[12]))

    except (ValueError, IndexError) as e:
        print(e)
        print(line)
        continue

conn = get_conn()
cur = conn.cursor()

cur.executemany("INSERT INTO player (name, full_name, date_of_birth, age, city_of_birth, "
                "country_of_birth, positions, current_club, national_team, id, url)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", tup)
conn.commit()
cur.close()
conn.close()