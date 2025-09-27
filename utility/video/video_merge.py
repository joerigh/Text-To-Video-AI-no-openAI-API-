import os
import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
from .video_search import generate_video_url

def get_output_media(audio_path, timed_captions, video_segments, provider, output_path):
    clips = []

    for query in video_segments:
        try:
            video_url = generate_video_url(query, provider)
            if not video_url:  
                # fallback ke "nature" kalau query gagal
                print(f"Query '{query}' gagal, fallback ke 'nature'")
                video_url = generate_video_url("nature", provider)

            if video_url:
                video_clip = VideoFileClip(video_url).resize((1280, 720))
                clips.append(video_clip)
        except Exception as e:
            print(f"Gagal ambil video untuk '{query}': {e}")
            continue

    if not clips:
        raise RuntimeError("Tidak ada video yang berhasil diambil, bahkan fallback gagal.")

    # gabungkan semua video
    final_video = concatenate_videoclips(clips, method="compose")

    # tambahkan audio
    audio_clip = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio_clip)

    # export hasil
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path