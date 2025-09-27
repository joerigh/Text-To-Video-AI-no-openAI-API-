# utility/render/render_engine.py

import os
import tempfile
from moviepy.editor import (
    AudioFileClip, CompositeVideoClip, CompositeAudioClip,
    VideoFileClip, TextClip
)
from utility.video.background_video_generator import search_videos
import requests
import platform
import subprocess

# -------------------------
# Helpers
# -------------------------
def download_file(url, filename):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    with open(filename, 'wb') as f:
        f.write(response.content)

def get_program_path(program_name):
    try:
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except:
        return None

# -------------------------
# Main function
# -------------------------
def get_output_media(audio_file_path, timed_captions, background_video_data, video_server="pexel"):
    OUTPUT_FILE_NAME = "rendered_video.mp4"

    # Set ImageMagick binary for TextClip
    magick_path = get_program_path("magick")
    os.environ['IMAGEMAGICK_BINARY'] = magick_path if magick_path else '/usr/bin/convert'

    # Prepare video clips
    visual_clips = []
    temp_files = []

    for (t1, t2), video_url in background_video_data:
        if not video_url:
            continue
        video_filename = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        download_file(video_url, video_filename)
        temp_files.append(video_filename)

        clip = VideoFileClip(video_filename).subclip(0, max(1, t2-t1))
        clip = clip.set_start(t1).set_end(t2)
        visual_clips.append(clip)

    # Prepare audio
    audio_clip = AudioFileClip(audio_file_path)
    audio_clips = [audio_clip]

    # Prepare text captions
    for (t1, t2), text in timed_captions:
        text_clip = TextClip(txt=text, fontsize=70, color="white",
                             stroke_width=2, stroke_color="black", method="label")
        text_clip = text_clip.set_start(t1).set_end(t2).set_position(("center", "bottom"))
        visual_clips.append(text_clip)

    # Composite video
    video = CompositeVideoClip(visual_clips)
    if audio_clips:
        audio = CompositeAudioClip(audio_clips)
        video.audio = audio
        video.duration = audio.duration

    # Write final video
    video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')

    # Cleanup temp files
    for f in temp_files:
        os.remove(f)

    return OUTPUT_FILE_NAME