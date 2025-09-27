from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip

def get_output_media(audio_file, captions, video_segments, provider="pexels", output="final_video.mp4"):
    """
    Merge audio, video, dan captions jadi output final.
    video_segments = [(start, end, video_url), ...]
    captions = [((start, end), text), ...]
    """

    clips = []
    for (start, end, url) in video_segments:
        if url:
            try:
                clip = VideoFileClip(url).subclip(0, end - start)
                clips.append(clip)
            except Exception as e:
                print(f"[WARN] Gagal load video {url}: {e}")

    if not clips:
        raise RuntimeError("Tidak ada video yang berhasil diambil.")

    video = concatenate_videoclips(clips, method="compose")

    # Tambah captions
    caption_clips = []
    for (start, end), text in captions:
        txt_clip = (TextClip(text, fontsize=40, color="white", method="caption", size=(video.w, None))
                    .set_position(("center", "bottom"))
                    .set_start(start)
                    .set_duration(end - start))
        caption_clips.append(txt_clip)

    final = CompositeVideoClip([video, *caption_clips])

    # Tambah audio
    audio = AudioFileClip(audio_file)
    final = final.set_audio(audio)

    final.write_videofile(output, fps=24, codec="libx264", audio_codec="aac")

    return output