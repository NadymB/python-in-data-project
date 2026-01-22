from etl.extract_data import main as extract_main
from etl.transform_data import main as transform_main
from etl.load_data import main as load_main

def run_pipeline():
    """ 
        The ETL pipeline main function
    """
    # 1. Extract data
    extract_main()
    # 2. Transform data
    transform_main()
    # 3. Load data
    load_main()

if __name__ == "__main__":  
    run_pipeline()
