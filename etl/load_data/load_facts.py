from src.db.config import load_config
from src.db.connect import connect
from src.load.db.insert_data import load_fact_tables

def main():
    with connect(load_config()) as conn:
        load_fact_tables(conn)

if __name__ == "__main__":
    main()