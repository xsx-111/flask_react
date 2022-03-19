#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
from http import client
from bson.objectid import ObjectId
from collections import defaultdict
from collections import Counter 
from operator import itemgetter
from pymongo import MongoClient
import certifi


import popularity

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


#client = MongoClient(host='localhost',port=27017)
client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttdscluster.zsdaj.mongodb.net/test", tlsCAFile=certifi.where())
db = client.songs   # The database on mongodb


inverted_index = db.inverted_index_test
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


# In[2]:


def lyrics_search_result(raw_text):
    number_results=20
    preprocessed,raw_list = query_preprossing(raw_text,stemming=True)
    
    
    if len(preprocessed)==0:
        outputs=defaultdict(list)
        outp=popularity.output()  
        outputs['results']=outp.output_list[:number_results]
        artist_filter=result_filter(outputs['results'],'artist_name')
        outputs['artist_name'].append(artist_filter)
        album_filter=result_filter(outputs['results'],'album_name')
        outputs['album_name'].append(album_filter)
        return dict(outputs), []
        
        
    elif len(preprocessed)>0:
        preprocessed = preprocessed[0:10]
    
        case, common_dict, left_common_dict,song_lyrics_list,term_not_found_ind = common_dict_search(preprocessed,number_results)
        outputs=defaultdict(list)

        if len(term_not_found_ind) > 0:
            term_not_found = [raw_list[ind] for ind in term_not_found_ind]
            output_info = list(term_not_found)
        else:
            output_info=[]

        if case == 6:
            outp=popularity.output()  
            outputs['results']=outp.output_list #推荐歌单信息popularity

        elif case in [1,4,5]:
            song_score_dic = tfidf_score(common_dict)
            res_id = ranked_phrase_search(song_score_dic,number_results)
            for song_id in res_id:
                try:
                    song_output={}
                    song_output = songs_info.find({'song_id':int(song_id)})[0]
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
            # 搜的词在同一首歌的大于n,但在同一行的歌曲小于n
            # case, common_dict, left_common_dict,[],term_not_found_ind
            if len(common_dict)!=0:
                song_score_dic1 = tfidf_score(common_dict)
                res_id1 = ranked_phrase_search(song_score_dic1,number_results)
                for song_id in res_id1:
                    try:
                        song_output={}
                        song_output = songs_info.find({'song_id':int(song_id)})[0]
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
                        song_output = songs_info.find({'song_id':int(song_id)})[0]
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
            #所有词在同一首歌同一行
            if len(common_dict)!=0:
                song_score_dic1 = tfidf_score(common_dict)
                res_id1 = ranked_phrase_search(song_score_dic1,number_results)
                for song_id1 in res_id1:
                    try: 
                        song_output={}
                        song_output = songs_info.find({'song_id':int(song_id1)})[0]
                        song_output.pop('_id')
                        sen_id1  = str(list(common_dict[song_id1])[0])
                        song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                        song_output['mark_lyric']=song_output['lyrics'][0][sen_id1]
                        song_output.pop('lyrics')
                        #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id1})[0]['sentence']
                        outputs['results'].append(song_output)
                    except:
                        pass

            #所有词在同一首歌不同行

            count_l=sorted(list(left_common_dict.keys()),reverse=True)

            for count in count_l:
                temp_common_dict=left_common_dict[count]
                song_score_dic2 = tfidf_score(temp_common_dict)
                res_id2=ranked_phrase_search(song_score_dic2,number_results)

                for song_id2 in res_id2:
                    try:
                        song_output={}
                        song_output = songs_info.find({'song_id':int(song_id2)})[0]
                        song_output.pop('_id')
                        sen_id2  = str(list(temp_common_dict[song_id2])[0])
                        song_output['all_lyrics']=list(song_output['lyrics'][0].values())
                        song_output['mark_lyric']=song_output['lyrics'][0][sen_id2]
                        song_output.pop('lyrics')
                        #song_output['mark_lyric'] = sentences.find({'sentence_id': sen_id2})[0]['sentence']
                        outputs['results'].append(song_output)
                    except:
                        pass


             # 仅部分词在同一首歌

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
                            song_output = songs_info.find({'song_id':int(song_id3)})[0]
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



        artist_filter=result_filter(outputs['results'],'artist_name')
        outputs['artist_name'].append(artist_filter)
        album_filter=result_filter(outputs['results'],'album_name')
        outputs['album_name'].append(album_filter)

        return dict(outputs), output_info

