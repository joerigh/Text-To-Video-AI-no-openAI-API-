import os
import requests
import tempfile

PEXELS_API_KEY = os.environ.get('PEXELS_API_KEY')

def search_videos(query_string, orientation_landscape=True):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query_string,
        "orientation": "landscape" if orientation_landscape else "portrait",
        "per_page": 15
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def getBestVideo(query_string, orientation_landscape=True, used_vids=[]):
    vids = search_videos(query_string, orientation_landscape)
    videos = vids['videos']

    # Filter HD videos
    if orientation_landscape:
        filtered_videos = [v for v in videos if v['width']>=1920 and v['height']>=1080]
    else:
        filtered_videos = [v for v in videos if v['width']>=1080 and v['height']>=1920]

    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15-int(x['duration'])))

    for video in sorted_videos:
        for vf in video['video_files']:
            if orientation_landscape and vf['width']==1920 and vf['height']==1080:
                if not (vf['link'].split('.hd')[0] in used_vids):
                    return vf['link']
            elif not orientation_landscape and vf['width']==1080 and vf['height']==1920:
                if not (vf['link'].split('.hd')[0] in used_vids):
                    return vf['link']
    return None

def download_video(video_url):
    if not video_url:
        return None
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    headers = {"Authorization": PEXELS_API_KEY}
    r = requests.get(video_url, headers=headers)
    r.raise_for_status()
    with open(tmp_file.name, "wb") as f:
        f.write(r.content)
    return tmp_file.name

def generate_video_paths(timed_video_searches, orientation_landscape=True):
    video_paths = []
    used_links = []
    for (t1, t2), keywords in timed_video_searches:
        video_url = None
        for kw in keywords:
            video_url = getBestVideo(kw, orientation_landscape, used_vids=used_links)
            if video_url:
                used_links.append(video_url.split('.hd')[0])
                break
        local_path = download_video(video_url)
        video_paths.append(((t1, t2), local_path))
    return video_paths