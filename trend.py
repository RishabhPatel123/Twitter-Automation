import requests
from bs4 import BeautifulSoup

def fetch_trend():
    url = "https://xtrends.iamrohit.in/india"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            content = response.text
            return content 
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_trending_hashtags(html_content,limit):
    soup = BeautifulSoup(html_content, 'html.parser')
    trends = []
    #print(f"soup :{soup}")
    rows = soup.select('tbody tr')
    #print(f"Rows {rows}")
    for row in rows[:limit]:
        trend_link = row.find('a', class_='tweet')
        if trend_link:
            trend_name = trend_link.text.strip()
            trend_url = trend_link['href']
            tweet_count = trend_link.get('tweetcount', 'N/A')
            trends.append({
                'name': trend_name,
                'url': trend_url,
                'tweet_count': tweet_count
            })
    return trends

def is_english(text):
    return all(ord(char)<128 for char in text)

def get_EnglishTrend(htmlContent,limit=5):
    allTrends = get_trending_hashtags(htmlContent,15)
    english_Trends = [trend for trend in allTrends if is_english(trend['name'])]
    return english_Trends[:limit]

def prepareTrend(limit):
    html = fetch_trend()
    if html:
        trends_list = get_EnglishTrend(html,limit)
        lines=[]
        for idx, trend in enumerate(trends_list, 1):
            lines.append(f"{idx}. {trend['name']} ({trend['tweet_count']} Tweets) URL: {trend['url']}")
        return lines
