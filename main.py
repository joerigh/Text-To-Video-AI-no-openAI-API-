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
TEXT_FILE = "naskah.txt"

os.makedirs("output", exist_ok=True)

# -------------------------
# Fungsi buat audio TTS
async def generate_audio_tts(text, file_path):
    communicate = edge_tts.Communicate(text, "id-ID-ArdiNeural")
    await communicate.save(file_path)

# -------------------------
# Fungsi render video
def render_video(user_text, audio_path, video_path, step=2.0):
    print("[INFO] Membuat audio clip...")
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration

    # Background polos hitam
    video_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio_duration)

    print("[INFO] Membuat captions...")
    captions = text_to_captions(user_text, step=step)
    timed_captions = generate_timed_captions(captions)

    # Simpan ke file .srt
    with open(CAPTIONS_FILE, "w", encoding="utf-8") as f:
        for i, cap in enumerate(captions, start=1):
            f.write(f"{i}\n")
            f.write(f"{cap['start']:.2f} --> {cap['end']:.2f}\n")
            f.write(f"{cap['text']}\n\n")

    print(f"[INFO] Captions disimpan ke {CAPTIONS_FILE}")

    # Subtitle di-render ke video
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
# MAIN PROGRAM
if __name__ == "__main__":
    print("🎬 Easy-Text-To-Video-AI (Terminal Version)")

    # Cek apakah ada file naskah.txt
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding="utf-8") as f:
            user_text = f.read().strip()
        print(f"[INFO] Menggunakan teks dari {TEXT_FILE}")
    else:
        user_text = input("Masukkan naskah video: ").strip()

    if not user_text:
        print("[ERROR] Naskah kosong. Keluar.")
        exit(1)

    print("[INFO] Membuat audio TTS...")
    asyncio.run(generate_audio_tts(user_text, AUDIO_FILE))
    print(f"[SUCCESS] Audio berhasil dibuat: {AUDIO_FILE}")

    print("[INFO] Membuat video...")
    captions_text = render_video(user_text, AUDIO_FILE, VIDEO_FILE, step=2.0)

    print(f"[SUCCESS] Video berhasil dibuat: {VIDEO_FILE}")
    print(f"[INFO] Captions:\n{captions_text}")