CREATE DATABASE ci_task;
\connect ci_task
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE player(
	id VARCHAR(255) PRIMARY KEY DEFAULT uuid_generate_v4(),
	name VARCHAR(255),
	full_name VARCHAR(255),
	url VARCHAR(255) UNIQUE,
	date_of_birth DATE,
	city_of_birth VARCHAR(255),
	country_of_birth VARCHAR(255),
	age INTEGER DEFAULT 0,
	positions VARCHAR(255),
	scraping_timestamp TIMESTAMP,
	current_goals INTEGER DEFAULT 0,
	current_appearances INTEGER DEFAULT 0,
	current_club VARCHAR(255),
	national_team VARCHAR(255),
	national_team_apps INTEGER DEFAULT 0,
	last_modified TIMESTAMP);


CREATE FUNCTION sync_lastmod() RETURNS trigger AS $$
BEGIN
  NEW.last_modified := NOW();

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER
  sync_lastmod
BEFORE UPDATE ON
  player
FOR EACH ROW EXECUTE PROCEDURE
  sync_lastmod();
