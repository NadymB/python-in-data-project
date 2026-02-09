from etl.extract_data.extract_dimensions import main as extract_dimensions
from etl.transform_data.transform_dimensions import main as transform_dimensions
from etl.load_data.load_dimensions import main as load_dimensions
from etl.extract_data.extract_facts import main as extract_facts
from etl.transform_data.transform_facts import main as transform_facts
from etl.load_data.load_facts import main as load_facts

def run_pipeline():
    """ 
        The ETL pipeline main function
    """
    # 1. Extract data for dimension tables
    extract_dimensions()
    # 2. Transform data for dimension tables
    transform_dimensions()
    # 3. Load data for dimension tables
    load_dimensions()

    # 4. Extract data for fact tables
    extract_facts()
    # 5. Transform data for fact tables
    transform_facts()
    #6. Load data for fact tables
    load_facts()

if __name__ == "__main__":  
    run_pipeline()
