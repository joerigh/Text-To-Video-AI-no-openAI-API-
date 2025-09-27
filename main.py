from utility.audio.audio_generator import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media

# ===== Input teks / naskah =====
naskah = input("Masukkan teks / naskah video: ")

# ===== 1. Generate audio =====
AUDIO_FILE = "audio_tts.wav"
generate_audio(naskah, AUDIO_FILE)

# ===== 2. Generate timed captions =====
timed_captions = generate_timed_captions(AUDIO_FILE)

# ===== 3. Download video per caption =====
search_queries = getVideoSearchQueriesTimed(timed_captions)
video_files = []
for idx, q in enumerate(search_queries):
    vf = download_video_from_pexels(q, idx)
    if vf:
        video_files.append(vf)

if not video_files:
    print("Tidak ada video berhasil diambil. Hentikan proses.")
    exit(1)

# ===== 4. Merge video + audio =====
VIDEO_FILE = "final_video.mp4"
get_output_media(AUDIO_FILE, video_files, VIDEO_FILE)

print("Selesai! Video final tersimpan di:", VIDEO_FILE)