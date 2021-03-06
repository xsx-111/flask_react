#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from http import client
from bson.objectid import ObjectId
from collections import defaultdict
from collections import Counter 
from operator import itemgetter
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

nltk.download('stopwords')
nltk.download('punkt')

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
import certifi


#client = MongoClient(host='localhost',port=27017)
client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttdscluster.zsdaj.mongodb.net/test", tlsCAFile=certifi.where())
db = client.songs   # The database on mongodb

sentences=db.sentences
inverted_index = db.inverted_index
songs_info=db.songs_info
inv_ind_songname=db.songs_inverted_index
inv_ind_artist=db.artists_inverted_index
inv_ind_album=db.albums_inverted_index

from collections import defaultdict
from bson.objectid import ObjectId

def search_result(raw_text, search_type):
    if search_type=='lyrics':
        outputs,info=lyrics_search_result(raw_text)
    else:
        outputs,info=advance_output(raw_text,search_type)
        
    return outputs,info

def lyrics_search_result(raw_text):
    number_results=20
    preprocessed,raw_list = query_preprossing(raw_text,stemming=True)
    
    case, common_dict, left_common_dict,song_lyrics_list,term_not_found_ind = common_dict_search(preprocessed,number_results)
    outputs=defaultdict(list)
    
    if case == 6:
        res_id = [209419,310125,308772,204200,311258,217207,165570,165572,358852,6491,318733,
                      99478,345534,5030,165541,116832,253636,285393,83942,27092]
        for song_id in res_id:
            
            song_output={}
            song_output = songs_info.find({'song_id':song_id})[0]
            song_output.pop('_id')
            lyrics_list=list(song_output['lyrics'][0].values())
            song_output['all_lyrics']=lyrics_list
            song_output['mark_lyric']=lyrics_list[0] #????????????
            song_output.pop('lyrics')
            #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id})[0]['sentence']
            outputs['results'].append(song_output) #??????????????????popularity
            
    elif case in [1,4,5]:
            song_score_dic = tfidf_score(common_dict)
            res_id = ranked_phrase_search(song_score_dic,number_results)
            for song_id in res_id:
                try:
                    song_output={}
                    song_output = songs_info.find({'song_id':song_id})[0]
                    song_output.pop('_id')
                    sen_id  = str(list(common_dict[song_id])[0])
                    song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                    song_output['mark_lyric']=song_output['lyrics'][0][sen_id]
                    #song_output['mark_lyric']=sentences.find({'sentence_id': sen_id})[0]['sentence']
                    song_output.pop('lyrics')
                    outputs['results'].append(song_output)
                except:
                    pass
    
    
    elif case == 2:
        # ?????????????????????????????????n,??????????????????????????????n
        # case, common_dict, left_common_dict,[],term_not_found_ind
        if len(common_dict)!=0:
            song_score_dic1 = tfidf_score(common_dict)
            res_id1 = ranked_phrase_search(song_score_dic1,number_results)
            for song_id in res_id1:
                try:
                    song_output={}
                    song_output = songs_info.find({'song_id':song_id})[0]
                    song_output.pop('_id')
                    sen_id  = str(list(common_dict[song_id])[0])
                    song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                    song_output['mark_lyric']=song_output['lyrics'][0][sen_id]  
                    song_output.pop('lyrics')
                    outputs['results'].append(song_output)
                except:
                    pass
        
        count_list=sorted(list(left_common_dict.keys()),reverse=True)
        res_count=[len(left_common_dict[i]) for i in count_list]
        left_num_result=number_results-len(common_dict.keys())
        for i,count in enumerate(res_count):
            temp_common_dict=left_common_dict[count_list[i]]
            song_score_dic2 = tfidf_score(temp_common_dict)
            res_id2=ranked_phrase_search(song_score_dic2,number_results)
            for song_id in res_id2:
                try:
                    song_output={}
                    song_output = songs_info.find({'song_id':song_id})[0]
                    song_output.pop('_id')
                    sen_id  = str(list(temp_common_dict[song_id])[0])
                    song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                    song_output['mark_lyric']=song_output['lyrics'][0][sen_id]
                    song_output.pop('lyrics')
                    outputs['results'].append(song_output)
                except:
                    pass
            left_num_result-=count
            if left_num_result<0:
                break
        outputs['results']=outputs['results'][:number_results]
        
    elif case == 3:
        #?????????????????????????????????
        if len(common_dict)!=0:
            song_score_dic1 = tfidf_score(common_dict)
            res_id1 = ranked_phrase_search(song_score_dic1,number_results)
            for song_id1 in res_id1:
                try: 
                    song_output={}
                    song_output = songs_info.find({'song_id':song_id1})[0]
                    song_output.pop('_id')
                    sen_id1  = str(list(common_dict[song_id1])[0])
                    song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                    song_output['mark_lyric']=song_output['lyrics'][0][sen_id1]
                    song_output.pop('lyrics')
                    #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id1})[0]['sentence']
                    outputs['results'].append(song_output)
                except:
                    pass
                
            
        
        #?????????????????????????????????
        
        count_l=sorted(list(left_common_dict.keys()),reverse=True)
        
        for count in count_l:
            temp_common_dict=left_common_dict[count]
            song_score_dic2 = tfidf_score(temp_common_dict)
            res_id2=ranked_phrase_search(song_score_dic2,number_results)
            
            for song_id2 in res_id2:
                try:
                    song_output={}
                    song_output = songs_info.find({'song_id':song_id2})[0]
                    song_output.pop('_id')
                    sen_id2  = str(list(temp_common_dict[song_id2])[0])
                    song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                    song_output['mark_lyric']=song_output['lyrics'][0][sen_id2]
                    song_output.pop('lyrics')
                    #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id2})[0]['sentence']
                    outputs['results'].append(song_output)
                except:
                    pass
                
                
