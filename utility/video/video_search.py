import os
import requests
from googletrans import Translator

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

translator = Translator()

def translate_to_en(text):
    try:
        result = translator.translate(text, src="id", dest="en")
        return result.text
    except Exception as e:
        print("Translation failed:", e)
        return text

def getVideoSearchQueriesTimed(script, timed_captions):
    search_terms = []
    for item in timed_captions:
        if len(item) == 3:
            _, _, text = item
        else:
            _, text = item
        text_en = translate_to_en(text)
        search_terms.append(text_en)
    return search_terms

def generate_video_url(query, provider="pexels", per_page=1):
    if provider != "pexels":
        raise ValueError("Only Pexels provider is supported now.")

    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={per_page}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Pexels API Error:", response.text)
        return None

    data = response.json()
    videos = data.get("videos", [])
    if not videos:
        print(f"No video found for query: {query}")
        return None

    return videos[0]["video_files"][0]["link"]