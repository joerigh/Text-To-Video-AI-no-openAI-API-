import os
import re
from whisper_timestamped import load_model, transcribe_timestamped

def splitWordsBySize(words, maxCaptionSize):
    half = maxCaptionSize / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= maxCaptionSize:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= half and words:
                break
        captions.append(caption)
    return captions

def getTimestampMapping(whisper_analysis):
    index = 0
    mapping = {}
    for seg in whisper_analysis.get('segments', []):
        for word in seg.get('words', []):
            wtext = word.get('text', '')
            new_index = index + len(wtext) + 1
            mapping[(index, new_index)] = float(word.get('end', 0))
            index = new_index
    return mapping

def cleanWord(word):
    return re.sub(r'[^\w\s\-\_"\'’]', '', word)

def interpolateTimeFromDict(pos, d):
    for key, value in d.items():
        if key[0] <= pos <= key[1]:
            return float(value)
    return None

def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15):
    word_to_time = getTimestampMapping(whisper_analysis)
    position = 0
    start_time = 0
    captions_pairs = []
    text = whisper_analysis.get('text', '')
    words = text.split()
    words = [cleanWord(w) for w in splitWordsBySize(words, maxCaptionSize)]

    for word in words:
        position += len(word) + 1
        end_time = interpolateTimeFromDict(position, word_to_time)
        if end_time is not None and word:
            captions_pairs.append(((start_time, end_time), word))
            start_time = end_time
    return captions_pairs

def generate_timed_captions(audio_filename, model_size="base", fp16=False):
    if not os.path.exists(audio_filename):
        raise FileNotFoundError(f"{audio_filename} tidak ditemukan")
    model = load_model(model_size)
    analysis = transcribe_timestamped(model, audio_filename, verbose=False, fp16=fp16)
    return getCaptionsWithTime(analysis)