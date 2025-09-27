import asyncio
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.render.render_engine import get_output_media

SAMPLE_FILE_NAME = "audio_tts.wav"
VIDEO_SERVER = "pexel"
PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"

# Baca naskah dari file
with open("naskah.txt", "r", encoding="utf-8") as f:
    script_text = f.read()

# Generate audio
asyncio.run(generate_audio(script_text, SAMPLE_FILE_NAME))

# Generate timed captions
timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)

# Generate video search queries
search_terms = getVideoSearchQueriesTimed(script_text, timed_captions)

# Ambil background video dari Pexels
background_video_urls = None
if search_terms:
    all_videos = generate_video_url(search_terms, VIDEO_SERVER, api_key=PEXELS_API_KEY)
    if all_videos:
        background_video_urls = merge_empty_intervals(all_videos)

# Render video final
if background_video_urls:
    video_output = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
    print(f"Video berhasil dibuat: {video_output}")
else:
    print("Video Final tidak tersedia karena background video tidak ditemukan.")