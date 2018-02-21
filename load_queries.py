import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import operator

max_days = 5
data_dir = "C:/Users/Maks/Documents/Python Projects/EDWD+PED/OLXdata/search_queries/"

index_query = 0
index_category = 1
index_count = 2
whole_sum = 0

day_names = []
daily_queries = []
col_names = ["query", "category", "count"]
categories_freq = {}
words_freq = {}
best_words = []
month_queries=[]
month_freq_queries=[]
month="start"
sorted_freq=[]
months=[]
queries_in_months = {}
queries_in_days = {}

def convert_query(a):
    if a is None:
        return ""
    return str(a.strip('"'))

def convert_category(a):
    if a is None:
        return -1
    a = a.strip('"')
    a = a.strip(',')
    a = a.strip('"')
    return a
    #return int(a)

def convert_count(a):
    if a is None:
        return 0
    a = a.strip('"')
    a = a.strip(',')
    a = a.strip('"')
    return int(a)

converters = {index_query:convert_query, index_category:convert_category, index_count: convert_count}

#różne wzroce tygodniowe dla różnych kategorii/zapytań
#zliczenie liczby wyszukań dla każdej kategorii / zapytania - histogram lub spis
#pierwsza data wystąpienia zapytania
#trendy wyszukań w sezonach/miesiącach

#histogram wywietlający ile sposród 10% najpopularniejszych typów wyszukań jest wyszukiwane najczęsciej w danym miesiącu i dniu tygodnia


for file_index, file_name in enumerate(os.listdir(data_dir)):
    #if("2016" in file_name):    
        if file_index < max_days:
            p = os.path.join(data_dir, file_name)
            queries = pd.read_csv(p,delimiter='","', engine="python", header =0, names = col_names, quotechar='"',
                                   converters=converters)
            
            file_name = file_name.split(".")[0]
            day = file_name.split("s_")[1]
            newmonth = int(file_name.split("_")[3])
            if(month!=newmonth and month!="start"):
                month_queries.append(whole_sum)
                whole_sum=0
                months.append(month)
            whole_sum+= sum(queries["count"])
            
            
            #for i,row in enumerate(queries.values):
            #    a = row[0]
            #    b = row[1]
            #    c = row[2]
            #    if(str(a)!="nan" and len(str(a))>2 and c>10):
            #        if(a not in words_freq):
            #            words_freq.update({a:c})
            #        else:
            #            words_freq[a]+=c
            
            #month = int(file_name.split("_")[3])
            print(file_index,"done",file_name)
            
            
            
#print(words_freq)
#print(max(words_freq,key=words_freq.get))
#sorted_freq = sorted(words_freq.items(), key=operator.itemgetter(1))
#z = pd.DataFrame(sorted_freq)
#z.to_csv("sorted_freq2.csv",header=["query","freq"])
#print(sorted_freq)
#print(month_queries)
#for i in range(int(0.9*len(sorted_freq)),len(sorted_freq)):
#    best_words.append(sorted_freq[i][0])

most_frequent = pd.read_csv("most_freq.csv",delimiter=',', engine="python", header=0)
#print(most_frequent)
most_frequent_list = []
for i,row in enumerate(most_frequent.values):
    a = row[0]
    b = row[1]
    c = row[2]
    most_frequent_list.append(b)
    
freq_sum = 0    
for file_index, file_name in enumerate(os.listdir(data_dir)):
    if file_index < max_days:
            p = os.path.join(data_dir, file_name)
            queries = pd.read_csv(p,delimiter='","', engine="python", header =0, names = col_names, quotechar='"',
                                   converters=converters)
            for i,row in enumerate(queries.values):
                a = row[0]
                b = row[1]
                c = row[2]
                if(a in most_frequent_list):
                    newmonth = int(file_name.split("_")[3])
                    if(month!=newmonth and month!="start"):
                        month_freq_queries.append(freq_sum)
                        freq_sum=0
                freq_sum+=c
            print(file_index,"done2",file_name)            
            #file_name = file_name.split(".")[0]
            #today = datetime.date(int(file_name.split("_")[2]), int(file_name.split("_")[3]), int(file_name.split("_")[4]))
            #day_names.append(today.strftime("%A")[:4])
            #daily_queries.append(whole_sum)

percents=[]
for i in range(len(months)):
    percents.append(month_freq_queries[i]/month_queries[i])
#print(days_dict.items())
#print(days_dict.keys())
#print(days_dict.values())    
plt.bar(range(len(months)),percents,width=0.8)
plt.xticks(range(len(months)),months,rotation=90)
plt.savefig("mostFreqPercents.png",dpi=800)
plt.show()
plt.close()          
