-- Termination of Chess960 games
SELECT game_id, eval, White, termination
FROM game_data
WHERE Variant IS NOT NULL
	AND ply = 1;

-- Average plys per game
SELECT 
    AVG(max_ply) AS avg_plys,
    MIN(max_ply) AS shortest_game,
    MAX(max_ply) AS longest_game
FROM (
    SELECT game_id, MAX(ply) AS max_ply
    FROM game_data
    GROUP BY game_id
);