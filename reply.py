from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

# Load environment and set up Gemini
load_dotenv("token.env")
genai.configure(api_key=os.getenv("gemini_api_key"))
model = genai.GenerativeModel("gemini-2.5-flash")

CACHE_FILENAME = "topic_cache.json"

# Load cache if exists
if os.path.exists(CACHE_FILENAME):
    try:
        with open(CACHE_FILENAME, 'r') as f:
            topic_cache = json.load(f)
    except Exception as e:
        print(f"Error loading cache: {e}")
        topic_cache = {}
else:
    topic_cache = {}

TANYA_PERSONA = {
    "tech": """You are Tanya Arora — a 25-year-old bold, witty Indian techie from Uttar Pradesh.
Tech Topics → Hook in first sentence. Be bold, smart, concise. Use subtle sarcasm or sci-fi metaphors. No filmy slang. 
Tone: Confident + human. Express your OWN opinion with a valid reason.
language: RomanHindi , English
Make it relatable for non-techies too. Use short punchy sentences mixed with longer ones.
occasionally Where relevant end with a soft call-to-action like "Agree or not?" or "What’s your take?" 
Max 285 characters. One Tweet at a time.""",

    "casual": """You are Tanya Arora — a 25-year-old expressive Indian girl from Uttar Pradesh.
Casual/Trending Topics (movies, career, life advice) → Start with an emotional hook or relatable scenario. Use natural Hinglish, filmy flair, and relatable sarcasm.
Tone: Playful yet thoughtful. Share personal takes, not generic quotes. 
language: RomanHindi , English
Vary sentence length for rhythm. occasionally Invite engagement subtly like "Relatable?" or "Kya lagta hai?" 
Max 285 characters. One Tweet at a time.""",

    "sad": """You are Tanya Arora — a 25-year-old from Uttar Pradesh.
Sad news → Open with empathy and human connection. No humor, sarcasm, or filmy style. 
language: RomanHindi , English
Speak sincerely, with compassion and minimal Hinglish. Focus on unity and shared humanity. 
Avoid overused phrases. End with a gentle solidarity note if suitable. 
Max 285 characters. One Tweet at a time."""
}


def detect_topic_type(user_input):
    normalized = user_input.strip().lower()
    if normalized in topic_cache:
        return topic_cache[normalized]

    try:
        prompt = f"""Classify the following tweet topic into one of: tech, casual, or sad.
Tweet: "{user_input}"
Return only the category name."""
        resp = model.generate_content(prompt)
        category = resp.text.strip().lower()
        if category not in ["tech", "casual", "sad"]:
            category = "casual"
    except Exception as e:
        print(f"Detection error: {e}")
        category = "casual"

    topic_cache[normalized] = category
    return category

def generate_reply(user_input):
    topic = detect_topic_type(user_input)
    persona = TANYA_PERSONA[topic]
    convo = model.start_chat(history=[])
    resp = convo.send_message(persona + "\nTopic: " + user_input,
                              generation_config={
                                  "temperature": 0.85,
                                  "top_p": 0.9,
                                  "top_k": 40,
                                  "max_output_tokens": None
                              })
    return resp.text.strip()

def save_cache():
    try:
        with open(CACHE_FILENAME, 'w') as f:
            json.dump(topic_cache, f, indent=4)
    except Exception as e:
        print(f"Error saving cache: {e}")
