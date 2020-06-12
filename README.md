The Project consists of putting into practice the following concepts: 
1. Data Modeling with Postgres
2. Implementing star schema to create 1 fact table(songplays) and 4 dimension tables(songs, users, time, artists)
3. Build ETL pipeline with python to load the data in database.

Database Schema Design

The Schema used in this project is the Star schema with 1 fact table and 4 dimension tables, each with a primary key that is referenced from fact table.

Fact Table 

songplays: records in log data associated with song plays i.e. records with page NextSong

* songplay_id int PRIMARY KEY : ID for each songplay record
* start_time timestamp NOT NULL : start time (timestamp) of user activity
* user_id int NOT NULL : ID of user 
* level text : paid level or free level
* song_id text : ID of song
* artist_id text : ID of artist
* session_id text : ID of user session
* location text : User location
* user_agent text : Agent used by the user to access Sparkify Platform.

Dimension Tables

users: records user details in the system

* user_id int PRIMARY KEY : ID of user
* first_name text : user's first name
* last_name text : user's last name
* gender text : user's gender
* level text : paid level or free level

songs: records song details in the system

* song_id text PRiMARY KEY : ID of song
* title text : title of song
* artist_id text : ID of artist of the song
* year int : Year of song release
* duration float : Song duration in milliseconds

artists: records artist details

* artist_id text PRIMARY KEY : ID of artist
* name text : Name of artist
* location text : Location of artist
* latitude decimal : Latitude location of artist
* longitude decimal : Longitude location of artist

time:timestamps of records in songplays broken down into specific units

* start_time timestamp PRIMARY KEY : start time (timestamp) of user activity
* hour int : Hour extracted from timestamp
* day int : Day extracted from timestamp
* week int : Week extracted from timestamp
* month int : Month extracted from timestamp
* year int : Year extracted from timestamp
* weekday text : Weekday extracted from timestamp

Files used on the project:
1. data folder consists of all the jsons file which is processed and inserted in database. It consists of 2 subdirectories namely 'song_data' and 'log_data'

2. sql_queries.py consists of all the sql queries which is used by other python scripts. 

3. create_tables.py drops and creates tables. Run this file to reset the tables before running the ETL scripts.

4. test.ipynb displays the first few rows of each table to let you check the database.

5. etl.ipynb reads and processes a single file from song_data and log_data and loads the data into the tables.

6. etl.py reads and processes json files from song_data and log_data and loads them into the tables.

7. README.md current file, provides summary of my project.


Steps followed: 
1. Wrote DROP, CREATE and INSERT query statements in sql_queries.py

2. Run in terminal the following command to create the sparkify database and create all the tables.
    -> python create_tables.py
3. Used test.ipynb Jupyter Notebook to interactively verify the creation of tables.

4. Followed the instruction in the etl.ipynb Notebook and data modeling techniques to create the pipeline and insert all the data into the tables.

5. Verified with test.ipynb file. Once verified, completed the etl.py file.

6. Run etl in console, and verify results:
    -> python etl.py

ETL pipeline:

Database and tables created before starting the etl script

1. We start etl.py by executing commands to connect to sparkify database.

2. Then we start processing all song related data. We iterate over all files under /data/song_data, we store all the files with .json extension in a list.

3. We iterate over this list and send each json file to a function called process_song_file.

4. Here we load the file as a dataframe using a pandas function called read_json().

5. We extract the song_data and the artist_data to be inserted in songs and artists table respectively.

6. For songs_data we extract the fields : song_data = [song_id, title, artist_id, year, duration]

7. For artist_data we extract the fields : artist_data = [artist_id, name, location, latitude, longitude]

8. And finally we insert this data into their respective tables.

9. After processing song_data, we move on to processing log_data.

10. The json files are extracted as in Step 2. But it is now send to function process_log_file.

11. We load the data into dataframe and we filter rows where page = 'NextSong'.

12. We convert ts column to start_time as timestamp in milliseconds to datetime format. We use th builtin function of pandas datetime to extract (hour, day, week, etc.) and insert everything to time dimension table.

13. Next we extract user information such as (userId, first_name, last_name, etc) and insert into users table.

14. Finally we lookup song_id and artist_id from their tables based on the title, artist name, and duration of a song. The query for this is: 

song_select = ("""SELECT songs.song_id, artists.artist_id 
                  FROM songs JOIN artists
                  ON songs.artist_id = artists.artist_id
                  WHERE songs.title = %s
                  AND artists.name = %s
                  AND songs.duration = %s;
                  
""")

15. Lastly, we insert all the data as we need into the song_play Fact table.

Purpose of this database for startup Sparkify: 

1. The startup sparkify wants to analyze user data and the songs they are listening to. 

2. The data is available in the json format and it's not very big so data modeling with postgres is suitable. 

3. For analysis star schema is the ideal option which contains a fact table for easy analysis. 

4. We have created a fact table with name song_play which consist of references from song_id, user_id, artist_id thus helps in analysis for which user is streaming which song. 

Output for songplay: 

As we are provided a subset of the entire database, there is only 1 row in song_play table currently which has not null values for song_id and artists_id. 

I executed the following query to find out this value: 

%sql SELECT * FROM songplays JOIN songs ON songplays.song_id = songs.song_id WHERE songplays.song_id IS NOT NULL;

The result is: 
Title of the song : Setanta matins
Song id : SOZCTXZ12AB0182364
Artist id : AR5KOSW1187FB35FF4







