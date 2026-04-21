import os
import psycopg2
import fastapi
from prometheus_fastapi_instrumentator import Instrumentator


app = fastapi.FastAPI()
Instrumentator().instrument(app).expose(app)


DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_status():
    return {"status": "ok"}


@app.get("/auto-deploy")
def auto_deploy():
    return {"status": "ok"}


@app.get("/me")
def health_status():
    return {"user": "It's a me, Mario!"}

@app.get("/users")
def get_users():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES ('toto')")
    conn.commit()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"users": rows}