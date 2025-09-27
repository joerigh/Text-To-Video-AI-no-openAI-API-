import whisper_timestamped as whisper

def generate_timed_captions(audio_file):
    model = whisper.load_model("small")
    result = model.transcribe(audio_file)
    # Kembalikan format [(start, end), text]
    timed_captions = [(segment.start, segment.end, segment.text) for segment in result["segments"]]
    return timed_captions