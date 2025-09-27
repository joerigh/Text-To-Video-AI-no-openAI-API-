import streamlit as st
import asyncio
from utility.script.script_generator import generate_script_manual
from utility.video.video_searc_query_generator import getVideoSearchQueriesTimed_manual
from utility.audio.audio_generator import generate_audio
from utility.captions.timed_caption_generator import generate_timed_captions
from utility.video.background_video_generator import generate_video_url
from utility.render.render_engine import get_output_media
from googletrans import Translator
from langdetect import detect
import re

# -------------------
# Helpers
# -------------------
translator = Translator()

def extract_keywords_from_script(script, top_n=10):
    words = re.findall(r'\b\w+\b', script.lower())
    stopwords = set(["the","and","is","are","a","of","to","in","for","with","that","on","as","by","at"])
    words = [w for w in words if w not in stopwords]
    counts = {}
    for w in words:
        counts[w] = counts.get(w,0)+1
    keywords = sorted(counts, key=counts.get, reverse=True)[:top_n]
    return keywords

def translate_keywords_to_english(keywords):
    translated = []
    for kw in keywords:
        try:
            trans = translator.translate(kw, src='auto', dest='en').text
            translated.append(trans)
        except:
            translated.append(kw)
    return translated

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

# -------------------
# Streamlit UI
# -------------------
st.title("Easy Text-to-Video AI (Manual + Auto Keyword)")

# Input Script
script_text = st.text_area("Masukkan script video (ID/EN):", height=150)

# Option to auto extract keywords
auto_keyword = st.checkbox("Auto extract keywords dari script?", value=True)

# Input manual keywords
keywords_input = st.text_area("Masukkan keywords (opsional, pisah koma/baris per segment):", height=150)

if st.button("Generate Video"):
    if not script_text:
        st.error("Script harus diisi!")
    else:
        # -------------------
        # 1. Generate Script (manual)
        # -------------------
        script_dict = generate_script_manual(script_text)
        script = script_dict["script"]

        # -------------------
        # 2. Detect language for TTS
        # -------------------
        lang = detect_language(script)
        tts_voice = "id-ID-GadisNeural" if lang == "id" else "en-AU-WilliamNeural"

        # -------------------
        # 3. Generate TTS Audio
        # -------------------
        audio_file = "audio.mp3"
        asyncio.run(generate_audio(script, audio_file, voice=tts_voice))

        # -------------------
        # 4. Generate Timed Captions
        # -------------------
        captions_timed = generate_timed_captions(audio_file)

        # -------------------
        # 5. Prepare keywords
        # -------------------
        if auto_keyword:
            manual_keywords = [translate_keywords_to_english(extract_keywords_from_script(c[1])) for c in captions_timed]
        elif keywords_input:
            # parse input manual
            manual_keywords = [ [kw.strip() for kw in k.split(",")] for k in keywords_input.strip().split("\n")]
        else:
            st.error("Masukkan keywords atau centang auto extract")
            st.stop()

        # -------------------
        # 6. Generate Video URLs via Pexels
        # -------------------
        video_server = "pexel"
        timed_video_urls = generate_video_url(list(zip([c[0] for c in captions_timed], manual_keywords)), video_server)

        # -------------------
        # 7. Render Final Video
        # -------------------
        output_video = get_output_media(audio_file, captions_timed, timed_video_urls, video_server)

        st.success(f"Video berhasil dibuat: {output_video}")
        st.video(output_video)