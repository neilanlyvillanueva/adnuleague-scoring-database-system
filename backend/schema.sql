-- ============================================================
-- ADNU League Intramurals Scoring Database System
-- PostgreSQL Schema — field names matched to frontend useStore
-- Run in pgAdmin or: psql -U postgres -d adnu_intramurals -f schema.sql
-- ============================================================

-- 1. Sport Table  (= "event" in the frontend)
CREATE TABLE IF NOT EXISTS sport (
    sport_id            SERIAL PRIMARY KEY,
    sport_name          VARCHAR(100) NOT NULL,
    sport_category      VARCHAR(50)  DEFAULT 'Sports',
    scoring_system_id   INTEGER      NOT NULL,   -- matches frontend scoringSystemId (1–8)
    matchup_type        VARCHAR(20)  NOT NULL,   -- '1v1' or 'free-for-all'
    is_lower_better     BOOLEAN      DEFAULT FALSE,
    total_sets_required INTEGER      DEFAULT 1
);

-- SCORING SYSTEM ID TABLE (frontend reference — no DB table needed)
-- 1 = Timed Incremental (1v1)
-- 2 = Ranked Incremental (1v1)
-- 3 = Ranked Incremental (FFA)
-- 4 = Threshold Incremental (1v1)  — uses sets
-- 5 = Ranked Timed (FFA)           — lowest time wins
-- 6 = Criteria Based (FFA)         — uses criteria, max 100 pts
-- 7 = Judge Based (FFA)            — uses criteria
-- 8 = Win/Lose (FFA)               — binary

-- 2. Criteria / Judge Table
CREATE TABLE IF NOT EXISTS sport_criteria (
    criteria_id   SERIAL PRIMARY KEY,
    sport_id      INTEGER REFERENCES sport(sport_id) ON DELETE CASCADE,
    criteria_name VARCHAR(100),
    max_points    INTEGER
);

-- 3. Team Table
CREATE TABLE IF NOT EXISTS team (
    team_id    SERIAL PRIMARY KEY,
    team_name  VARCHAR(100) UNIQUE NOT NULL,
    team_color VARCHAR(20)  DEFAULT '#0038A8'
);

-- 4. Participation Table (MANY-TO-MANY)
CREATE TABLE IF NOT EXISTS team_participation (
    participation_id SERIAL PRIMARY KEY,
    team_id  INTEGER REFERENCES team(team_id)   ON DELETE CASCADE,
    sport_id INTEGER REFERENCES sport(sport_id) ON DELETE CASCADE,
    UNIQUE(team_id, sport_id)
);

-- 5. User Table (For Authorization)
CREATE TABLE IF NOT EXISTS users (
    user_id       SERIAL PRIMARY KEY,
    username      VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    role          VARCHAR(20) DEFAULT 'scorer'   -- 'admin' or 'scorer'
);

-- 6. Game Table  (= "match" in the frontend)
--    matchup_type is inherited from the sport but stored here for easy querying
CREATE TABLE IF NOT EXISTS game (
    game_id     SERIAL PRIMARY KEY,
    sport_id    INTEGER REFERENCES sport(sport_id),
    venue       VARCHAR(100),
    school_year VARCHAR(15)  NOT NULL DEFAULT '2024-2025',
    season      VARCHAR(20)  NOT NULL DEFAULT 'Intramurals',
    game_status VARCHAR(20)  DEFAULT 'ongoing'   -- 'ongoing' | 'completed'
);

-- 7. Game Result  (one row per participant/team)
--    1v1: two rows — first = teamA, second = teamB
--    FFA: N rows — one per participant
CREATE TABLE IF NOT EXISTS game_result (
    result_id   SERIAL PRIMARY KEY,
    game_id     INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    team_id     INTEGER REFERENCES team(team_id),
    final_score NUMERIC(10, 3),
    is_winner   BOOLEAN DEFAULT FALSE
);

-- 8. Score Breakdown  (set scores or criteria scores per result row)
--    For set-based (scoringSystemId=4): component_name = 'set_1', 'set_2', ...
--    For criteria-based (6,7): component_name = criteria name
CREATE TABLE IF NOT EXISTS score_breakdown (
    breakdown_id   SERIAL PRIMARY KEY,
    result_id      INTEGER REFERENCES game_result(result_id) ON DELETE CASCADE,
    component_name VARCHAR(100),
    points_awarded NUMERIC(10, 2)
);

-- ============================================================
-- VIEWS
-- ============================================================

-- OVERALL LEADERBOARD
CREATE OR REPLACE VIEW overall_leaderboard AS
SELECT
    t.team_id,
    t.team_name,
    t.team_color,
    COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) AS total_wins,
    COUNT(gr.result_id)                                     AS games_played,
    (COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) * 10)
        + (COUNT(gr.result_id) * 2)                        AS overall_points
FROM team t
LEFT JOIN game_result gr ON t.team_id = gr.team_id
GROUP BY t.team_id, t.team_name, t.team_color
ORDER BY overall_points DESC;

-- MATCH HISTORY VIEW
CREATE OR REPLACE VIEW match_history_view AS
SELECT
    g.game_id,
    s.sport_id,
    s.sport_name,
    s.sport_category,
    s.matchup_type,
    g.venue,
    g.game_status,
    g.school_year,
    g.season,
    json_agg(
        json_build_object(
            'teamId',     t.team_id,
            'teamName',   t.team_name,
            'teamColor',  t.team_color,
            'finalScore', COALESCE(gr.final_score, 0),
            'isWinner',   gr.is_winner
        )
        ORDER BY gr.is_winner DESC, gr.result_id
    ) AS participants
FROM game g
JOIN sport s  ON g.sport_id  = s.sport_id
JOIN game_result gr ON g.game_id = gr.game_id
JOIN team t   ON gr.team_id  = t.team_id
GROUP BY g.game_id, s.sport_id, s.sport_name, s.sport_category,
         s.matchup_type, g.venue, g.game_status, g.school_year, g.season
ORDER BY g.game_id DESC;
