# test_mongo_connection.py

from config import MONGO_DB_STRING
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_connection():
    try:
        client = MongoClient(MONGO_DB_STRING)
        # Attempt to list databases to confirm connection
        databases = client.list_database_names()
        logging.info("MongoDB connection successful. Databases:")
        for db in databases:
            logging.info(f"- {db}")
    except Exception as e:
        logging.error(f"MongoDB connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    test_connection()
