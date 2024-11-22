import pandas as pd
from pymongo import MongoClient

# df = pd.read_csv('Book2.csv') <-- NEW CSV FILE TO BE INGESTED INTO DATABASE
df = pd.read_csv('MOCK_DATA - 2024_11_22.csv')

# connect to mongodb server
client = MongoClient('mongodb://localhost:27017')

# database created
db = client['business_produce']

# collection created
collection = db['produce_details']

# convert dataframe to list of dictionaries
data = df.to_dict(orient='records')

# insert data into mongodb
collection.insert_many(data)

print(data)