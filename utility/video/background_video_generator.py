import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_API_KEY:
    raise ValueError("PEXELS_API_KEY belum diset. Silakan set environment variable atau buat file .env")

def generate_video_url(search_terms, per_page=3):
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