import streamlit as st
from utility.audio.audio_generator import generate_audio
from utility.video.background_video_generator import generate_video_paths
from utility.render.render_engine import get_output_media
import asyncio

st.title("Easy Text-to-Video AI")

script_text = st.text_area("Masukkan naskah video")
keywords_text = st.text_area("Masukkan keyword (pisah koma)")

if st.button("Generate Video"):
    keywords = [k.strip() for k in keywords_text.split(",")]
    
    # Dummy timed captions, misal tiap kata 2 detik
    timed_captions = []
    t = 0
    for word in script_text.split():
        timed_captions.append(((t, t+2), word))
        t += 2

    # Generate video paths
    timed_video_searches = [((t1, t2), [k]) for (t1,t2), k in zip(timed_captions, keywords)]
    video_files = generate_video_paths(timed_video_searches)

    # Generate audio
    audio_file = "audio.mp3"
    asyncio.run(generate_audio(script_text, audio_file))

    # Render final video
    output_file = get_output_media(audio_file, timed_captions, video_files)
    st.success(f"Video berhasil dibuat: {output_file}")