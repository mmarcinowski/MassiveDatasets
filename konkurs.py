# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:57:14 2017

@author: Maks
"""

import numpy as np
import matplotlib.pyplot as plt

views = np.matrix([0.160,0.298,0.264,0.198,0.079])
replies = np.matrix([0.869,0.084,0.035,0.008,0.003])
sold = np.matrix([0.963,0.037])
vrprob = np.matrix([[0,1,2,3,4],[1,0,1,2,3],[2,1,0,1,2],[3,2,1,0,1],[4,3,2,1,0]])
sprob = np.matrix([[0,1],[1,0]])

result = []
x = []
y = []

for i in range(0,100):
    r= (1-i/100)/4
    if(r<(i/100)):
        vector = np.matrix([r,i/100,r,r,r]).transpose()
        y.append(np.argmin(vrprob*vector))
        x.append(i)
    
views_cost = views*vrprob
replies_cost = replies*vrprob
sold_cost = sold*sprob

plt.scatter(x,y)
plt.show()
#print(np.argmin(views_cost))
#print(np.argmin(replies_cost))
#print(np.argmin(sold_cost))

