import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# endpoint video Pexels
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

def translate_to_en(text):
    """
    Translate teks ke bahasa Inggris pakai deep-translator
    """
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print("Translation failed:", e)
        return text

def getVideoSearchQueriesTimed(timed_captions):
    """
    Convert captions -> list query strings (translated to English)
    timed_captions = [((start,end), text), ...]
    """
    queries = []
    for (start, end), text in timed_captions:
        text = text.strip()
        if text:
            text_en = translate_to_en(text)
            queries.append(text_en)
    return queries

def generate_video_url(query, per_page=1):
    """
    Ambil video URL dari Pexels API sesuai query
    Fallback otomatis ke 'nature' jika query gagal
    """
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page, "orientation": "landscape"}

    try:
        resp = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Pexels API request failed for query '{query}': {e}")
        return None

    data = resp.json()
    videos = data.get("videos", [])
    if not videos:
        print(f"No video found for query: '{query}'")
        return None

    # ambil video pertama
    return videos[0]["video_files"][0]["link"]

def generate_video_url_with_fallback(query):
    """
    Ambil video untuk query, fallback otomatis ke 'nature'
    """
    url = generate_video_url(query)
    if not url:
        print(f"Query '{query}' gagal, fallback ke 'nature'")
        url = generate_video_url("nature")
    return url