from src.load.db.config import load_config
from src.load.db.connect import connect
from src.load.db.insert_data import load_all_tables

def main():
    with connect(load_config()) as conn:
        load_all_tables(conn)
    
if __name__ == "__main__":
    main()