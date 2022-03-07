# python create_inverted_index.py
import os
import sys
sys.path.append("..")
import json
import pickle

import preprocessing
import database_functions
import argparse
import logging


logging.basicConfig(filename='result.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class IndexGenerator:
    def __init__(self, activate_stemming = True, activate_stop = False, start_index=0):
        """ This class reaeds the documents from db, generates an inverted index and saves it into db.

        Keyword Arguments:
            activate_stemming {bool} -- True enables the stemming function over the terms (default: {True})
            activate_stop {bool} -- True enables removing stop words (default: {False})
        """
        self.activate_stemming = activate_stemming
        self.activate_stop = activate_stop
        self.start = start_index

        self.temp = dict()

    def run_indexing(self):
        """
        This function gets the sentences from db and updates the inverted index in db by iterating the sentences.
        """
#         songs_num = database_functions.get_max_songs_id()
        cursors = database_functions.get_sentences_cursors()
        part_num = 1
        batch_size = 20000

#         for i, cursor in enumerate(cursors):
        for cursor in cursors:
            if (int(cursor.get('Song_id')[1:]) - 1) // batch_size == part_num:
                self.__regularize_dict()
                self.__save_pickle("part_" + str(part_num))
                logging.info("part_" + str(part_num) + "is finished.")
                part_num += 1

#             logging.info("loading the " + str(i) + "th sentences")
            self.__load_tempfile(cursor.get('Sentence_id'), cursor.get('Sentence'), cursor.get('Song_id'), cursor.get('Song_name'))

        if len(self.temp) != 0:
            self.__regularize_dict()
            self.__save_pickle("the_last_part")
            logging.info("the_last_part is finished.")


    def __load_tempfile(self, sentence_id, sentence, song_id, song_name):

        if sentence is None:
            return

        preprocessed = preprocessing.preprocess(sentence, stemming=self.activate_stemming, stop=self.activate_stop)
        preprocessed = list(filter(None, preprocessed))

        word_count = len(preprocessing.preprocess(sentence, stemming=False, stop=False))

        for term in set(preprocessed):
            positions = [n for n,item in enumerate(preprocessed) if item==term]
            self.temp[term] = self.temp.get(term, {
                'term': term,
#                 'doc_freq': 0,
                'songs': dict()
            })
#             self.temp[term]['doc_freq'] += 1
            self.temp[term]['songs'][song_id] = self.temp[term]['songs'].get(song_id, {'song_id': song_id, 'term_freq': 0, 'sentences': list()})
            self.temp[term]['songs'][song_id]['term_freq'] += len(positions)
            self.temp[term]['songs'][song_id]['sentences'].append({
                        'sentence_id': sentence_id,
                        'len': word_count,
                        'pos': positions
                    })

    def __regularize_dict(self):
        for value in self.temp.values():
            value['songs'] = list(value['songs'].values())

    def __save_pickle(self, name):
        with open('../data_functions/data/'+name + '.pickle', 'wb') as handle:
            pickle.dump(list(self.temp.values()), handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.temp.clear()

def run_with_arguments(stem, stop, start):
    indexGen = IndexGenerator(activate_stop=stop, activate_stemming=stem, start_index=start)
    indexGen.run_indexing()

parser = argparse.ArgumentParser(description='Inverted Index Generator')
parser.add_argument('--stemming', nargs="?", type=str, default='True', help='Activate stemming')
parser.add_argument('--remove_stopwords', nargs="?", type=str, default='False', help='Remove stopwords')
parser.add_argument('--start', nargs="?", type=int, default=0, help='Start batch index')
args = parser.parse_args()

run_with_arguments(eval(args.stemming), eval(args.remove_stopwords), args.start)