global TOTAL_NUMBER_OF_SONGS 
TOTAL_NUMBER_OF_SONGS= 326988

# 返回的是一个dic  song_score_dic[song_id]
def tfidf_score(common_dict):
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
            filter_value=res[filter_type] # 取对应字典的歌手名，专辑名
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


# In[3]:


def song_sentence_id(term):
    sentence_id_dict=defaultdict(tuple)
    sentence_id_dict1=defaultdict(tuple)
    sentence_id_dict2=defaultdict(tuple)
    part=inverted_index.find({"term": term})
    try:
        part[0]
    except IndexError:
        return sentence_id_dict
    else:
        for i in range(3):
            try:
                part_i=part[i]['songs']
#                 sentence_id_dict.update(part_i)
                #sentence_id_dict=dict(sentence_id_dict.items()+part_i.items())
                sentence_id_dict=dict(sentence_id_dict,**part_i)
            except:
                pass
        
        for i in range(3,6):
            try:
                part_i=part[i]['songs']
#                 sentence_id_dict.update(part_i)
                #sentence_id_dict=dict(sentence_id_dict.items()+part_i.items())
                sentence_id_dict1=dict(sentence_id_dict1,**part_i)
            except:
                pass
            
        for i in range(6,10):
            try:
                part_i=part[i]['songs']
#                 sentence_id_dict.update(part_i)
                #sentence_id_dict=dict(sentence_id_dict.items()+part_i.items())
                sentence_id_dict2=dict(sentence_id_dict2,**part_i)
            except:
                pass
        
            
        sentence_id_dict.update(sentence_id_dict1)
        sentence_id_dict.update(sentence_id_dict2)
        
        for sid in sentence_id_dict.keys():
            lyric_l=tuple(sentence_id_dict[sid])
            sentence_id_dict[sid]=lyric_l
         
        return sentence_id_dict
    # 搜不到词的话返回一个empty dictionary
    


# In[ ]:





# In[4]:


# from timeit import timeit
# from timeit import repeat

# t=repeat("song_sentence_id('me'),song_sentence_id('you'),song_sentence_id('these'),song_sentence_id('new')",'from __main__ import song_sentence_id', number=1,repeat=20)
# sum(t)/len(t)


# In[5]:




# def song_sentence_id(term):
#     sentence_id_dict=defaultdict(tuple)
#     sentence_id_dict1=defaultdict(tuple)
#     part=inverted_index.find({"term": term})
#     try:
#         part[0]
#     except IndexError:
#         return sentence_id_dict
#     else:
#         for i in range(5):
#             try:
#                 part_i=part[i]['songs']
# #                 sentence_id_dict.update(part_i)
#                 #sentence_id_dict=dict(sentence_id_dict.items()+part_i.items())
#                 sentence_id_dict=dict(sentence_id_dict,**part_i)
#             except:
#                 pass
        
#         for i in range(5,10):
#             try:
#                 part_i=part[i]['songs']
# #                 sentence_id_dict.update(part_i)
#                 #sentence_id_dict=dict(sentence_id_dict.items()+part_i.items())
#                 sentence_id_dict1=dict(sentence_id_dict1,**part_i)
#             except:
#                 pass
            
#         sentence_id_dict.update(sentence_id_dict1)
        
#         for sid in sentence_id_dict.keys():
#             lyric_l=tuple(sentence_id_dict[sid])
#             sentence_id_dict[sid]=lyric_l
         
#         return sentence_id_dict
#     # 搜不到词的话返回一个empty dictionary
    

def common_songs_search(cursors):
    #取 common song id 返回一个list
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
                #如果没有共同的歌词 直接为空 并且break掉 看下一个歌
                common_dict[sid] = []
                #found = False
                break     
    #只留下不为空的
    for sid in list(common_dict.keys()):
        if not common_dict.get(sid):
            del common_dict[sid]

    return common_dict

