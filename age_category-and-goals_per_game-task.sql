ALTER TABLE player
ADD COLUMN age_category VARCHAR(15), 
ADD COLUMN goals_per_club_game REAL;

UPDATE player SET age_category = CASE
				  	WHEN age <= 23 THEN 'Young'
				  	WHEN age > 32 THEN 'Old'
				  	ELSE 'MidAge'
				  END,
		   goals_per_club_game = CASE
		   				WHEN current_appearances = 0 THEN 0 
		   				ELSE current_goals::REAL/current_appearances::REAL
		   			  END;
		   