#         # ???????????????????????????

        left_num=number_results-len(outputs['results'])

        for most_common_dict in song_lyrics_list:
            lyr_count_list=sorted(list(most_common_dict.keys()),reverse=True)
            res_count=[len(most_common_dict[c]) for c in lyr_count_list]
            for i,lyr_count in enumerate(res_count):
                temp_common_dict=most_common_dict[lyr_count_list[i]]
                song_score_dic3 = tfidf_score(temp_common_dict)
                res_id3=ranked_phrase_search(song_score_dic3,number_results)    
                for song_id3 in res_id3:
                    try: 
                        song_output={}
                        song_output = songs_info.find({'song_id':song_id3})[0]
                        song_output.pop('_id')
                        sen_id3  = str(list(temp_common_dict[song_id3])[0])
                        song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                        song_output['mark_lyric']=song_output['lyrics'][0][sen_id3]
                        song_output.pop('lyrics')
                        #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id3})[0]['sentence']
                        outputs['results'].append(song_output)
                    except:
                        pass
                                       
                if lyr_count >= left_num:
                    break
                else:
                    left_num-=lyr_count
        outputs['results']=outputs['results'][:number_results]
                
    if len(term_not_found_ind) > 0:
        term_not_found = [raw_list[ind] for ind in term_not_found_ind]
        output_info = list(term_not_found)
    else:
        output_info=[]
        
    artist_filter=result_filter(outputs['results'],'artist_name')
    outputs['artist_name'].append(artist_filter)
    album_filter=result_filter(outputs['results'],'album_name')
    outputs['album_name'].append(album_filter)
    
    return dict(outputs), output_info

global TOTAL_NUMBER_OF_SONGS 
TOTAL_NUMBER_OF_SONGS= 326988

# ??????????????????dic  song_score_dic[song_id]
def tfidf_score(common_dict):
    song_score_dic = dict()
    # tf???????????????term ???????????????????????????????????????????????????????????????
    # df:?????????term???????????????????????????????????????????????????
    df_phrase = len(common_dict.keys())
    #???????????????song??????: 
    for song_id in common_dict.keys():    
        idf = math.log(1.0 * TOTAL_NUMBER_OF_SONGS / df_phrase)
        tf = len(common_dict[song_id])
        score = tf * idf
        #?????????????????? ???????????????songid???????????????
        song_score_dic[song_id] = score
    return song_score_dic
    
        
def ranked_phrase_search(scores_dic,number_results):
    #??????songs id????????????
    result_ids = [item[0] for item in get_top(scores_dic,number_results)] 
    return result_ids 

