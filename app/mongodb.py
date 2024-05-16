import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

dbname = os.getenv('DB_NAME')
dbpass = os.getenv('DB_PASSWORD')
uri    = f"mongodb+srv://{dbname}:{dbpass}@cluster0.e9tjso8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class mongo_db:

    def getAll(self):
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        Database = client.get_database('judicialdata')
        # Table
        jud = Database.judicialdata

        query = jud.find()
        output = {}
        i = 0

        for x in query:
            output[i] = x
            output[i]['_id'] = str(output[i]['_id'])
            i += 1
        return output

    def getById(self, id, per):
        client = MongoClient(uri, server_api=ServerApi('1'))
        Database = client.get_database('judicialdata')
        # Table
        jud = Database.judicialdata

        query = jud.find({"idUser":id, "type": per})

        output = {}
        i = 0

        for x in query:
            output[i] = x
            output[i]['_id'] = str(output[i]['_id'])
            i += 1

        return output

    def postProcess(self, data):
        client = MongoClient(uri, server_api=ServerApi('1'))
        Database = client.get_database('judicialdata')
        jud = Database.judicialdata
        ju = jud.insert_one(data)
        new_proc = jud.find_one({"_id":ju.inserted_id})
        return (new_proc)