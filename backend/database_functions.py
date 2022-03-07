import pymongo
import gridfs
import json

from pymongo import MongoClient

#client = MongoClient('mongodb://admin:iamyourfather@127.0.0.1:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
# client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttds-cluster.zsdaj.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient(host='localhost',port=27017)

db = client.songs   # The database on mongodb
sentences = db.sentences
# inverted_index_stop = db.inverted_index_with_stop
inverted_index = db.inverted_index

sentence_bson_list = list()
previous_id = -1

index_bson_list = list()

def get_max_sentences_id():
    return sentences.find_one({"_id": {"$exists": True}}, sort=[("_id", -1)])["_id"]

def get_sentences_cursors():
    return sentences.find({})