def most_common_lyric_search(cursors2,left_common_sid,all_song_lyr_dict):
    
    lyrics_id_list = []
    for each_term_dic in cursors2:
        # For n number of items, lyrics_id_list contains n tuples 
        # and each tuples contain len(left_common_sid) subtuples of lyric id
        lyrics_id_list.append(itemgetter(*list(left_common_sid))(each_term_dic))
    
    # max_count_dict:{在某一行最多出现的词数: {歌曲ID：对应的歌词ID}}
    max_count_dict=defaultdict(dict)
    if len(left_common_sid) >1:
        for ind,sid in enumerate(left_common_sid):
            lyrics_merge_list = list(all_song_lyr_dict[sid])
            # count the lyric id occurences
            lyrics_term_count = Counter(lyrics_merge_list).most_common()   
            # find the max amount of occurences
            max_count = lyrics_term_count[0][1]
            lid_list = [k for k,v in dict(lyrics_term_count).items() if v == max_count] 
            max_count_dict[max_count][sid]=lid_list  
            
    elif len(left_common_sid) ==1:
        sid = list(left_common_sid)[0]
        lyrics_merge_list=[j for i in lyrics_id_list for j in i] 
         
        # count the lyric id occurences
        lyrics_term_count = Counter(lyrics_merge_list).most_common()
        
        # find the max amount of occurences
        max_count = lyrics_term_count[0][1]
        lid_list = [k for k,v in dict(lyrics_term_count).items() if v == max_count]
    
        max_count_dict[max_count][sid]=lid_list  

    return max_count_dict
# max_count_dict:{在某一行最多出现的词数: {歌曲ID：对应的歌词ID}}
# 对每一首common_song, 找到出现词数最多的所有歌词
# 例： s1 最多同时出现两个搜索词在同一行，则返回所有满足条件的歌词id
# 缺点：同时出现词A和词B，或者同时出现词C和词B,会视为同一种情况

def most_common_song_search(cursors2):
    song_id_list = []
    # most_common_song: {出现的词数：歌曲ID} 
    # 不考虑所有词都在同一首歌的情况
    most_common_song=defaultdict(list)
    
    for each_term_dic in cursors2:
        song_id_list+=list(each_term_dic.keys())
        
    songid_tup=Counter(song_id_list).most_common()    
    for sid,count in songid_tup:
        if count!=len(cursors2) : #不考虑所有词都在同一首歌的情况
            most_common_song[count].append(sid)

    return most_common_song


# In[7]:


def common_dict_search(preprocessed,number_results):
    terms = preprocessed
    
    if len(terms) == 1:
        common_dict = song_sentence_id(terms[0])
        if len(common_dict) ==0:
    #6 搜索的词都不在数据库
            case = 6
            return case,{},{},[],[0]
        #这里要返回推荐歌单！！
        else:
            #5 只搜索了一个词 或 搜索多个词只有一个在数据库
            case = 5
            return case,common_dict,{},[],[]
        
    if len(terms) >1:
        cursors =[]
        used_terms = []
        term_not_found_ind=[]
        #s = time.time()
        for ind, term in enumerate(terms):
            #这里存了每一个term的字典 {歌ID：歌词ID}
            ### 在这里找
            term_dict =song_sentence_id(term)
            # 只要数据库里有的
            if len(term_dict)!=0:
                cursors.append(term_dict)
                used_terms.append(term)
            else:
                term_not_found_ind.append(ind)
        #p = time.time()
        #print(p-s)
        
        
        #6 全都不在数据库
        if len(term_not_found_ind)==len(terms):
            case = 6
            return case,{},{},[],term_not_found_ind
    
    #5. 只搜索了一个词 或 搜索多个词只有一个在数据库
        if len(used_terms) == 1:
            common_dict = song_sentence_id(used_terms[0])
            case = 5
            return case,common_dict,{},[],term_not_found_ind
        else: 
            cursors2 = cursors.copy()
            
        
        
        common_song_id = common_songs_search(cursors)
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
            
            all_song_lyr_dict=defaultdict(tuple)
            for temp_dict in cursors2:
                for sid in temp_dict:
                    all_song_lyr_dict[sid]+=temp_dict[sid]
                        
            if len(left_common_sid)>0:
            # 当只有部分词或单个词在同一行时
                #s = time.time()
                left_common_dict = most_common_lyric_search(cursors2,left_common_sid,all_song_lyr_dict)
                #p = time.time()
                #print(p-s)
                
            #所有的词都存在同一首歌 找是否有相同的歌词？：
            #取common_songid以及里面的common歌词id

            # 搜的词在同一首歌的歌曲大于n:
            if len(common_song_id) >= number_results:
                # 搜的词在同一行的歌曲大于n
                if len(common_dict.keys()) >= number_results:
                    case = 1
                    return case, common_dict, {},[],term_not_found_ind
                # 搜的词在同一行的歌曲小于n
                elif len(common_dict.keys()) < number_results:
                    case = 2
                    return case, common_dict, left_common_dict,[],term_not_found_ind  

            #3、搜的词在同一首歌的歌曲就小于n了   
            elif len(common_song_id) < number_results:
                # 先把common_dict, left_common_dict拿过来，再找most_common_song
                case = 3
                # 还需要返回的结果数量
                left_num_result=number_results-len(common_song_id)

                # 找出现词数最多的歌曲，按出现词数分类返回成一个字典(已去除所有词在同首歌的情况)
                # most_common_song_dict: {出现的词数：[歌曲ID]} 
                most_common_song = most_common_song_search(cursors2)

                # song_lyrics_list is a list of dictionary, each dict corresponds to 
                # different max number of common terms in a song 
                song_lyrics_list=[]
                # count_list：出现在同一首歌的最大词数 e.g.[3,2,1]
                count_list=sorted(list(most_common_song.keys()),reverse=True)
                
                #s=time.time()
                        
                song_lyrics_list=[]
                for count in count_list:
                    max_count_dict=defaultdict(dict)    
                    for sid in most_common_song[count]:
                        lyric_tup=all_song_lyr_dict[sid]
                        lyrics_term_count=Counter(lyric_tup).most_common()
                        max_count=lyrics_term_count[0][1]
                        lid_list=[k for k,v in dict(lyrics_term_count).items() if v == max_count]
                        max_count_dict[max_count][sid]=lid_list   
                    song_lyrics_list.append(max_count_dict) 
                    
                    if len(most_common_song[count]) >= left_num_result:
                        # 若已达到需要返回的结果数量，则break
                        break
                    else:
                        left_num_result-=len(most_common_song[count])
                        
                #p=time.time()
                #print(p-s)
                
                return case, common_dict, left_common_dict,song_lyrics_list,term_not_found_ind    
            
            


