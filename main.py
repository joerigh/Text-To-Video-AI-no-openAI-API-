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

    print("=== [3] Translate & Generate Pexels Queries ===")
    search_queries = getVideoSearchQueriesTimed(timed_captions)
    video_segments = [generate_video_url(q) or generate_video_url("nature") for q in search_queries]
    print("Video segments:", video_segments)

    print("=== [4] Merge Audio + Video + Captions ===")
    final_path = get_output_media(AUDIO_FILE, timed_captions, video_segments, "pexels", VIDEO_FILE)
    print(f"Video selesai dibuat: {final_path}")


if __name__ == "__main__":
    main()