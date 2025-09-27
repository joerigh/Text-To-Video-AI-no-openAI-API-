import streamlit as st
from utility.audio.audio_generator import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media

st.title("Easy Text-To-Video AI")

# Input teks
user_text = st.text_area("Masukkan teks / naskah video:", height=150)

if st.button("Generate Video"):
    if not user_text.strip():
        st.warning("Teks kosong!")
    else:
        st.info("Membuat audio...")
        AUDIO_FILE = "audio_tts.wav"
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

        if not video_files:
            st.error("Tidak ada video berhasil diambil.")
        else:
            st.info("Menggabungkan video + audio...")
            VIDEO_FILE = "final_video_streamlit.mp4"
            get_output_media(AUDIO_FILE, video_files, VIDEO_FILE)

            st.success(f"Video final tersimpan: {VIDEO_FILE}")
            st.video(VIDEO_FILE)