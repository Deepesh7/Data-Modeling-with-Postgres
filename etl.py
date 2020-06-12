import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''Function reads the json file in data/song_data directory and inserts artist record and song record
    
        Input: 
            cur: It is the cursor object used to execute the query on the database
            filepath: It is path of a json file in the directory data/song_data
            
        Output: 
            The function has no return value'''
    df = pd.read_json(filepath, lines=True)
    
    artist_id, latitude, location, longitude, name = df.values[0][[0, 1, 2, 3, 4]]
    artist_data = [artist_id, name, location, latitude, longitude]
    cur.execute(artist_table_insert, artist_data)

    artist_id, duration, song_id, title, year = df.values[0][[0, 5, -3, -2, -1]]
    song_data = [song_id, title, artist_id, year, duration]
    cur.execute(song_table_insert, song_data)    


def process_log_file(cur, filepath):
    '''Function reads the json file in data/log_data and inserts time ,user and songplay record. To insert data          in songplay fact table, the function also performs an sql query to retrieve song_id and artist_id.
    
        Input: 
            cur: It is the cursor object used to execute the query on the database
            filepath: It is path of a json file in the directory data/log_data
            
        Output: 
            The function has no return value'''
    df = pd.read_json(filepath, lines=True)

    df = df[df['page'] == 'NextSong']

    t = pd.to_datetime(df['ts'],unit='ms')
    
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday_name)
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    
    time_df_dict = {}
    for i,c in enumerate(column_labels):
        time_df_dict[c] = time_data[i]
    
    time_df = pd.DataFrame(time_df_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].copy()

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (pd.to_datetime(row['ts'],unit='ms'), int(row['userId']), row['level'], songid,                            artistid, int(row['sessionId']), row['location'], row['userAgent'])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''The function gets all the json file in 'filepath' directory. It iterates over the files and passes it to a        fuction 'func' to extract data.
        
        Input:
            cur: It is the cursor object used to execute the query on the database
            conn: Connect object to the database. Used for commiting to the database.
            filepath: The filepath from where the function will extract all the .json files.
            func: Function which processes the files iteratively and stores in the database.
            
        Output: 
            The function has no return value'''
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()