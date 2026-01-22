import os 
from dotenv import load_dotenv

REQUIRED_ENV = [
    "DB_HOST",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
]

def load_config():
    load_dotenv()
    print("db host", os.getenv("DB_HOST"))
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing env vars: {missing}")
    
    return {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    

if __name__ == '__main__':
    config = load_config()
    print(config)