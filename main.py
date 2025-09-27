from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_utils import merge_empty_intervals, get_output_media

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_video.mp4"
DEFAULT_BG = "assets/bg_default.mp4"

def main():
    # Input manual
    script_text = input("Masukkan naskah video: ").strip()
    if not script_text:
        print("❌ Naskah kosong!")
        return

    # 1. Generate Audio
    print("🎙️ Membuat audio TTS...")
    generate_audio(script_text, AUDIO_FILE)

    # 2. Generate Captions (pakai Whisper timestamped)
    print("📝 Membuat caption sinkron dengan audio...")
    timed_captions = generate_timed_captions(AUDIO_FILE, model_size="base")

    # 3. Cari Background Video
    print("🔍 Mengambil video background dari Pexels...")
    search_terms = getVideoSearchQueriesTimed(script_text, timed_captions)
    background_video_urls = generate_video_url(search_terms, "pexel")

    # Fallback kalau kosong
    if not background_video_urls:
        print("⚠️ Tidak ada video dari Pexels, pakai default background.")
        background_video_urls = [{
            "url": DEFAULT_BG,
            "start": 0,
            "end": timed_captions[-1]["end"]
        }]

    # 4. Merge interval
    background_video_urls = merge_empty_intervals(background_video_urls)

    # Debug
    print("Background video URLs:", background_video_urls)

    # 5. Render Final Video
    print("🎬 Merender video akhir...")
    captions_text = get_output_media(AUDIO_FILE, timed_captions, background_video_urls, "pexel")

    print("✅ Video berhasil dibuat:", VIDEO_FILE)

if __name__ == "__main__":
    main()