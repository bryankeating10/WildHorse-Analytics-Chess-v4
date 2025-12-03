-- Termination of Chess960 games
SELECT game_id, eval, White, termination
FROM game_data
WHERE Variant IS NOT NULL
	AND ply = 1;

