#!/usr/bin/env python
# coding: utf-8

# In[1]:


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



from pymongo import MongoClient
import certifi


#client = MongoClient(host='localhost',port=27017)
client = MongoClient("mongodb+srv://TTDS:ttdscw3@ttdscluster.zsdaj.mongodb.net/test", tlsCAFile=certifi.where())
db = client.songs   # The database on mongodb


songs_info=db.songs_info


from collections import defaultdict
from bson.objectid import ObjectId


# In[4]:


class output:
    res_id = [209419,310125,308772,204200,311258,217207,165570,165572,358852,6491,318733,
                      99478,345534,5030,165541,116832,253636,285393,83942,27092,188910,170695,116953,336113,
              168817,307219,253622,165535,310129,168815,13702,328238,418,351425,310124,209420,165540,365100,
              239329,230216,37988,326620,220890,168814,165534,267436,365111,132681,4242,37985]
        
    
    output_list=[]
    for song_id in res_id: 
        song_output={}
        song_output = songs_info.find({'song_id':int(song_id)})[0]
        song_output.pop('_id')
        lyrics_list=list(song_output['lyrics'][0].values())
        song_output['all_lyrics']=lyrics_list
        song_output['mark_lyric']=lyrics_list[0] #取第一句   
        song_output.pop('lyrics')
        output_list.append(song_output)
        
    def _init_(self):
        self.output_list=output_list
        
    
    
# In[ ]:





# In[ ]:




