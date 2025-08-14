import time
import datetime as dt
import random
import twitter_client
#MY Files
import reply ,trend,database
client = twitter_client.get_client()
USER_ID = twitter_client.USER_ID


# === Scheduled Tweet ===
def scheduled_tweet(tweets):
    STATUS = False
    try:
        client.create_tweet(text=tweets)
        print("✅ Scheduled Tweet sent.")
        STATUS = True
        return STATUS
    except Exception as e:
        print("❗ Scheduled Tweet Error:", e)
        return STATUS

def getStatus():
    hour = dt.datetime.now().hour
    if hour >=1 and hour <= 6:
        return False
    else:
        return True

def isTrendingTime():
    hour = dt.datetime.now().hour
    if hour in (9,1,3,10):
        return False
    return True

def trending_tweets():
    limit = 3
    try:
        trend_tweet = trend.prepareTrend(limit=limit)   #increase number to fetch more trending topics
        for t in trend_tweet:
            print(t)
        return random.choices(trend_tweet)   #choose topic randomly
    except:
        return None
# === Main Loop ===
def run_bot():
    while True:
            prompt = ""
            topic = ""
            if isTrendingTime():
                print(f"[+] Getting Trending Topics...")
                topic = trending_tweets()
                if not topic:
                    continue
                prompt+=f"These are the tweet details.[pattern- topic,number of tweets,url of tweet]{topic}. use all these details for your tweet knowledge not for reference"
                context = " "     #input(f"Want add Context for {topic}: ")
                if not context:
                    context = "There is no context by user. must use topic details to understand the context and intent.Use detail to get tweet reference."
                prompt+=context.join(topic)
                
            else:
                prompt ="Create one tweet in most engaging and trending topic."    #input("Enter topic of tweet:")
                
            #print(prompt)
            #Generate Reply from AI
            print("Gererating Reply...Topic: ",prompt)
            tweet = reply.generate_reply(prompt)
            if tweet:
                print(f"Tweet: {tweet}")
                option = "y"        #input("Want to Tweet(y/n) :").lower()
                if "y" == option:
                    status = scheduled_tweet(tweet)
                    database.save_tweets(tweet=tweet,tweet_type="tweet",status=status)
                    if not status:
                        continue
                    print("[+] Bot Cycle Complete. Sleeping for 1 hour... ---\n")
                    timer = 3600*1
                    for i in range(timer+1):
                        print(f"[+]Remaining Time [{timer-i}] ",end="\r")
                        time.sleep(1)
                elif(option =="n"):
                    continue
                elif(option == "exit"):
                    quit()
                    break
                print("\n")
            else:
                print("Reply not generated...")

run_bot()