def get_top(scores,n):
        # get top N results (skipping the first `skip` results)
        # return a list of (id, score) tuples, sorted from highest to lowest by score (e.g. [(19, 1.5), (6, 1.46), ...]
        return [(id, score) for id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)][0:n]

def result_filter(res_list,filter_type):
    if res_list!=[]:
        filter_dict=defaultdict(list)
        for i,res in enumerate(res_list):
            filter_value=res[filter_type] # ???????????????????????????????????????
            filter_dict[filter_value].append(res)
        sorted_dict = dict(sorted(filter_dict.items()))
        return sorted_dict
    else:
        return {}
    
    

def query_preprossing(raw_text,stemming=True):
    tokenized = tokenize(raw_text)
    raw_list = list(filter(lambda x: x.isalnum(), tokenized))
    filtered = [term.lower() for term in tokenized]
    if (stemming):
        filtered = stem(filtered)
    preprocessed = list(filter(lambda x: x.isalnum(), filtered))
    return preprocessed,raw_list


    
def song_sentence_id(term):
    sentence_id_dict=defaultdict(tuple)
    try:
        
        part=inverted_index.find({"term": term})
        for i in range(10):
            part_i=part[i]        
            for song_dict in part_i['songs']:
                sentence_id=tuple(song_dict['sentences'])
                # store the song_id and corresonding sentence_id tuple into the dictionary
                sentence_id_dict[song_dict['song_id']]=sentence_id
        return sentence_id_dict
    # ??????????????????????????????empty dictionary
    except IndexError:
        return sentence_id_dict


def common_songs_search(cursors):
    #??? common song id ????????????list
    common_song_id = cursors.pop()
    for each_term_dic in cursors:
        if len(set(common_song_id) & set(each_term_dic.keys()))>0:
            common_song_id = set(common_song_id) & set(each_term_dic.keys())
        else:
            common_song_id = []
            break
    return common_song_id


def common_lyric_search(cursors2,common_song_id):
    common_dict={}
    for sid in common_song_id:
        ld3 = cursors2.copy()
        temp = ld3.pop()
        if sid not in common_dict:
            common_dict[sid] = temp[sid]
        for each_term_dic in ld3:
            #each_term_dic = ld3[0]
            if len(set(common_dict[sid]) & set(each_term_dic[sid]))>0:
                common_dict[sid] = set(common_dict[sid]) & set(each_term_dic[sid])
            else:
                #??????????????????????????? ???????????? ??????break??? ???????????????
                common_dict[sid] = []
                #found = False
                break     
    #?????????????????????
    for sid in list(common_dict.keys()):
        if not common_dict.get(sid):
            del common_dict[sid]

    return common_dict

def most_common_lyric_search(cursors2,left_common_sid):
    
    lyrics_id_list = []
    for each_term_dic in cursors2:
        # For n number of items, lyrics_id_list contains n tuples 
        # and each tuples contain len(left_common_sid) subtuples of lyric id
        lyrics_id_list.append(itemgetter(*list(left_common_sid))(each_term_dic))
    
    # max_count_dict:{?????????????????????????????????: {??????ID??????????????????ID}}
    max_count_dict=defaultdict(dict)
    
    for ind,sid in enumerate(left_common_sid):
        # lyrics_list_each_sid contains n tuples, 
        # each tuple contains the lyric id of corresponding term
        lyrics_tuple_single_song=[lyrics_tup[ind] for lyrics_tup in lyrics_id_list]
        # merge the tuples and convert it to a single list
        lyrics_merge_list=[j for i in lyrics_tuple_single_song for j in i] 
        
        
        # count the lyric id occurences
        lyrics_term_count=Counter(lyrics_merge_list).most_common()
        # find the max amount of occurences
        max_count=lyrics_term_count[0][1]
        lid_list=[]
        for lyric_id, count in lyrics_term_count:
            if count<max_count:
                break
            lid_list.append(lyric_id)
        
        max_count_dict[max_count][sid]=lid_list  

    return max_count_dict
# max_count_dict:{?????????????????????????????????: {??????ID??????????????????ID}}
# ????????????common_song, ???????????????????????????????????????
# ?????? s1 ????????????????????????????????????????????????????????????????????????????????????id
# ????????????????????????A??????B????????????????????????C??????B,????????????????????????

