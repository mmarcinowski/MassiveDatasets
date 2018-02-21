# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 11:37:02 2017

@author: Maks
"""

import psycopg2
import pandas as pd
import json
#Ranking popularności piosenek,

#Ranking użytkowników ze względu na największą liczbę odsłuchanych
#unikalnych utworów,

#Artysta z największą liczbą odsłuchań,

#Sumaryczna liczba odsłuchań w podziale na poszczególne miesiące,

#Wszyscy użytkownicy, którzy odsłuchali wszystkie trzy najbardziej po-
#pularne piosenki zespołu Queen.

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE dates (
                timestamp VARCHAR(255) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE artists (
                artist_id SERIAL PRIMARY KEY,
                artist_name VARCHAR(255)
        )
        """,
        """
        CREATE TABLE songs (
                song_id VARCHAR(255) PRIMARY KEY,
                release_id VARCHAR(255) NOT NULL,
                artist_id INTEGER NOT NULL,
                song_title VARCHAR(255) NOT NULL,
                FOREIGN KEY (artist_id)
                    REFERENCES artists (artist_id)
        )
        """,
        """
        CREATE TABLE users (
                user_id VARCHAR(255) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE listenings (
                user_id VARCHAR(255) NOT NULL,
                release_id VARCHAR(255) NOT NULL,
                timestamp VARCHAR(255) NOT NULL,
                
                PRIMARY KEY (user_id, release_id, timestamp),
                FOREIGN KEY (user_id)
                    REFERENCES users (user_id),
                FOREIGN KEY (release_id)
                    REFERENCES songs (release_id),
                FOREIGN KEY (timestamp)
                    REFERENCES dates (timestamp)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        #params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect("dbname=edwdBase user=postgres password=root")
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("Tables created")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
def insert_data():
    dates = """INSERT INTO dates(timestamp)
             VALUES(%s);"""
    artists = """INSERT INTO artists(artist_name)
             VALUES(%s);""" 
    songs = """INSERT INTO songs(release_id,song_id,artist_id,song_title)
             VALUES(%s,%s,%s,%s);"""
    users = """INSERT INTO users(user_id)
             VALUES(%s);"""
    listenings = """INSERT INTO listenings(user_id,release_id,timestamp)
             VALUES(%s,%s,%s);"""
    search_artists = """SELECT artist_id FROM artists WHERE artist_name=%s"""
    
    unique_tracks = pd.read_csv('unique_tracks.txt', names=['song_id','release_id','artist_name','song_title'],encoding='utf-8')
    triplets_sample = pd.read_csv('triplets_sample_20p.txt', names=['user_id','release_id','timestamp'],encoding='utf-8')
    
    artist_id_list = []
    
    #print(list(set(unique_tracks['song_id'].tolist())))
    #print(triplets_sample['timestamp'].tolist())
    conn = None
    #print(len(list(set(unique_tracks['artist_name'].tolist()))))
    try:
        conn = psycopg2.connect("dbname=edwdBase user=postgres password=root")
        # create a new cursor
        cur = conn.cursor()
        
        print("start copying")
        # execute the INSERT statement
        for i in list(set(triplets_sample['timestamp'].tolist())):
            cur.execute(dates,(i,))
        print("Dates added")
        conn.commit()
        
        for i in list(set(unique_tracks['artist_name'].tolist())):
            cur.execute(artists,(i[:255],))
            #conn.commit()
        print("Artists added")
        conn.commit()
        
        for i in unique_tracks['artist_name'].tolist():
            cur.execute(search_artists,(i[:255],))
            record = cur.fetchone()
            #print(record[0])
            artist_id_list.append(record[0])
        print("Artist list made")
        #with open('artist_list.json', 'w') as file:
        #    json.dumps(artist_id_list,file)  
        
        for i in list(set(triplets_sample['user_id'].tolist())):
            cur.execute(users,(i,))
        print("Users added")
        conn.commit()
        
        #json_data=open('artist_list.json').read()
        #artist_id_list = json.loads(json_data)
        
        for i,j,k,l in zip(unique_tracks['release_id'].tolist(),unique_tracks['song_id'].tolist(),artist_id_list,unique_tracks['song_title'].tolist()):
            cur.execute(songs,(i,j,k,l))
        print("Songs added")
        conn.commit()
        
        for i,j,k in zip(triplets_sample['user_id'].tolist(),triplets_sample['release_id'].tolist(),triplets_sample['timestamp'].tolist()):
            cur.execute(listenings,(i,j,k))
        print("Listenings added")
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error,error.args)
    finally:
        if conn is not None:
            conn.close()

 
if __name__ == '__main__':
    #create_tables()
    insert_data()