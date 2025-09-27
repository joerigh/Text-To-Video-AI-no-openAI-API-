import streamlit as st
import os
from utility.audio.tts import generate_audio
from utility.captions.whisper_caption import generate_timed_captions
from utility.video.video_search import getVideoSearchQueriesTimed, generate_video_url
from utility.video.video_merge import get_output_media

AUDIO_FILE = "audio_tts.wav"
VIDEO_FILE = "final_video.mp4"

st.title("🎬 Easy Text To Video AI")

user_text = st.text_area("Masukkan naskah video:", height=200)

if st.button("Generate Video"):
    if not user_text.strip():
        st.error("Silakan isi naskah dulu!")
    else:
        with st.spinner("🔊 Membuat audio..."):
            generate_audio(user_text, AUDIO_FILE)

        with st.spinner("📝 Membuat captions..."):
            timed_captions = generate_timed_captions(AUDIO_FILE)

        with st.spinner("🔍 Cari video di Pexels..."):
            search_terms = getVideoSearchQueriesTimed(user_text, timed_captions)
            video_segments = generate_video_url(search_terms, "pexels")

        st.text("Background video URLs:")
        st.write(video_segments)

        with st.spinner("🎥 Merender video akhir..."):
            final_path = get_output_media(AUDIO_FILE, timed_captions, video_segments, "pexels", VIDEO_FILE)

        st.success("✅ Video selesai dibuat!")
        st.video(final_path)