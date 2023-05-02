from dotenv import load_dotenv

load_dotenv()

import os
import psycopg2

conn = psycopg2.connect(os.environ["DATABASE_URL"])

def delete_all_tables():
  commands = (
    """
    DROP TABLE IF EXISTS career_stats CASCADE
    """,
    """
    DROP TABLE IF EXISTS game_stats CASCADE
    """,
    """
    DROP TABLE IF EXISTS predicted_stats CASCADE
    """
  )
  try:
    cur = conn.cursor()
    for command in commands:
      cur.execute(command)
    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)


def create_table():
  commands = (
    """
    CREATE TABLE IF NOT EXISTS career_stats (
      id SERIAL PRIMARY KEY,
      player_name VARCHAR(255) NOT NULL,
      jsondata VARCHAR(5000) NOT NULL,
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    """,
    """
    CREATE TABLE IF NOT EXISTS game_stats (
      id SERIAL PRIMARY KEY,
      player_name VARCHAR(255) NOT NULL,
      jsondata VARCHAR(5000) NOT NULL,
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    """,
    """
      CREATE TABLE IF NOT EXISTS predicted_stats (
      id SERIAL PRIMARY KEY,
      player_name VARCHAR(255) NOT NULL,
      jsondata VARCHAR(5000) NOT NULL,
      updated_at TIMESTAMP NOT NULL DEFAULT NOW()
      )
    """,
  )
  try:
    cur = conn.cursor()
    for command in commands:
      cur.execute(command)
    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
    
create_table()

conn.close()