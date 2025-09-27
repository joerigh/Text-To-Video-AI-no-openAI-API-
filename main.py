import os
from utility.audio.audio_generator import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_video.mp4"

# ===== Input teks / naskah =====
naskah = input("Masukkan teks / naskah video: ")

# ===== 1. Generate audio baru jika file tts.wav tidak ada =====
if not os.path.exists(AUDIO_FILE):
    print("Membuat audio baru...")
generate_audio(naskah, AUDIO_FILE)

# ===== 2. Generate timed captions =====
timed_captions = generate_timed_captions(AUDIO_FILE)

# ===== 3. Generate query & download video =====
search_queries = getVideoSearchQueriesTimed(timed_captions)
video_files = []
for idx, q in enumerate(search_queries):
    vf = download_video_from_pexels(q, idx)
    if vf:
        video_files.append(vf)

print("Video files berhasil diambil:")
for vf in video_files:
    print(vf, os.path.exists(vf))

# ===== 4. Fallback jika kosong =====
if not video_files:
    fallback_path = "output/fallback.mp4"
    if os.path.exists(fallback_path):
        print("Menggunakan video fallback")
        video_files.append(fallback_path)
    else:
        print("Tidak ada video tersedia, hentikan proses")
        exit(1)

# ===== 5. Merge video + audio =====
get_output_media(AUDIO_FILE, video_files, VIDEO_FILE)
print("Selesai! Video final tersimpan di:", VIDEO_FILE)