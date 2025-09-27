import streamlit as st
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_utils import merge_empty_intervals, get_output_media

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_video.mp4"
DEFAULT_BG = "assets/bg_default.mp4"  # siapkan default video di sini

st.title("🎬 Easy-Text-To-Video-AI")

# --- Input ---
user_text = st.text_area("Masukkan Naskah Video:", height=200)

if st.button("Generate Video"):
    if user_text.strip() == "":
        st.error("Silakan masukkan naskah terlebih dahulu.")
    else:
        # 1. Generate Audio (TTS)
        st.write("🎙️ Membuat audio TTS...")
        generate_audio(user_text, AUDIO_FILE)

        # 2. Generate Captions (pakai Whisper timestamped)
        st.write("📝 Membuat caption sinkron dengan audio...")
        timed_captions = generate_timed_captions(AUDIO_FILE, model_size="base")

        # 3. Cari Query untuk Background Video
        st.write("🔍 Mengambil video background dari Pexels...")
        search_terms = getVideoSearchQueriesTimed(user_text, timed_captions)
        background_video_urls = generate_video_url(search_terms, "pexel")

        # Fallback kalau kosong
        if not background_video_urls:
            st.warning("⚠️ Tidak ada video dari Pexels, pakai default background.")
            background_video_urls = [{
                "url": DEFAULT_BG,
                "start": 0,
                "end": timed_captions[-1]["end"]
            }]

        # 4. Merge interval
        background_video_urls = merge_empty_intervals(background_video_urls)

        # Debug print
        st.write("Background video URLs:", background_video_urls)

        # 5. Render Final Video
        st.write("🎬 Merender video akhir...")
        captions_text = get_output_media(AUDIO_FILE, timed_captions, background_video_urls, "pexel")

        st.success("✅ Video berhasil dibuat!")
        st.video(VIDEO_FILE)