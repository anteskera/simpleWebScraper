# SIMPLE WEB SCRAPER

To run import_script.py you need to set the host, db_db, db_user and db_password to match your database credentials.
The script will automatically look at the playersData.csv file and upsert the useful data.


To run the simple_scraper.py you need to provide the file with player URLs as a command line argument
Example: simple_scraper.py playerURLs.csv
Simple scraper opens the file with URLs goes through each URL and tries to fetch the data from each URL, if data is successfully fetched it is then parsed and upserted into the database.




