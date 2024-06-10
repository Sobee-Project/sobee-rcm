from pymongo import MongoClient
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from mongo import fetch_transactions,connect_to_mongo
from bson import ObjectId

def generate_rules(transactions, min_support, min_confidence):
    # Convert the transactions into a format suitable for the apriori algorithm
        # Convert the transactions into a format suitable for the apriori algorithm
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apply the Apriori algorithm
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)

    # Generate the association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules

def recommend_products(input_products, rules, num_recommendations=5):
    recommendations = []
    
    for product in input_products:
        # Filter rules where the input product is in the antecedents
        relevant_rules = rules[rules['antecedents'].apply(lambda x: product in x)]
        
        # Sort rules by confidence and lift
        relevant_rules = relevant_rules.sort_values(by=['confidence', 'lift'], ascending=False)
        
        # Extract recommended products from consequents
        for _, rule in relevant_rules.iterrows():
            for consequent in rule['consequents']:
                if consequent not in input_products and consequent not in recommendations:
                    recommendations.append(consequent)
                    if len(recommendations) >= num_recommendations:
                        return recommendations
    
    return recommendations

def recommend_products_script(input_product: str, num_recommendations=10):
    transactions = fetch_transactions()

    min_support = 0.0001    
    

    rules = generate_rules(transactions, min_support=min_support, min_confidence=0.4)

    # Filter rules by desired metrics
    filtered_rules = rules[(rules['confidence'] > 0.4) & (rules['lift'] > 1.2)]

    db = connect_to_mongo()

    product = db['products'].find_one({"_id": ObjectId(input_product)})

    if product is None:
        return []
    related_products = db['products'].find({"category": product['category']}).limit(10)

  # replace with actual product IDs
    recommendations = recommend_products([related_products, input_product], filtered_rules, num_recommendations)
    return recommendations
    
