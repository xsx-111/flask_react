import os
import sys
sys.path.append("..")
import logging
import preprocessing
import database_functions
import argparse
import pickle
from pymongo import MongoClient
import dns

logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

client = MongoClient(host='localhost',port=27017)
# client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttds-cluster.zsdaj.mongodb.net/?retryWrites=true&w=majority")
inverted_index = client.songs.inverted_index

class IndexWriter:
    def __init__(self, path):
        self.dir = path
        self.temp = dict()

    def __iterate_dir(self):
        """ It itertes all of the leaf files under the root path directory.

        Yields:
            string -- leaf path
        """
        for file in os.listdir(self.dir):
            filename = os.fsdecode(file)
            if filename.endswith(".pickle"):
                yield os.path.join(self.dir, filename), filename

    def __read_pickle(self, path):
        logging.info(path + ' is processing...')
        with open(path, 'rb') as handle:
            file = pickle.load(handle)
        return file

    def __flush_db(self):
        global inverted_index
        logging.info('DB flushing...')
        inverted_index.insert_many(self.temp)
        self.temp.clear()
        logging.info("DB flushed!")

    def write_index(self):
        for path, filename in self.__iterate_dir():
            self.temp = self.__read_pickle(path)
            self.__flush_db()

# asd = IndexWriter("/afs/inf.ed.ac.uk/user/s20/s2001999/TTDS-CW3/index_generator")
asd = IndexWriter("../data_functions/data")
asd.write_index()
