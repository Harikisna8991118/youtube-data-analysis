from googleapiclient.discovery import build # Google API client library for Python
import pymongo # MongoDB client library for Python
import psycopg2 # PostgreSQL client library for Python
import pandas as pd # Data manipulation library
import streamlit as st # Web app framework for Python

# Function to establish a connection to the YouTube Data API

def Api_connect():
    # My API key for the YouTube Data API
    Api_id = "AIzaSyAFLIeg9WMiH5r6dcxDO9O-UzaGLJtzGxU"
    # The name of the API service I am connecting to (YouTube Data API)
    api_service_name = "youtube"
    # The version of the API I am using
    api_version = "v3"
    # Building the YouTube API client using the provided service name, version, and API key
    youtube = build(api_service_name,api_version,developerKey=Api_id)
    # Return the YouTube API client object to be used for making API requests
    return youtube
# Establish the connection to the YouTube API by calling the Api_connect function
youtube = Api_connect()

#get channel info

def get_channel_info(channel_id):
    # Create a request to get the details of the specified YouTube channel
    request = youtube.channels().list(part = "snippet,ContentDetails,statistics", id = channel_id)
    # Execute the request and store the response
    response = request.execute()
    
    # Iterate over the items in the response (although typically there will be only one item for a specific channel ID)
    for i in response['items']:
        # Create a dictionary with the relevant channel information
        data = dict(Channel_Name = i["snippet"]["title"],# Channel's title
                    Channel_Id = i["id"],# Channel's ID
                    Subscribers = i["statistics"]["subscriberCount"],# Number of subscribers
                    Views = i["statistics"]["viewCount"],# Total view count
                    Total_Videos = i["statistics"]["videoCount"],# Total number of videos
                    Channel_Description = i["snippet"]["description"], # Channel's description
                    Playlist_id = i["contentDetails"]["relatedPlaylists"]["uploads"])# Playlist ID of the channel's uploads
    # Return the dictionary containing the channel information
    return data

#get video ids
def get_videos_ids(channel_id):
    # Initialize an empty list to store video IDs
    video_ids=[]
    # Retrieve the playlist ID that contains the uploaded videos for the specified channel
    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # Initialize the token for the next page of results
    next_page_token=None

    # Loop to get all video IDs from the playlist
    while True:
        # Request a list of playlist items, specifying the part and maxResults per page
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        
        # Loop through the items in the response and extract video IDs
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        
        # Get the token for the next page, if any    
        next_page_token=response1.get('nextPageToken')

        # Break the loop if there are no more pages
        if next_page_token is None:
            break
        
    # Return the list of video IDs
    return video_ids

#get video information
def get_video_info(video_ids):
    # Initialize an empty list to store video data
    video_data=[]
    
    # Loop through each video ID to retrieve its information
    for video_id in video_ids:
        # Create a request to get details of the video with the specified ID
        request=youtube.videos().list(
            part="snippet,ContentDetails,statistics",
            id=video_id
        )
        
        # Execute the request and store the response
        response=request.execute()

        # Iterate over the items in the response (although typically there will be only one item per video ID)
        for item in response["items"]:
            
            # Create a dictionary with the relevant video information
            data=dict(Channel_Name=item['snippet']['channelTitle'],# Channel's name
                    Channel_Id=item['snippet']['channelId'],# Channel's ID
                    Video_Id=item['id'], # Video's ID
                    Title=item['snippet']['title'],# Video's title
                    Tags=item['snippet'].get('tags'),# Video's tags (if available)
                    Thumbnail=item['snippet']['thumbnails']['default']['url'],# URL of the video's thumbnail
                    Description=item['snippet'].get('description'),# Video's description (if available)
                    Published_Date=item['snippet']['publishedAt'],# Date the video was published
                    Duration=item['contentDetails']['duration'],# Duration of the video
                    Views=item['statistics'].get('viewCount'), # Number of views (if available)
                    Likes=item['statistics'].get('likeCount'),# Number of likes (if available)
                    Comments=item['statistics'].get('commentCount'),# Number of comments (if available)
                    Favorite_Count=item['statistics']['favoriteCount'],# Number of times the video was marked as favorite
                    Definition=item['contentDetails']['definition'],# Video definition (e.g., HD, SD)
                    Caption_Status=item['contentDetails']['caption']# Caption status (e.g., true, false)
                    )
            # Append the dictionary to the list of video data
            video_data.append(data)    
            
    # Return the list of video data
    return video_data

