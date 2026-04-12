"""
Initialize the Supabase database with views.
Tables should already exist - this script creates the views and seeds users.

Usage: python init_db.py
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_connection():
    """Create connection to Supabase PostgreSQL."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

def init_database():
    """Initialize database views and seed default users."""
    print("Connecting to Supabase database...")
    conn = get_connection()
    cur = conn.cursor()

    try:
        # Add team_color column if it doesn't exist
        print("Checking schema...")
        cur.execute("""
            ALTER TABLE team
            ADD COLUMN IF NOT EXISTS team_color VARCHAR(20) DEFAULT '#0038A8'
        """)
        conn.commit()
        print("  - Added team_color column to team table")

        # Drop views if they exist and recreate them
        print("Creating/recreating views...")

        # Drop existing views
        cur.execute("DROP VIEW IF EXISTS match_history_view CASCADE")
        cur.execute("DROP VIEW IF EXISTS overall_leaderboard CASCADE")
        conn.commit()

        # Create overall_leaderboard view
        cur.execute("""
        CREATE OR REPLACE VIEW overall_leaderboard AS
        SELECT
            t.team_name,
            COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) as total_wins,
            COUNT(gr.result_id) as games_played,
            (COUNT(gr.result_id) FILTER (WHERE gr.is_winner = TRUE) * 10) + (COUNT(gr.result_id) * 2) as overall_points
        FROM team t
        LEFT JOIN game_result gr ON t.team_id = gr.team_id
        GROUP BY t.team_id, t.team_name
        ORDER BY overall_points DESC
        """)
        print("  - Created overall_leaderboard view")

        # Create match_history_view
        cur.execute("""
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
        ORDER BY g.game_id DESC
        """)
        print("  - Created match_history_view view")

        conn.commit()
        print("Views created successfully!")

        # Seed default users
        print("Checking default users...")

        cur.execute("SELECT username FROM users WHERE username IN ('admin', 'tabulation')")
        existing = [row[0] for row in cur.fetchall()]

        # Import password hashing
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from werkzeug.security import generate_password_hash

        if 'admin' not in existing:
            admin_hash = generate_password_hash('admin123')
            cur.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
            """, ('admin', admin_hash, 'admin'))
            print("  - Created admin user (password: admin123)")
        else:
            print("  - Admin user already exists")

        if 'tabulation' not in existing:
            tabulation_hash = generate_password_hash('tabulation123')
            cur.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
            """, ('tabulation', tabulation_hash, 'scorer'))
            print("  - Created tabulation user (password: tabulation123)")
        else:
            print("  - Tabulation user already exists")

        conn.commit()
        print("\nDatabase initialization complete!")
        print("\nDefault credentials:")
        print("  - admin / admin123 (role: admin)")
        print("  - tabulation / tabulation123 (role: scorer)")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    init_database()
