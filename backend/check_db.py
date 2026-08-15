import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="vibrantic_ai",
    user="postgres",
    password="postgres",  # or "postgres" if that's the actual Docker password
)
cur = conn.cursor()

cur.execute("SELECT version(), current_database();")
print("DB:", cur.fetchone())

cur.execute("SELECT extname FROM pg_extension;")
print("Extensions:", cur.fetchall())

cur.execute("SELECT typname FROM pg_type WHERE typname = 'vector';")
print("Types:", cur.fetchall())

conn.close()