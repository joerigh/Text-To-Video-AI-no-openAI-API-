import streamlit as st
from main import VIDEO_OUTPUT, AUDIO_FILE, VIDEO_FOLDER, timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels
from utility.video.video_merge import get_output_media
from utility.audio.text_to_speech import generate_tts
import os

st.title("Easy Text to Video AI")

text_input = st.text_area("Masukkan naskah video:", height=150)

if st.button("Buat Video"):
    if not text_input.strip():
        st.warning("Teks kosong!")
    else:
        # Simpan timed captions sementara, bisa disederhanakan
        captions = [(i*5, line.strip()) for i, line in enumerate(text_input.split('\n')) if line.strip()]

        # Generate TTS
        AUDIO_FILE_PATH = "output/tts.wav"
        if not os.path.exists(AUDIO_FILE_PATH):
            generate_tts(captions, AUDIO_FILE_PATH)

        # Query panjang
        queries = getVideoSearchQueriesTimed(captions, max_words=10)
        video_files = []
        for idx, query in enumerate(queries):
            output_path = os.path.join(VIDEO_FOLDER, f"video_{idx}.mp4")
            if os.path.exists(output_path):
                video_files.append(output_path)
            else:
                vid = download_video_from_pexels(query, idx=idx)
                if vid:
                    video_files.append(vid)

        if video_files:
            st.info("Menggabungkan video + audio...")
            get_output_media(AUDIO_FILE_PATH, video_files, VIDEO_OUTPUT)
            st.success(f"Selesai! Video akhir ada di: {VIDEO_OUTPUT}")
            st.video(VIDEO_OUTPUT)
        else:
            st.error("Tidak ada video yang berhasil didownload.")