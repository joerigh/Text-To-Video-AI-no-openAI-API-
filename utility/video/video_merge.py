from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def get_output_media(audio_path, timed_captions, video_urls, provider, output_path):
    clips = []

    for url in video_urls:
        if not url:
            url = generate_video_url("nature")  # fallback
        try:
            clip = VideoFileClip(url).resize((1280, 720))
            clips.append(clip)
        except Exception as e:
            print(f"Gagal load video {url}: {e}")
            continue

    if not clips:
        raise RuntimeError("Tidak ada video yang berhasil diambil, bahkan fallback gagal.")

    final_video = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path