#get comments information
def get_comment_info(video_ids):
    
    # Initialize an empty list to store comment data
    Comment_data=[]
    
    try:
        # Loop through each video ID to retrieve its comments
        for video_id in video_ids:
            
            # Create a request to get the top-level comments of the video with the specified ID
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            # Execute the request and store the response
            response=request.execute()

            # Iterate over the items in the response
            for item in response['items']:
                # Create a dictionary with the relevant comment information
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],  # Comment ID
                        Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'], # Video ID the comment belongs to
                        Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'], # Text of the comment
                        Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'], # Author of the comment
                        Comment_Published=item['snippet']['topLevelComment']['snippet']['publishedAt']) # Date the comment was published
                
                # Append the dictionary to the list of comment data
                Comment_data.append(data)
                
    except: # Catch any exceptions that occur during the API request
        pass # Ignore the exception and continue
    
    # Return the list of comment data
    return Comment_data

#get_playlist_details

def get_playlist_details(channel_id):
    
        # Initialize variables
        next_page_token=None # Token for the next page of results
        All_data=[]  # List to store all playlist data
        
        # Loop to retrieve all playlists of the specified channel
        while True:
                # Create a request to get playlists of the specified channel
                request=youtube.playlists().list(
                        part='snippet,contentDetails',
                        channelId=channel_id,
                        maxResults=50, # Maximum number of playlists to retrieve per request
                        pageToken=next_page_token
                )
                # Execute the request and store the response
                response=request.execute()

                # Iterate over the items in the response
                for item in response['items']:
                        # Create a dictionary with the relevant playlist information
                        data=dict(Playlist_Id=item['id'], # Playlist ID
                                Title=item['snippet']['title'], # Playlist title
                                Channel_Id=item['snippet']['channelId'], # Channel ID the playlist belongs to
                                Channel_Name=item['snippet']['channelTitle'], # Channel name the playlist belongs to
                                PublishedAt=item['snippet']['publishedAt'], # Date the playlist was published
                                Video_Count=item['contentDetails']['itemCount']) # Number of videos in the playlist
                      
                        # Append the dictionary to the list of all playlist data
                        All_data.append(data)

                # Get the token for the next page of results, if any
                next_page_token=response.get('nextPageToken')
                
                # Break the loop if there are no more pages
                if next_page_token is None:
                        break
        
        # Return the list containing all playlist data
        return All_data
    
# Connect to the MongoDB Atlas cluster
client = pymongo.MongoClient("mongodb+srv://hariharan:Vikram123@clusters.8ow9xdk.mongodb.net/?retryWrites=true&w=majority&appName=clusters")

# Access the "Youtube_data" database within the MongoDB cluster
db = client["Youtube_data"]
 

#get the channel details
def channel_details(channel_id):
    # Retrieve channel details using the provided channel ID
    ch_details = get_channel_info(channel_id)
    
    # Retrieve playlist details for the channel
    pl_details = get_playlist_details(channel_id)
    
    # Retrieve video IDs associated with the channel
    vi_ids = get_videos_ids(channel_id)
    
    # Retrieve detailed information about each video
    vi_details = get_video_info(vi_ids)
    
    # Retrieve comments information for the videos
    com_details = get_comment_info(vi_ids)
    
    # Access the "channel_details" collection in the MongoDB database
    coll1=db["channel_details"]
    
    # Insert a document containing channel, playlist, video, and comment information into the collection
    coll1.insert_one({"channel_information":ch_details,
                      "playlist_information":pl_details,
                      "video_information":vi_details,
                      "comment_information":com_details})
    
    # Return a message indicating successful upload
    return "upload completed successfully"
    
    
