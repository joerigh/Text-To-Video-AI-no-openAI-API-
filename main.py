import os
from utility.audio.tts import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_merge import get_output_media

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_video.mp4"

def main():
    # Input manual atau dari file naskah.txt
    if os.path.exists("naskah.txt"):
        with open("naskah.txt", "r", encoding="utf-8") as f:
            user_text = f.read().strip()
    else:
        user_text = input("Masukkan teks naskah video: ").strip()

    print("=== [1] Generate Audio ===")
    generate_audio(user_text, AUDIO_FILE)

    print("=== [2] Generate Timed Captions ===")
    timed_captions = generate_timed_captions(AUDIO_FILE)

    print("=== [3] Generate Search Queries ===")
    search_terms = getVideoSearchQueriesTimed(user_text, timed_captions)

    print("=== [4] Ambil Video dari Pexels ===")
    video_segments = generate_video_url(search_terms, "pexels")
    print("Background video URLs:", video_segments)

    print("=== [5] Render Final Video ===")
    final_path = get_output_media(AUDIO_FILE, timed_captions, video_segments, "pexels", VIDEO_FILE)
    print(f"Video selesai dibuat: {final_path}")


if __name__ == "__main__":
    main()