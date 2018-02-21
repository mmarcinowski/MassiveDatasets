'''
Author: Kalina Jasinska
'''

from plot_learning_curve import evaluate_accuracy_and_time
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from utils.evaluate import scorer_squared_error, scorer_01loss
from utils.load import read_datasets
from naive_bayes import NaiveBayesBoth
#import time
import numpy as np
import matplotlib.pyplot as plt
# Implement plotting of a learning curve using sklearn
# Remember that the evaluation metrics to plot are 0/1 loss and squared error


datasets = [('data/badges2-train.csv', 'data/badges2-test.csv',  "Badges2"),
            ('data/credit-a-train.csv','data/credit-a-test.csv', "Credit-a"),
            ('data/credit-a-mod-train.csv','data/credit-a-mod-test.csv', "Credit-a-mod"),
            ('data/spambase-train.csv', 'data/spambase-test.csv', "Spambase")]
titles_list=["Time of proceeding","Train 0-1 loss","Test 0-1 loss","Train squared error","Test squared error"]

def evaluate_classifier(estimator,dataset,n,m): 
    #m - liczba częsci na które ma być podzielony plik, n - liczba częsci które bierzemy pod uwagę,
    # czyli analizujemy n/m rozmiaru pliku
    
    fn, fn_test, ds_name = dataset
    #print("Dataset {0}".format(ds_name))
    X_train, y_train, X_test, y_test, is_categorical = read_datasets(fn, fn_test)
    a = int(len(X_train)*n*(1/m))
    #print(X_train[:a])
    return evaluate_accuracy_and_time(estimator, X_train[:a], y_train[:a], X_test, y_test)

def make_learning_curves():
    results={}
    datasets_names = []

    classifiers_list = [GaussianNB(),KNeighborsClassifier(),LogisticRegression()]
    
#=============================================================================
#Zebranie wyników dla wszystkich klasyfikatorów analizujących po kolei całosc kolejnych zbiorów. 
#
#Każda pozycja w słowniku wygląda następująco:
#{nazwa_klasyfikatora:[[lista_wyników_czasowych],[lista train 0/1 loss],[lista test 0/1 loss],[lista train squared error],[lista test squared error]}
#(czyli każda z wymienionych podlist jest 4-elementowa, bo są 4 zbiory danych)
    
    for j in range(len(datasets)):
        print(datasets[j][0])
        datasets_names.append(datasets[j][2])
        for i in classifiers_list:
            a = str(i)[:10]
            x= evaluate_classifier(i,datasets[j],1,1) #bierzemy całosć pliku czyli 1/1
            if(a not in results):
                results.update({a:[[x[0]],
                                   [x[1][0]],
                                   [x[1][1]],
                                   [x[1][2]],
                                   [x[1][3]]
                                  ]})
            else:
                results[a][0].append(x[0])
                results[a][1].append(x[1][0])
                results[a][2].append(x[1][1])
                results[a][3].append(x[1][2])
                results[a][4].append(x[1][3])

    #print(results)
    
#Wyswietlenie wyników na wykresach: x - zbiory danych, y - wartosci czasu/błędu, serie - każdy z klasyfikatorów
    for i in range(len(titles_list)):
        for k,v in results.items():
            plt.plot(range(len(datasets_names)), v[i], label=k)
        plt.title(titles_list[i])
        plt.xticks(range(len(datasets_names)),datasets_names,rotation=90) 
        plt.legend(loc="best")
        plt.savefig(titles_list[i]+".png",dpi=800)
        plt.show()
    
#===========================================================================  
    
    
    
#=============================================================================
# Analiza każdego zbioru danych przez każdy klasyfikator dla rosnących częsci pliku
#
#Każda pozycja w słowniku wygląda następująco:
#{nazwa_klasyfikatora:[[lista_wyników_czasowych],[lista train 0/1 loss],[lista test 0/1 loss],[lista train squared error],[lista test squared error]}
#(czyli każda z wymienionych podlist jest n-elementowa, bo analizowanych jest n podzbiorów danego zbioru danych)    
    m = 75
    for j in range(len(datasets)):
        results.clear()
        for i in classifiers_list:
            for n in range(1,m+1): #wykonywane jest m iteracji
                a = str(i)[:10]
                x= evaluate_classifier(i,datasets[2],n,m) #plik jest podzielony na m częsci
        
                if(a not in results):
                    results.update({a:[[x[0]],
                                       [x[1][0]],
                                       [x[1][1]],
                                       [x[1][2]],
                                       [x[1][3]]
                                      ]})
                else:
                    results[a][0].append(x[0])
                    results[a][1].append(x[1][0])
                    results[a][2].append(x[1][1])
                    results[a][3].append(x[1][2])
                    results[a][4].append(x[1][3])
                    
#Wyswietlenie wyników na wykresach: x - częsc zbioru danych(0.1, 0.2 ...), y - wartosci czasu/błędu, serie - każdy z klasyfikatorów    
        z = np.linspace(1/m,1,num=m)
        for l in range(len(titles_list)):
            for k,v in results.items():
                plt.plot(z, v[l], label=k)
            plt.title(titles_list[l]+datasets_names[j])
            plt.xticks(z, rotation=90) 
            plt.legend(loc="best")
            plt.savefig(titles_list[l]+datasets_names[j]+"Growing"+".png",dpi=800)
            plt.show()
#=============================================================================    

if __name__ == "__main__":
    #evaluate_classifer()
    make_learning_curves()