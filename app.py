# app.py
import streamlit as st
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_caption_generator import generate_timed_captions
from utility.video.video_search_query_generator import getVideoSearchQueriesTimed_manual as getVideoSearchQueriesTimed
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
import asyncio
import tempfile

st.set_page_config(page_title="Easy Text-To-Video AI", layout="wide")

st.title("🎬 Easy Text-To-Video AI")

# ---------------------------
# Input Section
# ---------------------------
script_input = st.text_area("Input your video script:", height=200)
st.markdown("Optional: You can add manual keywords per caption segment (comma-separated)")
manual_keywords_input = st.text_area("Manual keywords (one line per caption segment, optional):", height=150)

video_server = st.selectbox("Video source:", ["pexel"])

if st.button("Generate Video"):
    if not script_input.strip():
        st.warning("Please enter a script first!")
    else:
        # Prepare manual keywords
        manual_keywords = []
        if manual_keywords_input.strip():
            lines = manual_keywords_input.strip().split("\n")
            for line in lines:
                kws = [kw.strip() for kw in line.split(",") if kw.strip()]
                manual_keywords.append(kws)
        # ---------------------------
        # Step 1: Generate Audio
        # ---------------------------
        st.info("🔊 Generating audio...")
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        asyncio.run(generate_audio(script_input, temp_audio_file))
        
        # ---------------------------
        # Step 2: Generate Timed Captions
        # ---------------------------
        st.info("📝 Generating timed captions...")
        timed_captions = generate_timed_captions(temp_audio_file)

        # ---------------------------
        # Step 3: Generate Video Keywords (manual/auto)
        # ---------------------------
        st.info("🔑 Generating keywords for video search...")
        timed_keywords = getVideoSearchQueriesTimed(script_input, timed_captions, manual_keywords)

        # ---------------------------
        # Step 4: Download Background Videos
        # ---------------------------
        st.info("🎥 Downloading background videos...")
        timed_video_urls = generate_video_url(timed_keywords, video_server=video_server)

        # ---------------------------
        # Step 5: Render Final Video
        # ---------------------------
        st.info("🖥️ Rendering final video...")
        output_file = get_output_media(temp_audio_file, timed_captions, timed_video_urls, video_server=video_server)
        st.success(f"✅ Video generated: {output_file}")
        st.video(output_file)