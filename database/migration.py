import psycopg
import os

db_host = os.getenv('POSTGRES_HOST') or "localhost"
db_port = os.getenv('POSTGRES_PORT') or 5432
db_user = os.getenv('POSTGRES_USER')
db_pass = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')

conn_info = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

def migrate():
    conn = psycopg.connect(conn_info)
    cursor = conn.cursor()
    print("Creating tables...")
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute(open("./database/migration.sql", "r").read())
    cursor.execute("COMMIT;")
    print("Tables created successfully!")
    cursor.close()
    conn.close()

if __name__ == '__main__':
    migrate()