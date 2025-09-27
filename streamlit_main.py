import streamlit as st
import asyncio
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed, merge_empty_intervals
import os

st.title("Text-to-Video AI")

VIDEO_SERVER = "pexel"
SAMPLE_FILE_NAME = "audio_tts.wav"

# Pilihan input naskah
input_option = st.radio("Pilih sumber naskah:", ("Manual Input", "File naskah.txt"))

if input_option == "Manual Input":
    script_text = st.text_area("Masukkan naskah video Anda di sini:")
else:
    if os.path.exists("naskah.txt"):
        with open("naskah.txt", "r", encoding="utf-8") as f:
            script_text = f.read()
        st.text_area("Naskah dari file naskah.txt:", value=script_text, height=200)
    else:
        st.warning("File naskah.txt tidak ditemukan. Silakan pilih input manual.")
        script_text = ""

if st.button("Generate Video") and script_text.strip():
    st.info("Proses generate audio...")
    asyncio.run(generate_audio(script_text, SAMPLE_FILE_NAME))
    
    st.info("Proses generate captions...")
    timed_captions = generate_timed_captions(SAMPLE_FILE_NAME)
    st.write("Timed captions:", timed_captions)
    
    st.info("Proses generate video search queries...")
    search_terms = getVideoSearchQueriesTimed(script_text, timed_captions)
    st.write("Search terms:", search_terms)
    
    background_video_urls = None
    if search_terms:
        st.info("Proses generate background video...")
        background_video_urls = generate_video_url(search_terms, VIDEO_SERVER)
        st.write("Background video URLs:", background_video_urls)
    else:
        st.warning("Tidak ada background video yang ditemukan.")
    
    background_video_urls = merge_empty_intervals(background_video_urls)
    
    if background_video_urls:
        st.info("Proses render final video...")
        final_video = get_output_media(SAMPLE_FILE_NAME, timed_captions, background_video_urls, VIDEO_SERVER)
        st.success("Video berhasil dibuat!")
        st.video(final_video)
    else:
        st.warning("Tidak ada video yang bisa dibuat.")