import os
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

def download_video_from_pexels(query, idx=0):
    headers = {"Authorization": PEXELS_API_KEY, "User-Agent": "Mozilla/5.0"}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

    try:
        response = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        videos = data.get("videos", [])
        if not videos:
            print(f"Tidak ada video untuk query '{query}'")
            return None

        # pilih resolusi hd atau sd
        video_files = videos[0].get("video_files", [])
        video_url = None
        for vf in video_files:
            if vf.get("quality") in ["hd", "sd"]:
                video_url = vf.get("link")
                break
        if not video_url:
            print(f"Tidak ada file video valid untuk query '{query}'")
            return None

        # download video ke folder output
        local_file = os.path.join(OUTPUT_FOLDER, f"{idx}_{query.replace(' ','_')}.mp4")
        r = requests.get(video_url, headers=headers, stream=True)
        size = int(r.headers.get("content-length", 0))
        if size == 0:
            print(f"Video kosong untuk query '{query}'")
            return None

        with open(local_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Video '{query}' tersimpan di {local_file} ({size/1024:.2f} KB)")
        return local_file

    except Exception as e:
        print(f"Gagal ambil video '{query}': {e}")
        return None