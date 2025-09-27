import streamlit as st
import asyncio
import edge_tts
from moviepy.editor import TextClip, AudioFileClip, CompositeVideoClip, ColorClip
from utility.captions.timed_captions_generator import (
    text_to_captions,
    generate_timed_captions
)
import os

# -------------------------
# Konfigurasi dasar
AUDIO_FILE = "output/audio_tts.wav"
VIDEO_FILE = "output/final_video.mp4"
CAPTIONS_FILE = "output/captions.srt"

os.makedirs("output", exist_ok=True)

# -------------------------
# Fungsi buat audio TTS
async def generate_audio_tts(text, file_path):
    communicate = edge_tts.Communicate(text, "id-ID-ArdiNeural")  # suara Indonesia
    await communicate.save(file_path)


# -------------------------
# Fungsi buat video dengan caption
def render_video(user_text, audio_path, video_path, step=2.0):
    # 1. Load audio
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration

    # 2. Background video (warna polos)
    video_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio_duration)

    # 3. Generate captions
    captions = text_to_captions(user_text, step=step)
    timed_captions = generate_timed_captions(captions)

    # Simpan ke file .srt
    with open(CAPTIONS_FILE, "w", encoding="utf-8") as f:
        for i, cap in enumerate(captions, start=1):
            f.write(f"{i}\n")
            f.write(f"{cap['start']:.2f} --> {cap['end']:.2f}\n")
            f.write(f"{cap['text']}\n\n")

    # 4. Tambahkan teks ke video (hanya untuk demo)
    subtitle_clips = []
    for cap in captions:
        txt_clip = (TextClip(cap["text"], fontsize=40, color="white", size=(1200, None), method="caption")
                    .set_position(("center", "bottom"))
                    .set_start(cap["start"])
                    .set_end(cap["end"]))
        subtitle_clips.append(txt_clip)

    final = CompositeVideoClip([video_clip, *subtitle_clips]).set_audio(audio_clip)
    final.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac")

    return timed_captions


# -------------------------
# STREAMLIT UI
st.title("🎬 Easy-Text-To-Video-AI")
st.write("Masukkan naskah untuk membuat audio, subtitle, dan video otomatis.")

# Input manual teks
user_text = st.text_area("Masukkan naskah video:")

# Proses TTS
if st.button("Generate Audio + Video") and user_text.strip():
    st.info("Sedang membuat audio...")

    # Generate audio
    asyncio.run(generate_audio_tts(user_text, AUDIO_FILE))
    st.success(f"Audio berhasil dibuat: {AUDIO_FILE}")
    st.audio(AUDIO_FILE)

    # Render video
    st.info("Sedang merender video, tunggu sebentar...")
    captions_text = render_video(user_text, AUDIO_FILE, VIDEO_FILE, step=2.0)
    st.success("Video berhasil dibuat!")

    # Tampilkan caption
    st.subheader("Timed Captions")
    st.text_area("Subtitle:", captions_text, height=200)

    # Tampilkan video hasil
    st.subheader("Hasil Video")
    st.video(VIDEO_FILE)

    # Tombol download
    with open(VIDEO_FILE, "rb") as f:
        st.download_button("Download Video", f, file_name="final_video.mp4")