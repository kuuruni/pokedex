from fastapi import FastAPI
import psycopg
import psycopg.rows
import os

db_host = os.getenv('POSTGRES_HOST') or "localhost"
db_port = os.getenv('POSTGRES_PORT') or 5432
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

conn_info = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
conn = psycopg.connect(conn_info)

app = FastAPI()

@app.get("/")
def read_root():
    return "Hi Pokemon 🐈"

@app.get("/pokemon")
def get_pokemon(offset: int = 0, limit: int = 10):
    cur = conn.cursor(row_factory=psycopg.rows.dict_row)
    cur.execute(f"SELECT * FROM pokemon LIMIT {limit} OFFSET {offset}")
    data = cur.fetchall()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pokemon")
    total = cur.fetchone()[0]
    return {"total": total, "data": data}
    
@app.get("/pokemon/{pokemon_id}")
def get_pokemon_by_id(pokemon_id:int):
    cur = conn.cursor(row_factory=psycopg.rows.dict_row)
    cur.execute(f"SELECT * FROM pokemon WHERE id = {pokemon_id} LIMIT 1")
    data = cur.fetchone()
    return data