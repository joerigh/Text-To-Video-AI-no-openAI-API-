import os
import requests
import random
import tempfile
from pathlib import Path

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")  # ambil dari .env
PEXELS_VIDEO_SEARCH_URL = "https://api.pexels.com/videos/search"


def getVideoSearchQueriesTimed(script, timed_captions):
    """
    Buat query pencarian video berdasarkan caption + teks script
    """
    queries = []
    for _, text in timed_captions:
        words = text.split()
        if words:
            queries.append(" ".join(words[:2]))  # ambil 2 kata pertama
    if not queries:
        queries = ["nature", "background"]
    return queries


def download_video_from_url(url, save_dir="downloads"):
    """
    Download video dari URL ke folder lokal
    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    local_filename = os.path.join(save_dir, f"pexels_{random.randint(10000,99999)}.mp4")

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return local_filename
    else:
        print(f"❌ Gagal download video {url}")
        return None


def generate_video_url(search_terms, provider="pexel", per_query=1, save_dir="downloads"):
    """
    Cari & download video dari Pexels API berdasarkan search_terms
    Return: list of local video file paths
    """
    if provider != "pexel":
        raise ValueError("Hanya provider 'pexel' yang didukung untuk sekarang")

    if not PEXELS_API_KEY:
        raise EnvironmentError("PEXELS_API_KEY belum di-set di .env")

    headers = {"Authorization": PEXELS_API_KEY}
    local_videos = []

    for term in search_terms:
        params = {"query": term, "per_page": per_query}
        response = requests.get(PEXELS_VIDEO_SEARCH_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if "videos" in data and data["videos"]:
                # ambil video paling relevan dari hasil pertama
                video_file = data["videos"][0]["video_files"]

                # cari kualitas medium (biar ringan tapi jelas)
                best_file = sorted(video_file, key=lambda x: x["width"])[0]
                video_url = best_file["link"]

                local_path = download_video_from_url(video_url, save_dir=save_dir)
                if local_path:
                    local_videos.append(local_path)
        else:
            print(f"❌ Gagal ambil video untuk query '{term}', status {response.status_code}")

    # fallback kalau kosong
    if not local_videos:
        fallback = download_video_from_url(
            "https://player.vimeo.com/external/454699646.sd.mp4?s=aa7d8c4e8a", save_dir
        )
        if fallback:
            local_videos.append(fallback)

    return local_videos