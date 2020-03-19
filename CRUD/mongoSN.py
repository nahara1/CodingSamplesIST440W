
# GET
# Reading records from ServiceNow and saving them into local mongo database
from pymongo import MongoClient
import pymongo


client = MongoClient('localhost', 27017)
db = client['recipes_db']
collection_recipe = db['recipes']
#GET request w/ database table fields specified

#Need to install requests package for python
#easy_install requests
import requests, json, ast, itertools

# Set the request parameters
'''
Use sysparm_fields=field_name => field_name is the field you want to read
separate fields using commas in case you want to read more than one field from a table
'''
url = 'https://emplkasperpsu2.service-now.com/api/now/table/x_snc_brewing440_recipe?sysparm_fields=recipe_name&displayvariables=true&sysparm_action=getKeys'

#Use IST440 for both user and pwd
user = 'IST440'
pwd = 'IST440'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
# GET is the request to read data
response = requests.get(url, auth=(user, pwd), headers=headers )


# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)

recipe_names_pairs = data['result']



#
# Check type
print("Type recipe_names_pairs: " , type(recipe_names_pairs))
print()
#db.collection_recipe.insert(recipe_names_pairs)

for doc in recipe_names_pairs:
    try:
        # insert into db collection
        # print("Inserting ",  doc, " into db...")
        message = "Inserting ",  doc, " into db..."
        db.collection_recipe.insert_one(doc)
    except pymongo.errors.DuplicateKeyError:
        # skip document because it already exists in the local db collection
        continue
