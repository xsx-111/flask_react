#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from bson.objectid import ObjectId

# phrase search
import pymongo
import gridfs
import json
import time
import math

import re
import sys
import os
import nltk
import string

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

# nltk.download('stopwords')
# nltk.download('punkt')

stop_words = set(stopwords.words('english'))

tweetTokenizer = TweetTokenizer()

def tokenize(string_line):
    ''' This function tokenizes the string of text and removes all non alpha-numeric characters
    it takes a string of text as an argument
    it returns a list of all individual words after tokenizing and removing all non alpha-numeric characters'''    
    #return re.findall('[a-zA-Z0-9]+', string_line.lower())
    #return word_tokenize(string_line)
    tokens = tweetTokenizer.tokenize(string_line)
    return list(filter(None, [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]))

def stem(tokens):
    '''This function takes a list of tokens as an argument
    it uses Porter Stemmer to stem the words in the tokens list
    (Here we are using the NLTK library to do this task)
    it retuns a list of all the tokens after stemming'''
    ps = PorterStemmer()
    return [ps.stem(token) for token in tokens]

from pymongo import MongoClient

#client = MongoClient('mongodb://admin:iamyourfather@127.0.0.1:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
#client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttds-cluster.zsdaj.mongodb.net/?retryWrites=true&w=majority")
client = MongoClient(host='localhost',port=27017)
db = client.songs   # The database on mongodb

sentences=db.sentences
inverted_index = db.inverted_index
songs_info=db.songs_info

from collections import defaultdict
from bson.objectid import ObjectId

def search_result(raw_text):
    preprocessed,raw_list = query_preprossing(raw_text,stemming=True)

    common_dict_output= common_dict_search(preprocessed)
    if common_dict_output !={}:
        common_dict,term_not_found_ind=common_dict_output
        outputs=[]
        song_score_dic = phrase_tfidf(common_dict)
        res_id = ranked_phrase_search(song_score_dic, 10)
        for song_id in res_id:
            song_output={}
            song_output = songs_info.find({'song_id':song_id})[0]
            sen_id  = list(common_dict[song_id])[0]
            #标红的歌词内容（只取第一句） 
            song_output['mark_lyric'] = sentences.find({'Sentence_id': sen_id})[0]['Sentence']
            outputs.append(song_output)
            
        if len(term_not_found_ind) >0:
            term_not_found = [raw_list[ind] for ind in term_not_found_ind]
            output_info = list(term_not_found)
            #output_info='{} not found' .format(', '.join(term_not_found))
        else:
            output_info=[]
            
        return outputs,output_info
    
    else: 
        return common_dict_output    
    
    
def query_preprossing(raw_text,stemming=True):
    tokenized = tokenize(raw_text)
    raw_list = list(filter(lambda x: x.isalnum(), tokenized))
    filtered = [term.lower() for term in tokenized]
    if (stemming):
        filtered = stem(filtered)
    preprocessed = list(filter(lambda x: x.isalnum(), filtered))
    return preprocessed,raw_list


def common_dict_search(query_params_after):
    
    terms = query_params_after
    
    if len(terms) == 1:
        common_dict = song_sentence_id(terms[0])
        if len(common_dict) ==0:
            return {},[]
        else:
            return common_dict,[]
            
    
    if len(terms) >1:
        cursors =[]
        term_not_found_ind=[]
        for ind, term in enumerate(terms):
            #这里存了每一个term的字典 {歌ID：歌词ID}
            term_dict=song_sentence_id(term)
            if len(term_dict)!=0:
                cursors.append(term_dict)
            else:
                term_not_found_ind.append(ind)
            
        if len(term_not_found_ind)==len(terms):
            return {},[]
        else: 
            cursors2 = cursors.copy()
        
        #取 common song id 返回一个list
        common_song_id = cursors.pop()
        for each_term_dic in cursors:
            if len(set(common_song_id) & set(each_term_dic.keys()))>0:
                common_song_id = set(common_song_id) & set(each_term_dic.keys())
            else:
                common_song_id = []
                break
                
        
        #只有有共同的歌词 才进行下一步：
        #取common_songid以及里面的common歌词id
        if len(common_song_id) > 0:
            common_dict = {}
            for sid in common_song_id:
                ld3 = cursors2.copy()
                temp = ld3.pop()
                common_dict[sid] = temp[sid]
                for each_term_dic in ld3:
                    #each_term_dic = ld3[0]
                    if len(set(common_dict[sid]) & set(each_term_dic[sid]))>0:
                        common_dict[sid] = set(common_dict[sid]) & set(each_term_dic[sid])
                    else:
                        #如果没有共同的歌词 直接为空 并且break掉 看下一个歌
                        common_dict[sid] = []
                        #found = False
                        break
                  
            #只留下不为空的
            for sid in list(common_dict.keys()):
                if not common_dict.get(sid):
                    del common_dict[sid]
        
            return common_dict,term_not_found_ind
        else:
            return {},[]

def song_sentence_id(term):
    sentence_id_dict=defaultdict(tuple)
    try:
        # initialise the dictionary
        for i in range(5):
            part_i=db.inverted_index.find({"term": term})[i]
            for song_dict in part_i['songs']:
                # initialize the tuple of ObjectId
                sentence_id=() 
                # iterate over the sentences for each song
                for term_sentence_dict in song_dict['sentences']:
                    # update the tuple
                    sentence_id+=(term_sentence_dict['sentence_id'],)
                # store the song_id and corresonding sentence_id tuple into the dictionary
                sentence_id_dict[song_dict['song_id']]=sentence_id
        return sentence_id_dict
    # 搜不到词的话返回一个empty dictionary
    except IndexError:
        return sentence_id_dict


global TOTAL_NUMBER_OF_SONGS 
TOTAL_NUMBER_OF_SONGS= 3089762

def phrase_tfidf(common_dict):
    song_score_dic = dict()
    # tf就是这几个term 同时在一首歌出现了几次（在这里可以算行数）
    # df:这几个term一共在多少首歌里同时在同一行出现了
    df_phrase = len(common_dict.keys())
    #对于每一个song交集: 
    for song_id in common_dict.keys():    
        idf = math.log(1.0 * TOTAL_NUMBER_OF_SONGS / df_phrase)
        tf = len(common_dict[song_id])
        score = tf * idf
        #把分数加上去 存在对应的songid里当成分数
        song_score_dic[song_id] = score
    return song_score_dic
    
        
def ranked_phrase_search(scores_dic,number_results):
    #返回songs id的前几个
    result_ids = [item[0] for item in get_top(scores_dic,number_results,skip=0)] 
    return result_ids

def get_top(scores,n,skip=0):
    # get top N results (skipping the first `skip` results)
    # return a list of (id, score) tuples, sorted from highest to lowest by score (e.g. [(19, 1.5), (6, 1.46), ...]
    return [(id, score) for id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)][skip:skip+n]

# print(search_result('creep you out erfoakd'))
# print(search_result('what do you want'))
