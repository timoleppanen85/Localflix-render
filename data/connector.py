from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import os

mongo_url = os.getenv("MONGODB_URL")
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")


url = f"""mongodb+srv://{username}:{password}@{
    mongo_url}/localflix?retryWrites=true&w=majority&appName=MyCluster0"""


# Create a new client and connect to the server
client = MongoClient(url, server_api=ServerApi("1"))
database = client.localflix
collection = database.flix
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def create_new_flix(data):
    try:
        document = {
            "Title": data["Title"],
            "Genre": data["Genre"],
            "Filename": data["Filename"],
            "Cover": data["Cover"],
            "isMovie": data["isMovie"],
            "Season": data["Season"],
            "Episode": data["Episode"],
        }
        print(document)
        collection.insert_one(document)
        return "Success"
    except:
        print("Failed to create new flix")
    return None


def get_all_flix():
    try:
        flix = collection.find()
        return flix
    except:
        print("Failed to get all flix")
    return None


def get_one_flix(id):
    try:
        flix = collection.find_one({"_id": ObjectId(id)})
        return flix
    except:
        print("Failed to get single flix")
        return 404
    return None


def replace_flix(req, id):
    try:
        update = {"title": req["title"], "genre": req["genre"]}
        collection.replace_one({"_id": ObjectId(id)}, update)
        return "Success"
    except:
        print("Failed to update flix")
        return None
    return None


def delete_flix(id):
    try:
        collection.delete_one({"_id": ObjectId(id)})
        return "Success"
    except:
        print("Failed to delete flix")
        return None
    return None
