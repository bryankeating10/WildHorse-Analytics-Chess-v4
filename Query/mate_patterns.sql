SELECT *
FROM game_data;

-- Selecting all instances where there was mate on the board
SELECT *
FROM game_data
WHERE eval LIKE '%M%';

-- Grouping mate instances by game id
-- SELECT
--     game_id, move, clock, eval, TimeControl,
--     MIN(ply) AS first_mate_ply
-- FROM game_data
-- WHERE eval like '%M%'
-- GROUP BY game_id;

SELECT
    game_id,
    MIN(ply) as first_mate_ply
FROM game_data
WHERE eval like '%M%'
GROUP BY game_id;

-- Failed subquery attempt
-- SELECT
--     AVG(MIN(ply)) as avg_first_mate_ply
-- FROM game_data
-- WHERE eval like '%M%'
-- GROUP BY game_id;

-- Average ply where first mate instance is on the board
SELECT
    AVG(first_mate_ply) as avg_first_mate_ply
FROM(
    SELECT
        MIN(ply) as first_mate_ply
    FROM game_data
    WHERE eval LIKE '%M%'
    GROUP BY game_id
    );

-- Number of games with mate on the board
SELECT
    COUNT(DISTINCT game_id) as games_with_mate
FROM game_data
WHERE eval LIKE '%M%';

-- Total number of games
SELECT
    COUNT(DISTINCT game_id) as total_games
FROM game_data;

-- Percentage of games with mate, first attempt
-- SELECT
--     (with_mate / total_games) as perc_with_mate
-- FROM(
--
--     )

-- Percentage of games with mate on the board
SELECT
    (CAST(with_mate AS FLOAT)/ total_games)*100 AS perc_with_mate
FROM(
    SELECT
        COUNT(DISTINCT CASE WHEN eval LIKE '%M%' THEN game_id END) AS with_mate,
        COUNT(DISTINCT game_id) AS total_games
    FROM game_data
    )

-- Percentage of games ending in checkmate
SELECT
    COUNT(DISTINCT game_id) as mate_termination
FROM game_data
WHERE Termination = 0;
