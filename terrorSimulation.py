# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 16:56:54 2017

@author: Maks
"""
import matplotlib.pyplot as plt
import numpy as np
import time

#n = int(input("Give number of people"))
#h = int(input("Give number of hotels"))
#p = float(input("Give probability of spending night in hotel"))
#d = int(input("Give number of days"))
#returns how many pairs spend the same night in the same hotel more than once

n = 10000
h = 100
p = 0.01
d = 1000

pairs_dict = {}
days_hotels_dict = {}
histogram_dict = {}
dangerous_people = []
dangerous_pairs_number = 0
elements = 0


for i in range(d):
    for j in range(n):
        do_I_choose = np.random.random_sample()
        if do_I_choose>p:
            continue
        else:
            hotel = np.random.randint(0,h)
            if (i,hotel) not in days_hotels_dict:
                days_hotels_dict.update({(i,hotel):[j]})
            else:
                days_hotels_dict[(i,hotel)].append(j)

print("List ready")

#for i in days_hotels_dict.values():
#    elements = elements + len(i) 
#print(elements)

start=time.clock()

for k,v in days_hotels_dict.items():
    for l in v:
        for m in v:
            if l!=m:
                if (l,m) in pairs_dict and k[0] not in pairs_dict[(l,m)][1]:
                    pairs_dict[(l,m)][0]+=1
                    pairs_dict[(l,m)][1].append(k[0])
                elif (m,l) in pairs_dict and k[0] not in pairs_dict[(m,l)][1]:
                    pairs_dict[(m,l)][0]+=1
                    pairs_dict[(m,l)][1].append(k[0])
                elif (l,m) not in pairs_dict and (m,l) not in pairs_dict:
                    pairs_dict.update({(l,m):[1,[k[0]]]})
            else:
                continue

end=time.clock()

for key,value in pairs_dict.items():
    if value[0]>=2:
        dangerous_pairs_number+=1
        dangerous_people.append(key[0])
        dangerous_people.append(key[1])


for k,v in pairs_dict.items():
    if(v[0]==1):
        continue
    elif(v[0] not in histogram_dict.keys()):
        histogram_dict.update({v[0]:1})
    else:
        histogram_dict[v[0]]+=1

x = list(histogram_dict.keys())
y = list(histogram_dict.values())

f = open('log', 'w')
for k,v in days_hotels_dict.items():
    f.writelines([str(k),str(v),"\n"])
f.close()

print("Dangerous pairs:",dangerous_pairs_number)
print("Dangerous people:",len(set(dangerous_people)))
print("Time:",end-start)
print("Meetings:",y)

plt.xticks(x)
plt.bar(x,y)
plt.title("Histogram of dangerous pairs' meetings number")
plt.show()