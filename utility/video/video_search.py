import os
import requests
from deep_translator import GoogleTranslator

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/videos/search"

def translate_to_en(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print("Translation failed:", e)
        return text

def getVideoSearchQueriesTimed(timed_captions):
    queries = []
    for (start, end), text in timed_captions:
        text = text.strip()
        if text:
            text_en = translate_to_en(text)
            queries.append(text_en)
    return queries

def generate_video_url(query, provider="pexels", per_page=1):
    if provider != "pexels":
        raise ValueError("Only Pexels provider is supported.")

    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}

    try:
        resp = requests.get(PEXELS_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Pexels API request failed for query '{query}': {e}")
        return None

    data = resp.json()
    videos = data.get("videos", [])
    if not videos:
        print(f"No video found for query: '{query}'")
        return None

    return videos[0]["video_files"][0]["link"]