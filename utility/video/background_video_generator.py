import requests

def generate_video_url(search_terms, video_server, api_key=None):
    video_urls = []
    headers = {"Authorization": api_key} if api_key else {}
    for term in search_terms:
        if video_server.lower() == "pexel":
            response = requests.get(f"https://api.pexels.com/videos/search?query={term}&per_page=1", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data["videos"]:
                    video_urls.append(((0, 5), data["videos"][0]["video_files"][0]["link"]))
    return video_urls