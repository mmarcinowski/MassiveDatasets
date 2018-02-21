# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:10:05 2018

@author: Maks
"""
import pandas as pd
import operator
import time
#from sklearn.metrics import jaccard_similarity_score

def jaccard(a,b):
    c=list(set(a).intersection(b))
    return len(c)/(len(a)+len(b)-len(c))


users = {}
pairs = {}
last_user=''
start=time.clock()
frame = pd.read_csv("facts.csv",header=0)
#first_users=[]

print("File ready")

data=frame.groupby(['user_id'])['song_id'].apply(list)
print("groupby made")
data_head = data.head(100)
for indice,line in data_head.iteritems():
    #print(indice,line)
    pairs.update({indice:{}})
    for index,row in data.iteritems():
        #print(index,row)
        pairs[indice].update({index:jaccard(line,row)})
    pairs[indice] = sorted(pairs[indice].items(),key=operator.itemgetter(1))
    print(indice)
end=time.clock()
duration=end-start
print("Pairs added")
for k,v in pairs.items():
    print(k,v[-101:])
print(duration)
    
