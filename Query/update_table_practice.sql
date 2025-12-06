-- Sample query
SELECT *
FROM stak1.main.game_data
WHERE ply % 20 = 0
AND game_id > 1
LIMIT 5;

-- Column for protagonist color
ALTER TABLE stak1.main.game_data
ADD COLUMN ProtColor INT;

-- Find protagonist color
UPDATE stak1.main.game_data
SET ProtColor = CASE
    WHEN White = 'stak1' THEN 1
    ELSE -1
END;

-- Column for ELO spread
ALTER TABLE stak1.main.game_data
ADD COLUMN EloSpread INT;

-- Populate ELO spread
UPDATE stak1.main.game_data
SET EloSpread = (WhiteElo - BlackElo) * ProtColor;

SELECT game_id, ply, White, WhiteElo, Black, BlackElo, ProtColor, EloDifference
FROM stak1.main.game_data
WHERE ply % 20 = 0
AND game_id > 1
LIMIT 30;

PRAGMA table_info('stak1.main.game_data');  -- SQLite/DuckDB

SELECT AVG(WhiteElo), AVG(BlackElo) FROM stak1.main.game_data;

-- Opening frequency
SELECT ECO, COUNT(*) AS frequency
FROM game_data GROUP BY ECO
ORDER BY frequency DESC;

-- Opeing frequency accounting for game redundancy