#Table creation for channels,playlists,videos,comments
def channel_table():
    
    # Connect to the PostgreSQL database
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Hari@05404",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()

    # Drop the channels table if it already exists
    drop_query = '''drop table if exists channels'''
    cursor.execute(drop_query)
    mydb.commit()

    # Create the channels table with relevant columns
    try:
        create_query='''create table if not exists channels(Channel_Name varchar(100),
                                                            Channel_Id varchar(80) primary key,
                                                            Subscribers bigint,
                                                            Views bigint,
                                                            Total_Videos int,
                                                            Channel_Description text,
                                                            Playlist_Id varchar(80))'''
        cursor.execute(create_query)
        mydb.commit()

    except:
        print("Channels table already created")
        
    # Access and process data from MongoDB collection    
    ch_list=[]
    db = client["Youtube_data"]
    coll1 = db["channel_details"]
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])
    df = pd.DataFrame(ch_list)

     # Insert data from each row of the DataFrame into the channels table
    for index,row in df.iterrows():
        insert_query = '''insert into channels(Channel_Name,
                                            Channel_Id,
                                            Subscribers,
                                            Views,
                                            Total_Videos,
                                            Channel_Description,
                                            Playlist_Id)
                                                            
                                            values(%s,%s,%s,%s,%s,%s,%s)'''
        values = (row['Channel_Name'],
                row['Channel_Id'],
                row['Subscribers'],
                row['Views'],
                row['Total_Videos'],
                row['Channel_Description'],
                row['Playlist_id'])
        
        try:
            cursor.execute(insert_query,values)
            mydb.commit()
            
        except:
            print("Channels values are already inserted")
                                                            

def playlist_table():
    
    # Connect to the PostgreSQL database
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Hari@05404",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()
    
    # Drop the playlists table if it already exists
    drop_query = '''drop table if exists playlists'''
    cursor.execute(drop_query)
    mydb.commit()

    # Create the playlists table with relevant columns
    try:
        create_query='''create table if not exists playlists(Playlist_Id varchar(100) primary key,
                                                            Title varchar(100),
                                                            Channel_Id varchar(100),
                                                            Channel_Name varchar(100),
                                                            PublishedAt timestamp,
                                                            Video_Count int
                                                            )'''
        cursor.execute(create_query)
        mydb.commit()

    except:
        print("Playlist table already created")
    
    # Access and process data from MongoDB collection
    pl_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
        for i in range (len(pl_data["playlist_information"])):
            pl_list.append(pl_data["playlist_information"][i])
    df1 = pd.DataFrame(pl_list)
    
    # Insert data from each row of the DataFrame into the playlists table
    for index,row in df1.iterrows():
        insert_query = '''insert into playlists(Playlist_Id,
                                               Title,
                                               Channel_Id,
                                               Channel_Name,
                                               PublishedAt,
                                               Video_Count
                                               )
                                                            
        values(%s,%s,%s,%s,%s,%s)'''
        values = (row['Playlist_Id'],
                row['Title'],
                row['Channel_Id'],
                row['Channel_Name'],
                row['PublishedAt'],
                row['Video_Count'])
        
        try:
            cursor.execute(insert_query,values)
            mydb.commit()
            
        except:
            print("Playlists values are already inserted")
            
            