# In[8]:


# ## Advance search

def advance_output(query_advance,this_search_name):
    # 看看搜的是那一项
    number_results=20
    search_terms,raw_term = query_preprossing(query_advance)
    
    if len(search_terms)==0:
        outputs=defaultdict(list)
        outp=popularity.output()  
        outputs['results']=outp.output_list[:number_results]
        artist_filter=result_filter(outputs['results'],'artist_name')
        outputs['artist_name'].append(artist_filter)
        album_filter=result_filter(outputs['results'],'album_name')
        outputs['album_name'].append(album_filter)
        return dict(outputs),[]
        
    else:
        search_terms = search_terms[0:10]
    
        case,res_id,term_not_found_ind,res_exact= advance_search(this_search_name,search_terms,number_results)
        outputs=defaultdict(list)

        if case==0:
            if len(res_exact) == 0:#搜出来了但歌词为空 用推荐的
                outp=popularity.output() 
                outputs['results']=outp.output_list[:number_results]
                artist_filter=result_filter(outputs['results'],'artist_name')
                outputs['artist_name'].append(artist_filter)
                album_filter=result_filter(outputs['results'],'album_name')
                outputs['album_name'].append(album_filter)
            else:#正常情况
                outputs['results']=res_exact
            output_info=[]
        

        elif case==1:#模糊搜索
            if len(res_id) > 0:
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

            elif len(res_id) == 0: #啥都搜不出来 用写死的歌单
                outp=popularity.output() 
                outputs['results']=outp.output_list[:number_results]
                artist_filter=result_filter(outputs['results'],'artist_name')
                outputs['artist_name'].append(artist_filter)
                album_filter=result_filter(outputs['results'],'album_name')
                outputs['album_name'].append(album_filter)
        

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
    #这个时候 search_term可能是多个可能是单个
    
    # 把数据库搜不到的词的index存起来
    term_not_found_ind=[]
    
    #先精确搜索
    #假设有结果 有几个输出几个 按照popularity来排序：
    res_id = []        
    
    
    popularity_dic={} # {songid:popularity}
    songid_exact_list = []                
    exact_search_cursors =  songs_info.find({this_search_name:search_terms})
    res_exact=[]
    
    try:
         # 看能否搜得到，搜不到会报Index Error
        exact_search_cursors[0]
    except:
        # 精确搜索完全不出来：模糊搜索
        
        #inv_ind_songname {term: [songid1,songid2,...]}
        #inv_ind_artist {term: {'artist1':[sid1,sid2,...]}}
        #inv_ind_album {term: {'album1':[sid1,sid2,...]}}

        
        case = 1 #模糊
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
                    # 从出现次数最多交集最多的开始往下收集,最后输出的结果数量小于等于number_results

                # sorted the key of count_dict
                count_list=sorted(list(count_dict.keys()),reverse=True) 
                # find the number of dict for each key in count_list
                songid_count=[len(count_dict[i]) for i in count_list]
                for i,c in enumerate(songid_count):
                    count_popu_dict=count_dict[count_list[i]]
                    res_id+=ranked_advance_search(count_popu_dict,number_results)
                    if len(res_id) >= number_results:
                        break

            else: #模糊搜索也完全搜不出,按popularity
                res_id = []

                    
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
                    
                    #收集包含这个term的整个term的list
                    #所有term的list合在一起
                    name_keys=list(term_dict[datatype].keys())
                    name_list+=name_keys
                    for name in name_keys:
                        name_dict[name]=term_dict[datatype][name]
                        #songid+pop的字典
                        
                except:
                    term_not_found_ind.append(ind)
            
            
            if len(name_list)>0: #搜到了东西
                count_name=Counter(name_list).most_common()
                for name,count in count_name:                
                    count_dict[count].append(name)
                    # 从出现次数最多交集最多的开始往下收集,最后输出的结果数量小于等于number_results

                # sorted the key of count_dict
                # 从大到小的出现次数顺序list
                count_list=sorted(list(count_dict.keys()),reverse=True) 
                
                for i in count_list:
                    sid_popu_dict={}
                    # name是包含这个term的name
                    for name in count_dict[i]:
                        # 对于每个出现次数为i的term来说 把他的songid和pop存进dict
                        name_sid_popu_dict=name_dict[name]
                        for sid in name_sid_popu_dict.keys():
                            sid_popu_dict[sid]=name_sid_popu_dict[sid]
                    res_id+=ranked_advance_search(sid_popu_dict,number_results) 
                    if len(res_id)>number_results:
                        break
            elif len(name_list)==0:
                res_id = []

        return case,res_id,term_not_found_ind,res_exact
    
    else:
        #精确搜索
        case=0
        #精确搜索搜出来一个 但是全都木有歌词数据

        for exact_song_dict in exact_search_cursors:
            try:
                exact_song_dict.pop('_id')
                lyrics_list = list(exact_song_dict['lyrics'][0].values())
                exact_song_dict['all_lyrics']=lyrics_list
                exact_song_dict['mark_lyric']=lyrics_list[0]
                exact_song_dict.pop('lyrics')
                res_exact.append(exact_song_dict)
            except:
                pass
        return case,[],[],res_exact

