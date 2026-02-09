import psycopg2

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print("Connection to the database was successful.")
            return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)