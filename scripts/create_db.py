import psycopg2

from trade import db

conn = psycopg2.connect(
  database="postgres", user="postgres", password="jmUQinWi2eA9LzhW", host="database-1.cb7zx4b6eekp.us-east-1.rds.amazonaws.com", port="5432"
)
conn.autocommit = True

cursor = conn.cursor()

sql = """CREATE DATABASE minancedb"""

cursor.execute(sql)

print("Database successfully created.")

conn.close()

db.create_all()