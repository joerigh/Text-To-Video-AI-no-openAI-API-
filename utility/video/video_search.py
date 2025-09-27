import os
import requests
from deep_translator import GoogleTranslator

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
OUTPUT_FOLDER = "output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def getVideoSearchQueriesTimed(timed_captions, max_words=10):
    """
    Mengubah timed captions menjadi query video untuk Pexels.
    Ambil 5-10 kata pertama tiap caption untuk menghemat quota.
    Translate ke Inggris.
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
    Memilih HD jika tersedia.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}
    url = "https://api.pexels.com/videos/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['videos']:
            video_files = data['videos'][0]['video_files']
            # Pilih HD jika ada, kalau tidak ambil yg pertama
            video_hd = next((v for v in video_files if v['quality'] == 'hd'), video_files[0])
            video_url = video_hd['link']

            output_path = os.path.join(output_folder, f"video_{idx}.mp4")
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


def download_video_by_id(video_id, output_folder=OUTPUT_FOLDER):
    """
    Download video dari Pexels berdasarkan ID video.
    Memilih HD jika tersedia.
    """
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/videos/videos/{video_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        video_files = data['video_files']
        video_hd = next((v for v in video_files if v['quality'] == 'hd'), video_files[0])
        video_url = video_hd['link']

        output_path = os.path.join(output_folder, f"video_{video_id}.mp4")
        r = requests.get(video_url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return output_path

    except Exception as e:
        print(f"Error saat download video ID '{video_id}': {e}")
        return None