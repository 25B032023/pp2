import psycopg2
from config import host, port, dbname, user, password


def connect():
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    return conn
