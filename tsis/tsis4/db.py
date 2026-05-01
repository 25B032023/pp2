import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def get_player_id(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO players(username)
        VALUES (%s)
        ON CONFLICT (username) DO NOTHING;
    """, (username,))

    cur.execute("""
        SELECT id FROM players
        WHERE username = %s;
    """, (username,))

    player_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return player_id


def save_game(username, score, level):
    player_id = get_player_id(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s);
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()


def get_best_score(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(gs.score)
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        WHERE p.username = %s;
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    if result is None:
        return 0

    return result


def get_leaderboard():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON gs.player_id = p.id
        ORDER BY gs.score DESC
        LIMIT 10;
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows