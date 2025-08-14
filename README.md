# **Twitter Auto-Tweet Bot**

An advanced **Python-based Twitter automation bot** that generates engaging tweets using **Google Gemini AI**, fetches **real-time trending topics**, and posts them automatically via the **Twitter API (Tweepy)**.

It includes:
- **Trending hashtag detection** from a live source.
- **AI-generated tweets** in different tones (tech, casual, sad) via Gemini AI.
- **Scheduled posting** at optimal times.
- **MySQL database integration** for tweet logging.
- **Duplicate reply prevention** using cached classifications.

---

## **Features**
- 📈 **Trending Topic Fetching** → Uses live data from [xtrends.iamrohit.in](https://xtrends.iamrohit.in/india)
- 🤖 **AI-Powered Tweet Generation** → Gemini AI with a custom “Tanya Arora” persona.
- 🗄 **MySQL Integration** → Stores tweet text, type, timestamp, and posting status.
- ⏰ **Scheduled & Conditional Posting** → Posts only during optimal engagement hours.
- 🛡 **Topic Classification Cache** → Avoids re-calling AI for repeated topics.
- 📝 **Flexible Tweet Types** → Tech, casual, or empathetic tone based on topic.

---

## **Requirements**
Install dependencies from `requirements.txt`:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**requirements.txt**
\`\`\`
tweepy
genai
\`\`\`

Also required:
- `beautifulsoup4` for trend scraping.
- `mysql-connector-python` for DB connection.

Install:
\`\`\`bash
pip install beautifulsoup4 mysql-connector-python
\`\`\`

---

## **Environment Variables (`token.env`)**
Create a `token.env` file in the root folder:

\`\`\`
api_key=YOUR_TWITTER_API_KEY
api_secret=YOUR_TWITTER_API_SECRET
access_token=YOUR_ACCESS_TOKEN
access_token_secret=YOUR_ACCESS_TOKEN_SECRET
bearer_token=YOUR_BEARER_TOKEN
USER_ID=YOUR_TWITTER_USER_ID
gemini_api_key=YOUR_GEMINI_API_KEY
\`\`\`

---

## **Database Setup**
1. Make sure MySQL server is running.
2. Edit DB credentials in `database.py`:
\`\`\`python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="twitter"
)
\`\`\`
3. Run the script to create DB & table automatically:
\`\`\`bash
python database.py
\`\`\`

---

## **How It Works**
1. **Trend Fetching** → `trend.py` scrapes trending hashtags.
2. **AI Tweet Generation** → `reply.py` classifies the topic and generates a tweet using Gemini AI.
3. **Posting** → `main.py` posts the tweet via Twitter API (Tweepy).
4. **Logging** → Tweet details are saved into MySQL.

---

## **Run the Bot**
\`\`\`bash
python main.py
\`\`\`
The bot will:
- Check if it’s a trending posting time.
- Fetch a random trending topic.
- Generate a tweet based on Tanya’s persona.
- Post the tweet and log it in the database.
- Sleep for 1 hour before next cycle.

---

## **File Structure**
\`\`\`
├── main.py             # Main bot loop
├── database.py         # MySQL setup & tweet saving
├── reply.py            # AI reply generation with persona
├── trend.py            # Trending hashtag scraper
├── twitter_client.py   # Twitter API client setup
├── requirements.txt    # Python dependencies
├── token.env           # API keys (not in repo)
\`\`\`

---

## **Example Output**
\`\`\`
[+] Getting Trending Topics...
1. #AIRevolution (45K Tweets) URL: https://twitter.com/search?q=%23AIRevolution
Generating Reply... Topic: AI Revolution in tech world...
Tweet: The AI wave isn’t coming—it’s already here. Adapt or get left behind. 🚀
✅ Scheduled Tweet sent.
[+] Tweet saved in Database.
[+] Bot Cycle Complete. Sleeping for 1 hour...
\`\`\`

---

## **Disclaimer**
This project is for **educational purposes**. Automating tweets can violate Twitter’s terms of service — use responsibly.
