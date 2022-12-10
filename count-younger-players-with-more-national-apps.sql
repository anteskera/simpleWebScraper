CREATE VIEW liverpool_data AS 
	SELECT UNNEST(STRING_TO_ARRAY(p.positions, ', ')) AS position, p.date_of_birth, p.national_team_apps 
	FROM player p 
	WHERE p.current_club = 'LIVERPOOL F.C.';
	
SELECT COUNT(DISTINCT ID) 
FROM player p
JOIN liverpool_data ld on p.positions = ld.position
WHERE p.date_of_birth < ld.date_of_birth AND p.national_team_apps > ld.national_team_apps;


