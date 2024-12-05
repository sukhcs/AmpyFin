from pymongo import MongoClient
import math
from datetime import datetime
from config import MONGO_DB_STRING
from helper_files.client_helper import strategies

# MongoDB connection string
mongo_url = MONGO_DB_STRING

def insert_rank_to_coefficient(max_rank):
    """
    Inserts rank and corresponding coefficient into the MongoDB collection.
    
    Args:
        max_rank (int): The maximum rank to insert.
    """
    client = MongoClient(mongo_url)  
    db = client.trading_simulator 
    collection = db.rank_to_coefficient

    # Clear existing entries
    collection.delete_many({})
    
    e = math.e
    rate = (e**e) / (e**2) - 1
    for rank in range(1, max_rank + 1):
        coefficient = rate ** (2 * rank)
        collection.insert_one({
            "rank": rank, 
            "coefficient": coefficient
        })
    
    client.close()

def initialize_rank():
    """
    Initializes rank documents for each strategy in the MongoDB collection.
    """
    client = MongoClient(mongo_url)  
    db = client.trading_simulator  
    holdings_collection = db.algorithm_holdings  
    points_collection = db.points_tally  
    initialization_date = datetime.now()  

    for strategy in strategies:
        strategy_name = strategy.__name__
        
        # Initialize algorithm_holdings if not present
        if not holdings_collection.find_one({"strategy": strategy_name}):
            holdings_collection.insert_one({  
                "strategy": strategy_name,  
                "holdings": {},  
                "amount_cash": 50000,  
                "initialized_date": initialization_date,  
                "total_trades": 0,  
                "successful_trades": 0,
                "neutral_trades": 0,
                "failed_trades": 0,   
                "last_updated": initialization_date, 
                "portfolio_value": 50000 
            })  
        
        # Initialize points_tally
        if not points_collection.find_one({"strategy": strategy_name}):
            points_collection.insert_one({  
                "strategy": strategy_name,  
                "total_points": 0,  
                "initialized_date": initialization_date,  
                "last_updated": initialization_date  
            })  
    
    client.close()

def main():
    """
    Main function to execute the rank initialization and insertion.
    """
    # Define the maximum rank you want to insert
    MAX_RANK = 50
    
    # Initialize ranks for strategies
    initialize_rank()
    print("Initialization of ranks completed.")
    
    # Insert rank to coefficient mappings
    insert_rank_to_coefficient(MAX_RANK)
    print(f"Inserted rank to coefficient up to rank {MAX_RANK}.")

if __name__ == "__main__":
    main()
