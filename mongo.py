from pymongo import MongoClient
import os

MONGODB_URI=os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = os.environ.get('DB_NAME', 'sobeedb')

def connect_to_mongo():
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    return db

def fetch_transactions():
    db = connect_to_mongo()
    orders = db['orders'].find()

    transactions = []
    for order in orders:
        transaction = [str(item['product']) for item in order['orderItems']]
        transactions.append(transaction)
    
    return transactions
