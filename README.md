Project Name: YouTube Data Harvesting and Warehousing

Objective:
The goal of this project is to create a tool that lets users access and analyze data from various YouTube channels.

Tools and Libraries Used:
Streamlit: It's a tool used to make the program easy to use.
Python: This is the main programming language used for the project.
Google API Client: Helps in talking to YouTube's data.
MongoDB: A type of database that's good for storing different kinds of data.
PostgreSQL: Another type of database, known for being reliable and good for managing data.
Ethical Perspective on YouTube Data Scraping:
It's important to be responsible when getting data from YouTube. This means following YouTube's rules, getting permission if needed, and making sure people's privacy is respected.

Required Libraries:
googleapiclient.discovery
streamlit
psycopg2
pymongo
pandas

Features:
You can get data from YouTube channels and videos using the YouTube API.
The data is saved in MongoDB for easy storage.
Data can also be moved from MongoDB to PostgreSQL for easier searching and analyzing.


Installation Instructions:
1. Install Python:
Make sure you have Python installed on your computer. You can download it from Python's official website.

2. Install Required Libraries:
Open your command line or terminal.
Use pip, Python's package manager, to install the required libraries by running the following commands:

pip install streamlit google-api-python-client pymongo psycopg2 pandas

3. Set Up Google API Credentials:
Go to the Google Developers Console.
Create a new project or select an existing one.
Enable the YouTube Data API v3 for your project.
Create credentials for your project (API key or OAuth 2.0 client ID) and save them securely.

4. Set Up Environment Variables:

Create a file named .env in the project directory.
Add your Google API credentials and any other sensitive information as environment variables in this file. For example:
makefile

YOUTUBE_API_KEY=your-api-key
MONGODB_URI=your-mongodb-uri
POSTGRESQL_URI=your-postgresql-uri

5. Run the Application:

Navigate to the project directory in your command line or terminal.
Run the Streamlit application using the following command:
arduino

streamlit run app.py

6. Access the Application:

Once the application is running, open your web browser and go to the URL provided by Streamlit (usually http://localhost:8501).
You should now be able to interact with the YouTube Data Harvesting and Warehousing application.
