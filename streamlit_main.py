import streamlit as st
import os
from dotenv import load_dotenv
from utility.captions.timed_captions_generator import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_merge import get_output_media
from utility.audio.tts import generate_audio

load_dotenv()

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_output.mp4"

st.title("🎬 Easy Text-To-Video AI")

user_text = st.text_area("Masukkan teks untuk video:", height=200)

if st.button("Generate Video"):
    if not user_text.strip():
        st.error("Silakan isi teks dulu.")
    else:
        with st.spinner("🔊 Membuat audio..."):
            generate_audio(user_text, AUDIO_FILE)

        with st.spinner("📜 Membuat caption..."):
            timed_captions = generate_timed_captions(AUDIO_FILE)

        with st.spinner("🔎 Mencari video dari Pexels..."):
            search_terms = getVideoSearchQueriesTimed(user_text, timed_captions)
            background_video_files = generate_video_url(search_terms, "pexel")
            st.write("Video ditemukan:", background_video_files)

        with st.spinner("🎬 Merender video..."):
            captions_text = get_output_media(AUDIO_FILE, timed_captions, background_video_files, "pexel")

        st.success("✅ Video berhasil dibuat!")
        st.video(VIDEO_FILE)