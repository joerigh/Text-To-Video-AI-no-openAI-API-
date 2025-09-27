import os
import requests
from deep_translator import GoogleTranslator

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
OUTPUT_FOLDER = "output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def getVideoSearchQueriesTimed(timed_captions, max_words=5):
    """
    Mengubah timed captions menjadi query video untuk Pexels.
    Ambil 3-5 kata pertama tiap caption, translate ke Inggris.
    """
    queries = []
    for _, caption in timed_captions:
        words = caption.split()[:max_words]
        query = " ".join(words)
        query_en = GoogleTranslator(source='auto', target='en').translate(query)
        queries.append(query_en)
    return queries


def download_video_from_pexels(query, idx=0, output_folder=OUTPUT_FOLDER):
    """
    Download video dari Pexels API sesuai query.
    """
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }
    url = "https://api.pexels.com/videos/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data['videos']:
            video_url = data['videos'][0]['video_files'][0]['link']
            output_path = os.path.join(output_folder, f"video_{idx}.mp4")

            # Download video
            r = requests.get(video_url, stream=True)
            with open(output_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return output_path
        else:
            print(f"Tidak ada video ditemukan untuk query: {query}")
            return None

    except Exception as e:
        print(f"Error saat download video untuk query '{query}': {e}")
        return None