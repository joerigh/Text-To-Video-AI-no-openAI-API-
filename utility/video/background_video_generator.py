import os
import requests
from dotenv import load_dotenv

# load .env file
load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY belum diset. Silakan isi file .env di root project")

def generate_video_url(search_terms, per_page=3):
    """
    Ambil video dari Pexels berdasarkan kata kunci (search_terms)
    """
    video_urls = []
    headers = {"Authorization": PEXELS_API_KEY}

    for term in search_terms:
        url = f"https://api.pexels.com/videos/search?query={term}&per_page={per_page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            for video in data.get("videos", []):
                video_file = max(video["video_files"], key=lambda x: x.get("width", 0))
                video_urls.append(video_file["link"])
        else:
            print(f"Gagal ambil video untuk '{term}', status code: {response.status_code}")

    if not video_urls:
        print("Tidak ada video yang ditemukan di Pexels.")
        return None

    return video_urls

def merge_empty_intervals(video_urls):
    return video_urls