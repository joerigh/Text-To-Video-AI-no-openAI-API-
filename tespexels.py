import requests

# Masukkan API Key Pexels langsung di sini
PEXELS_API_KEY = "DLzD281196wa1jxs3Fq2yVITUnt9NPTV3FUcpykXqBv1p9tzOLRMnIqH"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

# Query contoh
query = "nature"
local_file = "video_test.mp4"

# Header & parameter request
headers = {"Authorization": PEXELS_API_KEY}
params = {"query": query, "per_page": 1, "orientation": "landscape"}

try:
    # Ambil video dari Pexels
    response = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    videos = data.get("videos", [])

    if not videos:
        print(f"Tidak ada video ditemukan untuk query '{query}'")
    else:
        video_url = videos[0]["video_files"][0]["link"]
        print(f"Video berhasil diambil: {video_url}")
        
        # Download video ke lokal
        r = requests.get(video_url, stream=True)
        with open(local_file, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Video tersimpan di file: {local_file}")

except Exception as e:
    print(f"Gagal mengambil atau mendownload video: {e}")