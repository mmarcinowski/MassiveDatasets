import pandas as pd
import itertools
import numpy as np
# song_id,user_id

data = pd.read_csv("facts.csv", usecols=[0,1], header=0)
#data = data.drop_duplicates()

data = data.groupby('user_id')['song_id'].apply(list)

result = {}

print(" Jaccard start")

def jaccard(a, b):
    c = list(set(a).intersection(b))
    return float(len(c)) / (len(a) + len(b) - len(c))

for a, b in itertools.combinations(data.items(), 2):
  a_id = a[0]
  b_id = b[0]

  a_songs = a[1]
  b_songs = b[1]

  jaccard_value =  jaccard(a_songs, b_songs)

  if(a_id not in result):
    result[a_id] = [(b_id, jaccard_value)]
  else:
    result[a_id].append((b_id, jaccard_value))

with open('result.txt', 'w') as file:
  for key in result:
    file.write('User: ' + key + "\n")
    for value in result[key]:
      file.write(value[0] + ": " + value[1] + "\n")

    file.write("\n")
    file.write("\n")
file.close()