def ranked_advance_search(popularity_dic,number_results):
    #返回songs id的前几个
    result_ids = [item[0] for item in get_top(popularity_dic,number_results)] 
    return result_ids 


# In[18]:

# 歌词搜索

# #case1
# raw_text='creep you' #15s

# #case2
# raw_text='creep you out' #12.8s

# #case3
# raw_text='black pain see sweet call' # 10s

# #case4
# raw_text='gucci Saffronia' #2.9s

# #case5
# raw_text='creep abcdos' #只有一个在数据库 3.9s
# #raw_text='creep' #只有一个词 3.88s

#case6
# raw_text='abcdos' #3s
# #raw_text='phrasesea, abcdos' #3s

s=time.time()
raw_text='black pain see sweet call'
search_type = 'lyrics'
#search_type = 'artist_name_preprocess'
output,info = search_result(raw_text, search_type)
e=time.time()

print(e-s)


# In[ ]:

import time
s=time.time()

# #raw_text='phrasesea, abcdos'
# raw_text='Share Your Love With Little Prayer'
# #raw_text='wild wind four woman'
#raw_text='Basement Jaxx'
raw_text='h'

#search_type = 'artist_name_preprocess'
#search_type = 'album_name_preprocess'
search_type = 'song_name_preprocess'
#search_type = 'lyrics'
output,info=search_result(raw_text,search_type)
e=time.time()
e-s

