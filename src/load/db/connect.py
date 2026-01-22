import psycopg2
from src.load.db.config import load_config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print("Connection to the database was successful.")
            return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    config = load_config()
    connect(config)