# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:20:31 2017

@author: Maks
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier


def generate_points(n,w0,w1,w2):
    x1 = []
    x2 = []
    y = []
    c = []
    for i in range(n):
        a = np.random.uniform(-1,1)
        b = np.random.uniform(-1,1)
        x1.append(a)
        x2.append(b)
        #X = np.append(X,[a,b])
        #x2.append(b)
        v = np.sign(w1*a+w2*b+w0)
        #v = np.sign(np.power((a-w1),2)+np.power((b-w2),2)-w0)
        y.append(v)
        if(v<0): 
            c.append("r")
        else:
            c.append("b") 
    return x1, x2, y, n


def make_grid(x1,x2,y,n):
    X = np.array([x1,x2])
    Y = np.array([y])
    X = np.transpose(X)
    Y = np.transpose(Y)
    
    print(X.shape)
    print(Y.shape)
    

    x1_min, x1_max = X[:,0].min()-0.2, X[:,0].max()+0.2
    x2_min, x2_max = X[:,1].min()-0.2, X[:,1].max()+0.2
    
    xx, yy = np.meshgrid(np.arange(x1_min, x1_max,(x1_max-x1_min)/n),
                     np.arange(x2_min, x2_max,(x2_max-x2_min)/n))
    return X,Y,xx,yy

def plot_contours(ax, clf, xx, yy):
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    out = ax.contourf(xx, yy, Z,  cmap=plt.cm.coolwarm, alpha = 0.6)
    return out    

w0 = 1
w1 = 1
w2 = 1
x1, x2, y, n = generate_points(1000,w0,w1,w2)
X,Y,xx,yy = make_grid(x1, x2, y, n)
    
models = [DecisionTreeClassifier(), KNeighborsClassifier(), LogisticRegression(), GaussianNB()] 
models = [clf.fit(X, Y) for clf in models]
titles = ['DecisionTree', 'KNN','LogisticRegression','GaussianNB']    
fig, sub = plt.subplots(2, 2)
plt.subplots_adjust(wspace=0.4, hspace=0.4)       
    # Z = clf1.predict(np.c_[xx.ravel(), yy.ravel()])
    #Z = Z.reshape(xx.shape)
    
    #plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha = 0.6)
    #plt.pcolormesh(xx, yy, Z, alpha=0.4)
for clf, title, ax in zip(models, titles, sub.flatten()):
    plot_contours(ax, clf, xx, yy)
    ax.scatter(X[:, 0], X[:, 1], c=y, alpha=0.4, s=20, cmap=plt.cm.coolwarm)
    ax.set_title(title)

plt.savefig("decision_boundary2.png",dpi=600)
plt.show()      