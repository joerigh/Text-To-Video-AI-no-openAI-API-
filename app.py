import streamlit as st
import asyncio
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
from utility.render.render_engine import get_output_media

# ===========================
# Konfigurasi
# ===========================
SAMPLE_FILE_NAME = "audio_tts.wav"
VIDEO_SERVER = "pexel"
PEXELS_API_KEY = "DLzD281196wa1jxs3Fq2yVITUnt9NPTV3FUcpykXqBv1p9tzOLRMnIqH"

# ===========================
# Streamlit GUI
# ===========================
st.title("Text-To-Video AI (Tanpa OpenAI)")
st.write("Masukkan naskah/video storyboard di bawah ini:")

script_text = st.text_area("Naskah Video", height=200)

if st.button("Generate Video") and script_text.strip():
    with st.spinner("Membuat audio..."):
        asyncio.run(generate_audio(script_text, SAMPLE_FILE_NAME))
    st.success("Audio berhasil dibuat!")

    with st.spinner("Membuat timed captions..."):
        timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    st.success("Timed captions dibuat!")

    with st.spinner("Mencari background video di Pexels..."):
        search_terms = getVideoSearchQueriesTimed(script_text, timed_captions)
        background_video_urls = None
        if search_terms:
            all_videos = generate_video_url(search_terms, VIDEO_SERVER, api_key=PEXELS_API_KEY)
            if all_videos:
                background_video_urls = merge_empty_intervals(all_videos)

    if background_video_urls:
        with st.spinner("Membuat video final..."):
            video_output = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        st.success("Video Final berhasil dibuat!")
        st.video(video_output)
    else:
        st.error("Video Final tidak tersedia karena background video tidak ditemukan.")