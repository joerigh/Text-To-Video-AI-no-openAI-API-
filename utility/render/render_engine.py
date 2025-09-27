import tempfile
import os
import subprocess
from moviepy.editor import AudioFileClip, CompositeVideoClip, CompositeAudioClip, VideoFileClip, TextClip

def get_program_path(program_name):
    try:
        search_cmd = "where" if os.name == "nt" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except:
        return None

def download_file(url, filename):
    import requests
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    visual_clips = []
    for (t1, t2), video_url in background_video_data:
        video_filename = tempfile.NamedTemporaryFile(delete=False).name
        download_file(video_url, video_filename)
        video_clip = VideoFileClip(video_filename).subclip(0, t2-t1)
        video_clip = video_clip.set_start(t1)
        visual_clips.append(video_clip)

    audio_clip = AudioFileClip(audio_file_path)
    audio_clips = [audio_clip]

    for t1, t2, text in timed_captions:
        text_clip = TextClip(text, fontsize=50, color="white", stroke_width=2, stroke_color="black")
        text_clip = text_clip.set_start(t1).set_end(t2).set_position(("center","bottom"))
        visual_clips.append(text_clip)

    video = CompositeVideoClip(visual_clips)
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.audio = audio
        video.duration = audio.duration

    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25)
    return OUTPUT_FILE_NAME