def video_table():
    
    # Connect to the PostgreSQL database
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Hari@05404",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()

    # Drop the videos table if it already exists
    drop_query = '''drop table if exists videos'''
    cursor.execute(drop_query)
    mydb.commit()

    # Create the videos table with relevant columns
    try:
        create_query='''create table if not exists videos(Channel_Name varchar(100),
                                                        Channel_Id varchar(100),
                                                        Video_Id varchar(30) primary key,
                                                        Title varchar(150),
                                                        Tags text,
                                                        Thumbnail varchar(200),
                                                        Description text,
                                                        Published_Date timestamp,
                                                        Duration interval,
                                                        Views bigint,
                                                        Likes bigint,
                                                        Comments int,
                                                        Favorite_Count int,
                                                        Definition varchar(10),
                                                        Caption_Status varchar(50)
                                                            )'''
        cursor.execute(create_query)
        mydb.commit()

    except:
        print("Videos table already created")

    # Access and process data from MongoDB collection
    vd_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    for vd_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range (len(vd_data["video_information"])):
            vd_list.append(vd_data["video_information"][i])
    df2 = pd.DataFrame(vd_list)

    # Insert data from each row of the DataFrame into the videos table
    for index,row in df2.iterrows():
            insert_query = '''insert into videos(Channel_Name,
                                                        Channel_Id,
                                                        Video_Id,
                                                        Title,
                                                        Tags,
                                                        Thumbnail,
                                                        Description,
                                                        Published_Date,
                                                        Duration,
                                                        Views,
                                                        Likes,
                                                        Comments,
                                                        Favorite_Count,
                                                        Definition,
                                                        Caption_Status
                                                    )
                                                    
                                                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            values = (row['Channel_Name'],
                        row['Channel_Id'],
                        row['Video_Id'],
                        row['Title'],
                        row['Tags'],
                        row['Thumbnail'],
                        row['Description'],
                        row['Published_Date'],
                        row['Duration'],
                        row['Views'],
                        row['Likes'],
                        row['Comments'],
                        row['Favorite_Count'],
                        row['Definition'],
                        row['Caption_Status']
                        )
            
            try:
                cursor.execute(insert_query,values)
                mydb.commit()
                
            except:
                print("videos values are already inserted")


def comment_table():
    
    # Connect to the PostgreSQL database
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="Hari@05404",
                        database="youtube_data",
                        port="5432")
    cursor=mydb.cursor()
    
    # Drop the comments table if it already exists
    drop_query = '''drop table if exists comments'''
    cursor.execute(drop_query)
    mydb.commit()
    
    # Create the comments table with relevant columns
    try:
        create_query='''create table if not exists comments(Comment_Id varchar(100) primary key,
                                                            Video_Id varchar(50),
                                                            Comment_Text text,
                                                            Comment_Author varchar(150),
                                                            Comment_Published timestamp
                                                            )'''
        cursor.execute(create_query)
        mydb.commit()

    except:
        print("Comments table already created")
        
    # Access and process data from MongoDB collection    
    cd_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    for cd_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range (len(cd_data["comment_information"])):
            cd_list.append(cd_data["comment_information"][i])
    df3 = pd.DataFrame(cd_list)

    # Insert data from each row of the DataFrame into the comments table
    for index,row in df3.iterrows():
            insert_query = '''insert into comments(Comment_Id,
                                                        Video_Id,
                                                        Comment_Text,
                                                        Comment_Author,
                                                        Comment_Published
                                                    )
                                                    
                                                    values(%s,%s,%s,%s,%s)'''
                
                
            values=(row['Comment_Id'],
                        row['Video_Id'],
                        row['Comment_Text'],
                        row['Comment_Author'],
                        row['Comment_Published']
                        )
            
            try:
                cursor.execute(insert_query,values)
                mydb.commit()
                
            except:
                print("comments values are already inserted")


def tables():
    """
  This function creates all the necessary tables (channel, playlist, video, comment) 
  in a PostgreSQL database.
  """
    
    channel_table() # Create the channel table
    playlist_table() # Create the playlist table
    video_table() # Create the video table
    comment_table() # Create the comment table
    
    return "Tables created succesfully" # Return a success message

def show_channels_table():
    
    # Initialize an empty list to store channel information
    ch_list=[]
    db = client["Youtube_data"]
    coll1 = db["channel_details"]
    
    # Iterate through documents in the collection, extracting channel information
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(ch_data["channel_information"])
        
    # Create a Streamlit DataFrame from the list of channel information
    df = st.dataframe(ch_list)
    return df  # Return the DataFrame

def show_playlists_table():
    
    # Initialize an empty list to store playlist information
    pl_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    
    # Iterate through documents in the collection, extracting playlist information
    for pl_data in coll1.find({},{"_id":0,"playlist_information":1}):
        for i in range (len(pl_data["playlist_information"])):
            pl_list.append(pl_data["playlist_information"][i])
            
    # Create a Streamlit DataFrame from the list of playlist information
    df1 = st.dataframe(pl_list)
    return df1 # Return the DataFrame

def show_videos_table():
    
    # Initialize an empty list to store video information
    vd_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    
    # Iterate through documents in the collection, extracting video information
    for vd_data in coll1.find({},{"_id":0,"video_information":1}):
        for i in range (len(vd_data["video_information"])):
            vd_list.append(vd_data["video_information"][i])
            
    # Create a Streamlit DataFrame from the list of video information
    df2 = st.dataframe(vd_list)
    return df2 # Return the DataFrame

def show_comments_table():
    
    # Initialize an empty list to store comment information
    cd_list=[]
    db.client["Youtube_data"]
    coll1 = db["channel_details"]
    
    # Iterate through documents in the collection, extracting comment information
    for cd_data in coll1.find({},{"_id":0,"comment_information":1}):
        for i in range (len(cd_data["comment_information"])):
            cd_list.append(cd_data["comment_information"][i])
            
    # Create a Streamlit DataFrame from the list of comment information
    df3 = st.dataframe(cd_list)
    return df3 # Return the DataFrame

# Streamlit Part

# Title for the Streamlit app
st.title(":blue[YOUTUBE DATA HAVERSTING AND WAREHOUSING]")

# Sidebar section with project information
with st.sidebar:
    st.title(":white[GUVI's CAPSTONE:-]")
    
    # Problem statement header
    st.header(":blue[Problem Statement:]")
    
     # Explain the functionalities using markdown
    st.markdown('''The problem statement is to create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
  1. Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
  2. Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
     Option to store the data in a MYSQL or PostgreSQL.
  3. Ability to search and retrieve data from the SQL database using different search options, including joining tables to get channel details.'''
)
    # Header for results
    st.header(":blue[Result:]")
    
    # Explain the project's goals using markdown
    st.markdown('''This project aims to develop a user-friendly Streamlit application that utilizes the Google API to extract information on a YouTube channel, stores it in a SQL database, and enables users to search for channel details and join tables to view data in the Streamlit app.''')


# User input for channel ID    
channel_id = st.text_input("ENTER THE CHANNEL IDs")

# Button to collect and store data
if st.button("COLLECT AND STORE THE DATAS"):
    
    # Initialize empty list for channel IDs
    ch_ids=[]
    db=client["Youtube_data"]
    coll1 = db["channel_details"]
    
    # Iterate through existing channel details in MongoDB
    for ch_data in coll1.find({},{"_id":0,"channel_information":1}):
        ch_ids.append(ch_data["channel_information"]["Channel_Id"])
    
    # Check if entered channel ID already exists    
    if channel_id in ch_ids:
        st.success("*Alert: Channel details already exists*")
    else:
        # Assuming channel_details function is defined elsewhere, call it to collect data
        insert = channel_details(channel_id)
        st.success(insert)

# Button to migrate data to PostgreSQL tables        
if st.button("MIGRATE"):
    
    # Call the tables function to create tables
    Tables = tables()
    st.success(Tables)

# Radio button for selecting a table to view    
show_table = st.radio("SELECT THE TABLE FOR VIEW",("CHANNELS","PLAYLISTS","VIDEOS","COMMENTS"))

# Display tables based on user selection
if show_table == "CHANNELS":
    show_channels_table()
    
elif show_table == "PLAYLISTS":
    show_playlists_table()
    
elif show_table == "VIDEOS":
    show_videos_table()
    
elif show_table == "COMMENTS":
    show_comments_table()


# SQL Connections

# Connect to PostgreSQL database
mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    password="Hari@05404",
                    database="youtube_data",
                    port="5432")
cursor=mydb.cursor()

# Section for user to select a question
st.subheader(":blue[_SELECT YOUR QUESTIONs_]")
question = st.selectbox("",("1. What are the names of all the videos and their corresponding channels?",
                                              "2. Which channels have the most number of videos, and how many videos do they have?",
                                              "3. What are the top 10 most viewed videos and their respective channels?",
                                              "4. How many comments were made on each video, and what are their corresponding video names?",
                                              "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                              "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
                                              "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                              "8. What are the names of all the channels that have published videos in the year 2022?",
                                              "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                              "10. Which videos have the highest number of comments, and what are their corresponding channel names?"))

# Execute SQL queries based on user selection
if question=="1. What are the names of all the videos and their corresponding channels?":
    query1='''select title as videos,channel_name as channelname from videos'''
    cursor.execute(query1)
    mydb.commit()
    t1=cursor.fetchall()
    df=pd.DataFrame(t1,columns=["VIDEO TITLE","CHANNEL NAME"])
    st.write(df)

# ... similar logic for other questions with explanations ...

elif question=="2. Which channels have the most number of videos, and how many videos do they have?":
    query2='''select channel_name as channelname,total_videos as no_videos from channels 
                order by total_videos desc'''
    cursor.execute(query2)
    mydb.commit()
    t2=cursor.fetchall()
    df2=pd.DataFrame(t2,columns=["CHANNEL NAME","NO OF VIDEOS"])
    st.write(df2)

elif question=="3. What are the top 10 most viewed videos and their respective channels?":
    query3='''select views as views,channel_name as channelname,title as videotitle from videos 
                where views is not null order by views desc limit 10'''
    cursor.execute(query3)
    mydb.commit()
    t3=cursor.fetchall()
    df3=pd.DataFrame(t3,columns=["VIEWS","CHANNEL NAME","VIDEO TITLE"])
    st.write(df3)

elif question=="4. How many comments were made on each video, and what are their corresponding video names?":
    query4='''select comments as no_comments,title as videotitle from videos where comments is not null'''
    cursor.execute(query4)
    mydb.commit()
    t4=cursor.fetchall()
    df4=pd.DataFrame(t4,columns=["NO OF COMMENTS","VIDEO TITLE"])
    st.write(df4)

elif question=="5. Which videos have the highest number of likes, and what are their corresponding channel names?":
    query5='''select title as videotitle,channel_name as channelname,likes as likecount
                from videos where likes is not null order by likes desc'''
    cursor.execute(query5)
    mydb.commit()
    t5=cursor.fetchall()
    df5=pd.DataFrame(t5,columns=["VIDEO TITLE","CHANNEL NAME","LIKES COUNT"])
    st.write(df5)

elif question=="6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?":
    query6='''select likes as likecount,title as videotitle from videos'''
    cursor.execute(query6)
    mydb.commit()
    t6=cursor.fetchall()
    df6=pd.DataFrame(t6,columns=["LIKES COUNT","VIDEO TITLE"])
    st.write(df6)

elif question=="7. What is the total number of views for each channel, and what are their corresponding channel names?":
    query7='''select channel_name as channelname ,views as totalviews from channels'''
    cursor.execute(query7)
    mydb.commit()
    t7=cursor.fetchall()
    df7=pd.DataFrame(t7,columns=["CHANNEL NAME","TOTAL VIEWS"])
    st.write(df7)

elif question=="8. What are the names of all the channels that have published videos in the year 2022?":
    query8='''select title as video_title,published_date as videorelease,channel_name as channelname from videos
                where extract(year from published_date)=2022'''
    cursor.execute(query8)
    mydb.commit()
    t8=cursor.fetchall()
    df8=pd.DataFrame(t8,columns=["VIDEO TITLE","PUBLISHED DATE","CHANNEL NAME"])
    st.write(df8)

elif question=="9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    query9='''select channel_name as channelname,AVG(duration) as averageduration from videos group by channel_name'''
    cursor.execute(query9)
    mydb.commit()
    t9=cursor.fetchall()
    df9=pd.DataFrame(t9,columns=["CHANNEL NAME","AVERAGE DURATION"])

    T9=[]
    for index,row in df9.iterrows():
        channel_title=row["CHANNEL NAME"]
        average_duration=row["AVERAGE DURATION"]
        average_duration_str=str(average_duration)
        T9.append(dict(CHANNEL_NAME=channel_title,AVERAGE_DURATION=average_duration_str))
    df1=pd.DataFrame(T9)
    st.write(df1)

elif question=="10. Which videos have the highest number of comments, and what are their corresponding channel names?":
    query10='''select title as videotitle, channel_name as channelname,comments as comments from videos where comments is
                not null order by comments desc'''
    cursor.execute(query10)
    mydb.commit()
    t10=cursor.fetchall()
    df10=pd.DataFrame(t10,columns=[" VIDEO TITLE","CHANNEL NAME","COMMENTS"])
    st.write(df10)