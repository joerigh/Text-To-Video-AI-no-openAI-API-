import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, TextClip

def get_output_media(audio_file_path, timed_captions, background_video_data):
    visual_clips = []
    for (t1, t2), video_file in background_video_data:
        if video_file is None:
            continue
        video_clip = VideoFileClip(video_file).set_start(t1).set_end(t2)
        visual_clips.append(video_clip)

    audio_clip = AudioFileClip(audio_file_path)
    audio = CompositeAudioClip([audio_clip])

    for (t1, t2), text in timed_captions:
        text_clip = TextClip(txt=text, fontsize=100, color="white",
                             stroke_width=3, stroke_color="black", method="label")
        text_clip = text_clip.set_start(t1).set_end(t2).set_position(["center", 800])
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)
    video.duration = audio.duration
    video.audio = audio
    video.write_videofile("rendered_video.mp4", codec='libx264', audio_codec='aac', fps=25, preset='veryfast')

    return "rendered_video.mp4"