def most_common_song_search(cursors2):
    song_id_list = []
    # most_common_song: {????????????????????????ID} 
    # ?????????????????????????????????????????????
    most_common_song=defaultdict(list)
    
    for each_term_dic in cursors2:
        song_id_list+=list(each_term_dic.keys())
        
    songid_tup=Counter(song_id_list).most_common()    
    for sid,count in songid_tup:
        if count!=len(cursors2) : #?????????????????????????????????????????????
            most_common_song[count].append(sid)

    return most_common_song

def common_dict_search(preprocessed,number_results):
    terms = preprocessed
    
    if len(terms) == 1:
        common_dict = song_sentence_id(terms[0])
        if len(common_dict) ==0:
    #6 ??????????????????????????????
            case = 6
            return case,{},{},[],[0]
        #?????????????????????????????????
        else:
            #5 ????????????????????? ??? ???????????????????????????????????????
            case = 5
            return case,common_dict,{},[],[]
        
    if len(terms) >1:
        cursors =[]
        used_terms = []
        term_not_found_ind=[]
        for ind, term in enumerate(terms):
            #?????????????????????term????????? {???ID?????????ID}
            term_dict =song_sentence_id(term)
            # ????????????????????????
            if len(term_dict)!=0:
                cursors.append(term_dict)
                used_terms.append(term)
            else:
                term_not_found_ind.append(ind)
        
        #6 ?????????????????????
        if len(term_not_found_ind)==len(terms):
            case = 6
            return case,{},{},[],term_not_found_ind
    
    #5. ????????????????????? ??? ???????????????????????????????????????
        if len(used_terms) == 1:
            common_dict = song_sentence_id(used_terms[0])
            case = 5
            return case,common_dict,{},[],term_not_found_ind
        else: 
            cursors2 = cursors.copy()
            
        
        
        common_song_id=common_songs_search(cursors)
        if len(common_song_id) == 0:
            term_merge_dict = {}
            case = 4
            for term in terms:
                term_dict = song_sentence_id(term)
                for key in term_dict.keys():
                    term_merge_dict[key]=term_dict[key]
            return case, term_merge_dict, {},[],term_not_found_ind
        
        elif len(common_song_id) > 0:
            common_dict=common_lyric_search(cursors2,common_song_id)
            left_common_sid=common_song_id-set(common_dict.keys())
            if len(left_common_sid)>0:
            # ?????????????????????????????????????????????
                left_common_dict=most_common_lyric_search(cursors2,left_common_sid)
                
            #????????????????????????????????? ?????????????????????????????????
            #???common_songid???????????????common??????id

            # ???????????????????????????????????????n:
            if len(common_song_id) >= number_results:
                # ????????????????????????????????????n
                if len(common_dict.keys()) >= number_results:
                    case = 1
                    return case, common_dict, {},[],term_not_found_ind
                # ????????????????????????????????????n
                elif len(common_dict.keys()) < number_results:
                    case = 2
                    return case, common_dict, left_common_dict,[],term_not_found_ind  

            #3?????????????????????????????????????????????n???   
            elif len(common_song_id) < number_results:
                # ??????common_dict, left_common_dict??????????????????most_common_song
                case=3
                # ??????????????????????????????
                left_num_result=number_results-len(common_song_id)

                # ???????????????????????????????????????????????????????????????????????????(???????????????????????????????????????)
                # most_common_song_dict: {??????????????????[??????ID]} 
                most_common_song=most_common_song_search(cursors2)

                # song_lyrics_list is a list of dictionary, each dict corresponds to 
                # different max number of common terms in a song 
                song_lyrics_list=[]
                # count_list??????????????????????????????????????? e.g.[3,2,1]
                count_list=sorted(list(most_common_song.keys()),reverse=True)

                for count in count_list:
                    max_count_dict=defaultdict(dict)
                    # max_count_dict={max_term_count_in_one_lyric: {song_id: lyric_id}}
                    for sid in most_common_song[count]:
                        lyrics_list=[d[sid] for i,d in enumerate(cursors2) if sid in list(d.keys())]
                        # merge the tuples and convert it to a single list
                        lyrics_merge_list=[j for i in lyrics_list for j in i] 
                        lyrics_term_count=Counter(lyrics_merge_list).most_common()
                        # ?????????????????????????????????
                        max_count=lyrics_term_count[0][1]
                        lid_list=[]
                        for lyric_id, ly_count in lyrics_term_count:
                            if ly_count<max_count:
                                break
                        lid_list.append(lyric_id)
                        max_count_dict[max_count][sid]=lid_list
                    song_lyrics_list.append(max_count_dict)

                    if len(most_common_song[count]) >= left_num_result:
                    # ?????????????????????????????????????????????break
                        break
                return case, common_dict, left_common_dict,song_lyrics_list,term_not_found_ind    
            
            


