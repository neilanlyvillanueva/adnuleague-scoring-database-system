-- 1. Sport Table
CREATE TABLE sport (
    sport_id SERIAL PRIMARY KEY,
    sport_name VARCHAR(100) NOT NULL,
    sport_category VARCHAR(50) DEFAULT 'Sports',
    scoring_type VARCHAR(50) NOT NULL,
    matchup_type VARCHAR(10) NOT NULL,  -- '1v1' or 'FFA'
    is_lower_better BOOLEAN DEFAULT FALSE,
    total_sets_required INTEGER DEFAULT 1
);

-- SCORING TYPE LIST
-- A. TIMED INCREMENTAL (1v1) - Highest final score wins within X time (e.g. Basketball, Football, Futsal)
-- B. RANKED INCREMENTAL (1v1) - Highest score wins, no time limit (Scrabble, Billiards, Softball, Dodgeball)
-- C. RANKED INCREMENTAL (FFA) - Highest score (Meters/Points), no time limit (Sipa, Darts, Discus, Javelin, Long Jump, Shotput)
-- D. THRESHOLD INCREMENTAL (1v1) - Most set wins, counted by final scores per set (Volleyball, Table Tennis, Badminton, Lawn Tennis)
-- E. RANKED TIMED (FFA) - Ranked by lowest TIME (Chinese Garter, Sack Race, Limbo, All Running, All Swimming)
-- F. CRITERIA BASED (FFA) - Highest sum of scores from set criteria. MUST NOT EXCEED 100! (Gimmick Parade, Cheer, Dance, Elocution, Vocal, Arnis, Battle of the Bands)
-- G. JUDGE BASED (FFA) - Highest sum of scores from judges, similar to criteria based (Gimmick Parade, Cheer, Dance, Elocution, Vocal, Arnis, Bands)
-- H. WIN/LOSE (FFA) - Win or Lose (1 or 0). (Sungka, Tug of War, Connect 4, Generals, ESports.)

-- 2. Criteria/Judge Table
CREATE TABLE sport_criteria (
    criteria_id SERIAL PRIMARY KEY,
    sport_id INTEGER REFERENCES sport(sport_id) ON DELETE CASCADE,
    criteria_name VARCHAR(100),
    max_points INTEGER 
);

-- 3. Team Table (Identity Only)
CREATE TABLE team (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) UNIQUE NOT NULL,
    team_color VARCHAR(20) DEFAULT '#0038A8' NOT NULL
);

-- 4. Participation Table (MANY-TO-MANY)
-- This allows Team A to participate in Sport 1 AND Sport 2
CREATE TABLE team_participation (
    participation_id SERIAL PRIMARY KEY,
    team_id INTEGER REFERENCES team(team_id) ON DELETE CASCADE,
    sport_id INTEGER REFERENCES sport(sport_id) ON DELETE CASCADE,
    UNIQUE(team_id, sport_id) 
);

-- 5. User Table (For Authorization)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'scorer' -- 'admin' or 'scorer'
);

-- 6. Game Table
CREATE TABLE game (
    game_id SERIAL PRIMARY KEY,
    sport_id INTEGER REFERENCES sport(sport_id),
    venue VARCHAR(100),
    school_year VARCHAR(15) NOT NULL,
    season VARCHAR(20) NOT NULL,
    game_status VARCHAR(20) DEFAULT 'Upcoming' -- Upcoming, Ongoing, Completed
);

-- 7. Game Result
CREATE TABLE game_result (
    result_id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES game(game_id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES team(team_id),
    final_score NUMERIC(10, 3), 
    is_winner BOOLEAN DEFAULT FALSE
);

-- 8. Score Breakdown
CREATE TABLE score_breakdown (
    breakdown_id SERIAL PRIMARY KEY,
    result_id INTEGER REFERENCES game_result(result_id) ON DELETE CASCADE,
    component_name VARCHAR(100), 
    points_awarded NUMERIC(10, 2)
);

--- VIEWS ---

-- REFINED LEADERBOARD: Using a Point System (10 per win, 2 per game played)
CREATE OR REPLACE VIEW overall_leaderboard AS
SELECT 
    t.team_name, 
    COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) as total_wins,
    COUNT(gr.result_id) as games_played,
    (COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) * 10) + (COUNT(gr.result_id) * 2) as overall_points
FROM team t
LEFT JOIN game_result gr ON t.team_id = gr.team_id
GROUP BY t.team_id, t.team_name
ORDER BY overall_points DESC;

-- MATCH HISTORY VIEW
CREATE OR REPLACE VIEW match_history_view AS
SELECT 
    s.sport_name, 
    g.game_id, 
    g.game_status,
    string_agg(t.team_name || ' (' || COALESCE(gr.final_score, 0) || ')', ' vs ') as matchup
FROM game g
JOIN sport s ON g.sport_id = s.sport_id
JOIN game_result gr ON g.game_id = gr.game_id
JOIN team t ON gr.team_id = t.team_id
GROUP BY s.sport_name, g.game_id, g.game_status
ORDER BY g.game_id DESC;
