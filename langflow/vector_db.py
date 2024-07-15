import os
from dotenv import load_dotenv

load_dotenv()
clientId = os.getenv('clientId')
secret = os.getenv('secret')
ASTRA_DB_APPLICATION_TOKEN = os.getenv('token')
ASTRA_DB_API_ENDPOINT = os.getenv('vdb_endpoint')

import os
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.ids import UUID
from astrapy.exceptions import InsertManyException
from astrapy.info import CollectionVectorServiceOptions

# Initialize the client and get a "Database" object
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

print(f"* Database: {database.info().name}\n")

def create_collection(collection_name):
    collection = database.create_collection(
    collection_name,
    metric=VectorMetric.DOT_PRODUCT,
    service=CollectionVectorServiceOptions(
        provider="openai",
        model_name="text-embedding-3-small",
        authentication={
            "providerKey": "key1",
        },
    ),
    )
    return collection

def check_collections():
    collections = database.list_collection_names()
    print(collections)
    return collections

def insert_text(collection, text):
    return database[collection].insert_one(text)

def vector_search(collection,query):
    lst =[]
    # Perform a similarity search
    results = database[collection].find(
        sort={"$vectorize": query},
        limit=1,
        projection={"$vectorize": True},
        include_similarity=True,
    )
    # print('results = ',results, len(results))
    # print(type(results))
    print(results)
    for document in results:
        print(document)
        if '$vectorize' in document:
            vectorize_value = document
            print(vectorize_value['$vectorize'])
            return vectorize_value
            # break
    return None


if __name__ == '__main__':
    
    documents = [
        {
            "_id": UUID("018e65c9-df45-7913-89f8-175f28bd7f74"),
            "$vectorize": "Chat bot integrated sneakers that talk to you",
        },
        {
            "_id": UUID("018e65c9-e1b7-7048-a593-db452be1e4c2"),
            "$vectorize": "An AI quilt to help you sleep forever",
        },
        {
            "_id": UUID("018e65c9-e33d-749b-9386-e848739582f0"),
            "$vectorize": "A deep learning display that controls your mood",
        },
    ]
    # insertion_result = database['test3245'].insert_many(documents)
    check_collections()
    query = "I'd like some talking shoes"
    collection = 'test3245'
    results = vector_search(collection,query)
    # for document in results:
    #     print("    ", document)
    create_collection('sohan')
    # collections = check_collections()
    # print(insert_text('test3245',{'$vectorize' :'Chat bot integrated shoes that talk to you/n image_id = 12342342342341234'}))