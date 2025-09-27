import os
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media
from utility.audio.text_to_speech import generate_tts

VIDEO_OUTPUT = "output/final_video.mp4"
AUDIO_FILE = "output/tts.wav"
VIDEO_FOLDER = "output"

# Contoh timed captions: [(timestamp, caption)]
timed_captions = [
    (0, "Halo teman-teman, selamat datang di tutorial AI ini."),
    (5, "Kita akan belajar bagaimana membuat video otomatis dari teks.")
]

# Generate TTS jika belum ada
if not os.path.exists(AUDIO_FILE):
    generate_tts(timed_captions, AUDIO_FILE)

# Buat query panjang dari captions
queries = getVideoSearchQueriesTimed(timed_captions, max_words=10)

video_files = []
for idx, query in enumerate(queries):
    output_path = os.path.join(VIDEO_FOLDER, f"video_{idx}.mp4")
    if os.path.exists(output_path):
        print(f"Video sudah ada: {output_path}")
        video_files.append(output_path)
    else:
        print(f"Mencari video untuk query: {query}")
        vid = download_video_from_pexels(query, idx=idx)
        if vid:
            video_files.append(vid)

if video_files:
    print("Menggabungkan video + audio...")
    get_output_media(AUDIO_FILE, video_files, VIDEO_OUTPUT)
    print(f"Selesai! Video akhir ada di: {VIDEO_OUTPUT}")
else:
    print("Tidak ada video yang berhasil didownload.")