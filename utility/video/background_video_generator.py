# utility/video/background_video_generator.py

import os
import requests
from utility.utils import log_response, LOG_TYPE_PEXEL

PEXELS_API_KEY = os.environ.get('PEXELS_KEY')

def search_videos(query_string, orientation_landscape=True):
    url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0"
    }
    params = {
        "query": query_string,
        "orientation": "landscape" if orientation_landscape else "portrait",
        "per_page": 15
    }

    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    log_response(LOG_TYPE_PEXEL, query_string, json_data)
    return json_data

def getBestVideo(query_string, orientation_landscape=True, used_vids=[]):
    vids = search_videos(query_string, orientation_landscape)
    videos = vids.get('videos', [])

    if orientation_landscape:
        filtered_videos = [v for v in videos if v['width'] >= 1920 and v['height'] >= 1080 and v['width']/v['height']==16/9]
    else:
        filtered_videos = [v for v in videos if v['width'] >= 1080 and v['height'] >= 1920 and v['height']/v['width']==16/9]

    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15-int(x['duration'])))

    for video in sorted_videos:
        for vf in video['video_files']:
            if orientation_landscape and vf['width']==1920 and vf['height']==1080:
                if vf['link'].split('.hd')[0] not in used_vids:
                    return vf['link']
            elif not orientation_landscape and vf['width']==1080 and vf['height']==1920:
                if vf['link'].split('.hd')[0] not in used_vids:
                    return vf['link']
    print("NO LINKS found for query:", query_string)
    return None

def generate_video_url(timed_video_searches, video_server="pexel"):
    """
    timed_video_searches: list of [[t1,t2], [kw1, kw2, ...]]
    """
    timed_video_urls = []
    if video_server == "pexel":
        used_links = []
        for (t1, t2), search_terms in timed_video_searches:
            url = None
            for query in search_terms:
                url = getBestVideo(query, orientation_landscape=True, used_vids=used_links)
                if url:
                    used_links.append(url.split('.hd')[0])
                    break
            timed_video_urls.append([[t1, t2], url])
    else:
        # placeholder untuk future stable-diffusion
        timed_video_urls = [[interval, None] for interval, _ in timed_video_searches]

    return timed_video_urls