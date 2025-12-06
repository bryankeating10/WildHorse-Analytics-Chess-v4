-- Number of moves per game and save it to the database
CREATE SCHEMA IF NOT EXISTS stak1.queries;

CREATE TABLE stak1.queries.top50_longest_games AS
SELECT game_id, max(ply) AS max_ply
FROM game_data
GROUP BY game_id
ORDER BY max_ply DESC
LIMIT 50;

SELECT *
FROM queries.top50_longest_games;