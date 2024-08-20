from pymongo import MongoClient


# MONGO_USERNAME = "jpsi-0895"
# MONGO_PASSWORD = "Hll@@3466"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "me_video"

client = MongoClient(
    f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
db = client[MONGO_DB]

    # f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
