import streamlit as st
import os
from main import VIDEO_OUTPUT, AUDIO_FILE, VIDEO_FOLDER, timed_captions
from utility.audio.tts import generate_tts
from utility.video.video_merge import get_output_media
from utility.video.video_search import getVideoSearchQueriesTimed, download_video_from_pexels

st.title("Easy Text-To-Video AI")

if st.button("Generate Video"):
    os.makedirs(VIDEO_FOLDER, exist_ok=True)

    # Generate TTS
    generate_tts(" ".join([caption for _, caption in timed_captions]), AUDIO_FILE)

    # Ambil query video dari caption
    video_queries = getVideoSearchQueriesTimed(timed_captions, max_words=10)  # kata panjang

    # Download video dari Pexels
    video_files = []
    for idx, query in enumerate(video_queries):
        video_path = download_video_from_pexels(query, idx)
        if video_path:
            video_files.append(video_path)

    # Gabungkan video + audio
    if video_files and os.path.exists(AUDIO_FILE):
        get_output_media(AUDIO_FILE, video_files, VIDEO_OUTPUT)
        st.success(f"Video berhasil dibuat: {VIDEO_OUTPUT}")
        st.video(VIDEO_OUTPUT)
    else:
        st.error("Tidak ada video atau audio yang berhasil digabung")