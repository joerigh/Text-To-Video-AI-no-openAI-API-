import os
from utility.audio.tts import generate_tts
from utility.video.video_merge import get_output_media
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels

VIDEO_FOLDER = "output"
VIDEO_OUTPUT = "output/final_video.mp4"
AUDIO_FILE = "output/tts.wav"

# Pastikan folder output ada
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# Contoh timed captions (start_time, caption)
timed_captions = [
    (0, "Ini contoh kalimat pertama untuk video."),
    (5, "Kalimat kedua akan muncul di video."),
]

# Generate TTS audio
generate_tts(" ".join([caption for _, caption in timed_captions]), AUDIO_FILE)

# Ambil query video dari caption
video_queries = getVideoSearchQueriesTimed(timed_captions, max_words=10)  # kata panjang untuk irit quota

# Download video dari Pexels
video_files = []
for idx, query in enumerate(video_queries):
    video_path = download_video_from_pexels(query, idx)
    if video_path:
        video_files.append(video_path)

# Gabungkan video + audio
if video_files and os.path.exists(AUDIO_FILE):
    get_output_media(AUDIO_FILE, video_files, VIDEO_OUTPUT)
    print(f"Video berhasil dibuat: {VIDEO_OUTPUT}")
else:
    print("Tidak ada video atau audio yang berhasil digabung")