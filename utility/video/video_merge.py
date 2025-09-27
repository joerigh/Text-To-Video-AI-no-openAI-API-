import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip


def get_output_media(audio_file, timed_captions, video_files, provider="pexel", output_file="final_output.mp4"):
    """
    Merge background videos + audio + timed captions menjadi 1 video final.
    """
    valid_clips = []

    # cek video hasil download
    for vf in video_files:
        if not os.path.exists(vf):
            print(f"⚠️ Skip, file tidak ditemukan: {vf}")
            continue
        try:
            clip = VideoFileClip(vf).resize(height=720)
            valid_clips.append(clip)
        except Exception as e:
            print(f"⚠️ Skip video {vf}, error: {e}")

    if not valid_clips:
        raise RuntimeError("❌ Tidak ada video valid untuk digabung.")

    # gabung semua background video
    background = concatenate_videoclips(valid_clips, method="compose")

    # load audio
    audio = AudioFileClip(audio_file)
    background = background.set_audio(audio)

    # tambahkan caption
    caption_clips = []
    for (start, end), text in timed_captions:
        txt_clip = (TextClip(text, fontsize=40, color="white", size=(1200, None), method="caption")
                    .set_start(start)
                    .set_end(end)
                    .set_position(("center", "bottom")))
        caption_clips.append(txt_clip)

    final = CompositeVideoClip([background] + caption_clips)

    # set durasi sesuai audio (biar sinkron)
    final = final.set_duration(audio.duration)

    final.write_videofile(output_file, fps=24)

    return "Video berhasil dibuat."