import mysql.connector
import datetime as dt

"""Database Configuration"""
dbName = "twitter"
tableName = "tweets"

def get_tweet_time():
    """tweet time to save database"""
    now = dt.datetime.now()
    tweet_time = now.strftime("%H:%M")          # e.g., hh:mm 
    tweet_date = now.strftime("%d-%m-%y")       # e.g., dd-mm-yy
    tweet_day = now.strftime("%A")              # e.g., Thursday

    return tweet_time,tweet_date,tweet_day

def get_db_connection(dbName=None):
    """Connect to database """
    try:
        conn = mysql.connector.connect(host="localhost",user="root",password="rish366",database=dbName if dbName else None)
        print("[+] Database Connected")
        return conn 
    except Exception as e:
        print(f"[-] Connection Failed. {e}")
        return None

def createDatabase():
    db = get_db_connection()
    """Create Database if not Exist"""
    if db is None:
        return
 
    try:
        cursor = db.cursor()
        query = f"CREATE DATABASE IF NOT EXISTS {dbName};"
        cursor.execute(query)
        cursor.execute(f"USE {dbName}")
        tableQuery = f"""CREATE TABLE IF NOT EXISTS {tableName} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tweet_text TEXT NOT NULL,
                    tweet_type VARCHAR(50),
                    sent BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );"""
        cursor.execute(tableQuery)
        db.commit()
        print(f"[+] Database- {dbName} and Table- {tableName} Created.")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        db.close()

def save_tweets(tweet,tweet_type,status):
    try:
        db = get_db_connection(dbName=dbName)
        cursor = db.cursor()
        #SQL Query to save tweets detail
        query = f"""
                INSERT INTO {tableName} (tweet_text,tweet_type,sent,tweet_time,tweet_date,tweet_day)
                VALUES (%s,%s,%s,%s,%s,%s)
            """
        #get the time of tweet
        tweet_time,date,day=get_tweet_time()
        values = (tweet,tweet_type,status,tweet_time,date,day)
        cursor.execute(query,values)
        db.commit()
        print(f"[+] Tweet saved in Database.")
    except Exception as e:
        print(f"[-] Error in saving Tweets-- {e}")
        return None
    finally:
        cursor.close()
        db.close()
