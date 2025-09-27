import requests

# masukkan API key Pexels langsung di sini
PEXELS_API_KEY = "DLzD281196wa1jxs3Fq2yVITUnt9NPTV3FUcpykXqBv1p9tzOLRMnIqH"
PEXELS_VIDEO_URL = "https://api.pexels.com/videos/search"

# query contoh
query = "nature"

headers = {
    "Authorization": PEXELS_API_KEY
}

params = {
    "query": query,
    "per_page": 1,
    "orientation": "landscape"
}

try:
    response = requests.get(PEXELS_VIDEO_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    videos = data.get("videos", [])
    if not videos:
        print(f"Tidak ada video ditemukan untuk query '{query}'")
    else:
        video_url = videos[0]["video_files"][0]["link"]
        print(f"Video berhasil diambil: {video_url}")

except Exception as e:
    print(f"Gagal mengambil video: {e}")