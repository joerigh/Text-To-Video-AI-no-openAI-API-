import asyncio
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import argparse
import os

def read_script(file_path="naskah.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return input("Masukkan naskah video secara manual: ")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a video from a script.")
    parser.add_argument("--file", type=str, default="naskah.txt", help="Path to script file")
    args = parser.parse_args()

    SAMPLE_FILE_NAME = "audio_tts.wav"
    VIDEO_SERVER = "pexel"

    # Baca naskah
    script_text = read_script(args.file)
    print("Naskah video: \n", script_text)

    # Generate audio TTS
    asyncio.run(generate_audio(script_text, SAMPLE_FILE_NAME))

    # Generate timed captions
    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    print("Timed captions: ", timed_captions)

    # Generate video search queries
    search_terms = getVideoSearchQueriesTimed(script_text, timed_captions)
    print("Search terms: ", search_terms)

    # Generate background video
    background_video_urls = None
    if search_terms:
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        print("Background video URLs: ", background_video_urls)
    else:
        print("No background video")

    background_video_urls = merge_empty_intervals(background_video_urls)

    # Render final video
    if background_video_urls:
        final_video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        print("Video berhasil dibuat: ", final_video)
    else:
        print("Tidak ada video yang dibuat")