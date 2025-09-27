import os
from dotenv import load_dotenv
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_merge import get_output_media
from utility.audio.tts import generate_audio

load_dotenv()

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_output.mp4"

if __name__ == "__main__":
    # Ambil naskah dari file
    if os.path.exists("naskah.txt"):
        with open("naskah.txt", "r", encoding="utf-8") as f:
            script = f.read().strip()
    else:
        script = input("Masukkan teks untuk video: ")

    print("🔊 Generate audio...")
    generate_audio(script, AUDIO_FILE)

    print("📜 Generate timed captions...")
    timed_captions = generate_timed_captions(AUDIO_FILE)

    print("🔎 Cari video dari Pexels...")
    search_terms = getVideoSearchQueriesTimed(script, timed_captions)
    background_video_files = generate_video_url(search_terms, "pexel")

    print("🎬 Render video...")
    captions_text = get_output_media(AUDIO_FILE, timed_captions, background_video_files, "pexel")

    print(f"✅ Video final tersimpan di {VIDEO_FILE}")