import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def get_output_media(audio_path, video_files, output_path="final_video.mp4"):
    clips = []

    for vf in video_files:
        if not vf or not os.path.exists(vf):
            print(f"File video tidak ada: {vf}")
            continue
        try:
            clip = VideoFileClip(vf).resize((1280, 720))
            clips.append(clip)
        except Exception as e:
            print(f"Gagal load video {vf}: {e}")

    if not clips:
        raise RuntimeError("Tidak ada video yang berhasil digabung")

    final_video = concatenate_videoclips(clips, method="compose")
    audio_clip = AudioFileClip(audio_path)
    final_video = final_video.set_audio(audio_clip)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Video final tersimpan di {output_path}")
    return output_path