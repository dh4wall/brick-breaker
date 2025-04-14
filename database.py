import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def get_high_scores():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, highscore FROM users ORDER BY highscore DESC LIMIT 5")
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{'name': score[0], 'score': score[1]} for score in scores]

def update_high_score(user_id, score):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET highscore = GREATEST(highscore, %s) WHERE id = %s",
        (score, user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()