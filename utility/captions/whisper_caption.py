# utility/captions/whisper_caption.py
import re
import os
import sys

# Try import whisper_timestamped; if tidak ada, beri pesan jelas.
try:
    from whisper_timestamped import load_model, transcribe_timestamped
except Exception as e:
    raise ImportError(
        "Module 'whisper_timestamped' tidak tersedia. "
        "Install dulu dengan:\n\n"
        "  pip install git+https://github.com/linto-ai/whisper-timestamped.git\n\n"
        "atau lihat README repo whisper-timestamped. (Error detail: {})".format(e)
    )

def splitWordsBySize(words, maxCaptionSize):
    halfCaptionSize = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= halfCaptionSize and words:
                break
        captions.append(caption)
    return captions

def getTimestampMapping(whisper_analysis):
    index = 0
    locationToTimestamp = {}
    for segment in whisper_analysis.get('segments', []):
        for word in segment.get('words', []):
            # word['text'] may include leading spaces in some outputs; handle
            wtext = word.get('text', '')
            # newIndex = index + len(word['text']) + 1  (original logic)
            newIndex = index + len(wtext) + 1
            # store mapping from text-char-range -> word end time
            locationToTimestamp[(index, newIndex)] = float(word.get('end', 0.0))
            index = newIndex
    return locationToTimestamp

def cleanWord(word):
    # buang karakter non-alfanumerik (selain beberapa tanda)
    return re.sub(r'[^\w\s\-\_"\'’]', '', word)

def interpolateTimeFromDict(word_position, d):
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return float(value)
    return None

def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15, considerPunctuation=False):
    """
    Convert whisper_analysis -> list of ((start, end), text)
    """
    wordLocationToTime = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0.0
    CaptionsPairs = []
    text = whisper_analysis.get('text', '')

    if considerPunctuation:
        sentences = re.split(r'(?<=[.!?]) +', text)
        words = [word for sentence in sentences for word in splitWordsBySize(sentence.split(), maxCaptionSize)]
    else:
        words = text.split()
        words = [cleanWord(word) for word in splitWordsBySize(words, maxCaptionSize)]

    for word in words:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, wordLocationToTime)
        if end_time is not None and word:
            # append tuple: ((start,end), text)
            CaptionsPairs.append(((float(start_time), float(end_time)), word))
            start_time = end_time

    return CaptionsPairs

def generate_timed_captions(audio_filename: str, model_size: str = "base", fp16: bool = False):
    """
    Main wrapper:
      - load whisper model (load_model(model_size))
      - transcribe_timestamped(...)
      - convert to list of ((start,end), text)

    Returns: list of ((start,end), text)
    """
    if not os.path.exists(audio_filename):
        raise FileNotFoundError(f"Audio file not found: {audio_filename}")

    # load model (this may be slow / use GPU if available)
    model = load_model(model_size)

    # transcribe with timestamped output
    # NOTE: transcribe_timestamped returns a dict-like structure including 'segments' and 'text'
    whisper_analysis = transcribe_timestamped(model, audio_filename, verbose=False, fp16=fp16)

    captions = getCaptionsWithTime(whisper_analysis)
    return captions