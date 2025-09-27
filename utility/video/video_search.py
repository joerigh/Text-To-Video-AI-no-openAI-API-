import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_URL = "https://api.pexels.com/videos/search"

HEADERS = {"Authorization": PEXELS_API_KEY}

def getVideoSearchQueriesTimed(script, timed_captions):
    """
    Ambil query pencarian video dari caption.
    Format return: [(start, end, text), ...]
    """
    queries = []
    for (start, end), text in timed_captions:
        cleaned = text.strip()
        if cleaned:
            queries.append((start, end, cleaned))
    return queries


def generate_video_url(search_terms, provider="pexels"):
    """
    Cari video di Pexels sesuai query.
    search_terms = [(start, end, text), ...]
    Return: [(start, end, best_video_url), ...]
    """
    results = []
    for (start, end, query) in search_terms:
        params = {"query": query, "per_page": 1, "orientation": "landscape"}
        resp = requests.get(PEXELS_URL, headers=HEADERS, params=params)

        if resp.status_code == 200:
            data = resp.json()
            if data.get("videos"):
                best_video = data["videos"][0]["video_files"][0]["link"]
                results.append((start, end, best_video))
            else:
                results.append((start, end, None))
        else:
            results.append((start, end, None))

    return results