SELECT current_club, AVG(current_appearances) as average_appearances, AVG(age) as average_age
FROM player 
WHERE current_club <> ''
GROUP BY current_club;