# ## Advance search

def advance_output(query_advance,this_search_name):
    # ????????????????????????
    number_results=20
    search_terms,raw_term = query_preprossing(query_advance)
    
    case,res_id,term_not_found_ind,res_exact= advance_search(this_search_name,search_terms,number_results)
    outputs=defaultdict(list)
    
    if case==0:
        outputs['results']=res_exact
        
    elif case==1:
        if len(res_id) >0:
            for song_id in res_id:
                try:
                    song_output = {}
                    song_output = songs_info.find({'song_id':int(song_id)})[0]
                    song_output.pop('_id')
                    lyrics_list=list(song_output['lyrics'][0].values())
                    song_output['all_lyrics']=lyrics_list
                    song_output['mark_lyric']=lyrics_list[0]
                    song_output.pop('lyrics')
                    outputs['results'].append(song_output)
                except:
                    pass

        else: #?????????????????? ??????????????????
            res_id = [209419,310125,308772,204200,311258,217207,165570,165572,358852,6491,318733,
                          99478,345534,5030,165541,116832,253636,285393,83942,27092]
            for song_id in res_id:
                song_output = {}
                song_output = songs_info.find({'song_id':song_id})[0]
                song_output.pop('_id')
                lyrics_list=list(song_output['lyrics'][0].values())
                song_output.pop('lyrics')
                song_output['all_lyrics']=lyrics_list
                song_output['mark_lyric']=lyrics_list[0]
                outputs['results'].append(song_output)


    if len(term_not_found_ind) > 0:
        term_not_found = [raw_term[ind] for ind in term_not_found_ind]
        output_info = list(term_not_found)

    else:
        output_info=[]

    artist_filter=result_filter(outputs['results'],'artist_name')
    outputs['artist_name'].append(artist_filter)
    album_filter=result_filter(outputs['results'],'album_name')
    outputs['album_name'].append(album_filter)
        
    return dict(outputs),output_info

