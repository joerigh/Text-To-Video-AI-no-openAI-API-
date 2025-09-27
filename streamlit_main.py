import os
import streamlit as st
from utility.audio.audio_generator import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media
from PIL import Image

# Patch untuk Pillow terbaru agar TextClip resize tidak error
from moviepy.editor import TextClip
TextClip._resize_resampling_method = Image.Resampling.LANCZOS

st.title("Easy Text-To-Video AI")

user_text = st.text_area("Masukkan teks / naskah video:", height=150)

if st.button("Generate Video"):
    if not user_text.strip():
        st.warning("Teks kosong!")
    else:
        AUDIO_FILE = "audio_tts.wav"
        if not os.path.exists(AUDIO_FILE):
            st.info("Membuat audio baru...")
        generate_audio(user_text, AUDIO_FILE)

        st.info("Membuat timed captions...")
        timed_captions = generate_timed_captions(AUDIO_FILE)

        st.info("Mengambil video dari Pexels...")
        search_queries = getVideoSearchQueriesTimed(timed_captions)
        video_files = []
        for idx, q in enumerate(search_queries):
            vf = download_video_from_pexels(q, idx)
            if vf:
                video_files.append(vf)

        st.write("Video berhasil diambil:")
        for vf in video_files:
            st.write(vf, os.path.exists(vf))

        # Fallback
        if not video_files:
            fallback_path = "output/fallback.mp4"
            if os.path.exists(fallback_path):
                st.info("Menggunakan video fallback")
                video_files.append(fallback_path)
            else:
                st.error("Tidak ada video tersedia. Hentikan proses")
                st.stop()

        VIDEO_FILE = "final_video_streamlit.mp4"
        st.info("Menggabungkan video + audio...")
        get_output_media(AUDIO_FILE, video_files, VIDEO_FILE)

        st.success(f"Video final tersimpan: {VIDEO_FILE}")
        st.video(VIDEO_FILE)