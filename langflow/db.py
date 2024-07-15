from pymongo import MongoClient
import bcrypt
from PIL import Image
import io
import base64
from bson import ObjectId
from bson.objectid import ObjectId

# Connect to MongoDB
url = "mongodb+srv://sohanmahadev:Sohan%40123@cluster0.gachc3t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(url, tlsAllowInvalidCertificates=True)
db = client.ImageDB

# Function to retrieve image data from MongoDB
def get_image_from_mongodb(image_id): 
    collection = db['Images'] 

    # Retrieve the image document using its ID
    image_doc = collection.find_one({'_id': ObjectId(image_id)})
    if image_doc and 'image' in image_doc:
        image_data = image_doc['image']
        return image_data
    else:
        raise ValueError('Image not found in the database')

# Convert image data to a format suitable for genai.upload_file
def convert_image_data_to_file(image_data):
    with open('temp.png', 'wb') as f:
        f.write(image_data)
    return 'temp.png'

def check_user(username, password):
    try:
        user = db.Users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return user['_id']
        return None
    except Exception as e:
        print(f"Error checking user: {e}")
        return None
    
def empty_tags_id_extractor(user_id)->list:
    empty_tags_object_id = []
    user_id = ObjectId(user_id) if not isinstance(user_id, ObjectId) else user_id
    query = {"user_id": user_id, "tags": ""}
    documents = db.Images.find(query)
    
    for doc in documents:
        empty_tags_object_id.append(str(doc['_id']))
    
    return empty_tags_object_id


def update_tags_in_db(document_id, keywords):
    
    document_id = ObjectId(document_id) if not isinstance(document_id, ObjectId) else document_id
    
    result = db.Images.update_one(
        {"_id": document_id},
        {"$set": {"tags": keywords}}
    )
    
    return result.modified_count