def advance_search(this_search_name,search_terms,number_results):
    #???????????? search_term??????????????????????????????
    
    # ??????????????????????????????index?????????
    term_not_found_ind=[]
    
    #???????????????
    #??????????????? ????????????????????? ??????popularity????????????
    res_id = []        
    
    
    popularity_dic={} # {songid:popularity}
    songid_exact_list = []                
    exact_search_cursors=songs_info.find({this_search_name:search_terms})
    res_exact=[]
    
    try:
         # ????????????????????????????????????Index Error
        exact_search_cursors[0]
    except:
        # ??????????????????????????????????????????
        
        #inv_ind_songname {term: [songid1,songid2,...]}
        #inv_ind_artist {term: {'artist1':[sid1,sid2,...]}}
        #inv_ind_album {term: {'album1':[sid1,sid2,...]}}

        
        case=1
        if this_search_name=='song_name_preprocess':
            count_dict = defaultdict(dict)
            songid_list_vag=[]
            for ind,term in enumerate(search_terms):
                try:
                    term_dict=inv_ind_songname.find({'term': term})[0]['songs']
                    songid_list_vag+=list(term_dict.keys())
                    for key in term_dict.keys():
                        popularity_dic[key]=term_dict[key]
                except:
                    term_not_found_ind.append(ind)
                    
            if len(songid_list_vag) > 0:
                sid_count = Counter(songid_list_vag).most_common()
                for sid,count in sid_count:                
                    count_dict[count][sid]=popularity_dic[sid]
                    # ??????????????????????????????????????????????????????,???????????????????????????????????????number_results

                # sorted the key of count_dict
                count_list=sorted(list(count_dict.keys()),reverse=True) 
                # find the number of dict for each key in count_list
                songid_count=[len(count_dict[i]) for i in count_list]
                for i,c in enumerate(songid_count):
                    count_popu_dict=count_dict[count_list[i]]
                    res_id+=ranked_advance_search(count_popu_dict,number_results)
                    if c > number_results:
                        break

            else: #??????????????????????????????,???popularity
                res_id = [209419,310125,308772,204200,311258,217207,165570,165572,358852,6491,318733,
                          99478,345534,5030,165541,116832,253636,285393,83942,27092]

                    
        elif this_search_name=='artist_name_preprocess' or 'album_name_preprocess':
            if this_search_name=='artist_name_preprocess':
                data=inv_ind_artist 
                datatype='artists'
            else:
                data=inv_ind_album
                datatype='albums'
            
            name_list=[]
            count_dict=defaultdict(list)
            name_dict=defaultdict(dict)
            
            
            for ind,term in enumerate(search_terms):
                try:
                    term_dict=data.find({'term': term})[0]# check IndexError
             
                    name_keys=list(term_dict[datatype].keys())
                    name_list+=name_keys
                    for name in name_keys:
                        name_dict[name]=term_dict[datatype][name]
                        
                except:
                    term_not_found_ind.append(ind)
            
            
            if len(name_list)>0:
                count_name=Counter(name_list).most_common()
                for name,count in count_name:                
                    count_dict[count].append(name)
                    # ??????????????????????????????????????????????????????,???????????????????????????????????????number_results

                # sorted the key of count_dict
                count_list=sorted(list(count_dict.keys()),reverse=True) 
                
                for i in count_list:
                    sid_popu_dict={}
                    for name in count_dict[i]:
                        name_sid_popu_dict=name_dict[name]
                        for sid in name_sid_popu_dict.keys():
                            sid_popu_dict[sid]=name_sid_popu_dict[sid]
                    res_id+=ranked_advance_search(sid_popu_dict,number_results) 
                    if len(res_id)>number_results:
                        break
            elif len(name_list)==0:
                res_id = [209419,310125,308772,204200,311258,217207,165570,165572,358852,6491,318733,
                          99478,345534,5030,165541,116832,253636,285393,83942,27092]

        return case,res_id,term_not_found_ind,res_exact
    
    else:
        #????????????
        case=0
        for exact_song_dict in exact_search_cursors:
            try:
                lyrics_list=list(exact_song_dict['lyrics'][0].values())
                exact_song_dict.pop('lyrics')
                exact_song_dict.pop('_id')
                exact_song_dict['all_lyrics']=lyrics_list
                exact_song_dict['mark_lyric']=lyrics_list[0]
                res_exact.append(exact_song_dict)
            except:
                pass
        return case,[],[],res_exact

def ranked_advance_search(popularity_dic,number_results):
    #??????songs id????????????
    result_ids = [item[0] for item in get_top(popularity_dic,number_results)] 
    return result_ids 

def get_top(popularity_dic,number_results):
        # get top N results (skipping the first `skip` results)
        # return a list of (id, score) tuples, sorted from highest to lowest by score (e.g. [(19, 1.5), (6, 1.46), ...]
        return [(id, popularity) for id, popularity in sorted(popularity_dic.items(), key=lambda item: item[1], reverse=True)][0:number_results]
 



# In[ ]:





# In[2]:


# ????????????

# #case1
# raw_text='creep you' #15s

# #case2
# raw_text='creep you out' #12.8s

# #case3
# raw_text='black pain see sweet call' # 10s

# #case4
# raw_text='gucci Saffronia' #2.9s

# #case5
# raw_text='creep abcdos' #???????????????????????? 3.9s
# #raw_text='creep' #??????????????? 3.88s

#case6
# raw_text='abcdos' #3s
# #raw_text='phrasesea, abcdos' #3s


# In[ ]:





# In[29]:


# advance search
# import time
# s=time.time()
#raw_text='phrasesea, abcdos'
# raw_text='Share Your Love With Little Prayer'
#raw_text='Stairway to Heaven'
# raw_text='Greatest Hits'
#raw_text='mayhem'
#raw_text='Nina Sarah'

#search_type = 'artist_name_preprocess'
# search_type = 'album_name_preprocess'
#search_type = 'song_name_preprocess'
# search_type = 'lyrics'
# output,info=search_result(raw_text,search_type)
# e=time.time()


# print(e-s)

#output['results']


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




