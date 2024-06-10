from pymongo import MongoClient

DB_NAME = 'sobeedb'
URI='mongodb://localhost:27017/'

def connect_to_mongo():
    client = MongoClient(URI)
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
