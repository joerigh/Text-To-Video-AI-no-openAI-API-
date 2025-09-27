# utility/captions/timed_caption_generator.py

import whisper_timestamped as whisper
from whisper_timestamped import load_model, transcribe_timestamped
import re

def generate_timed_captions(audio_filename, model_size="base"):
    """
    Generate timed captions from audio file using whisper-timestamped.
    Returns: list of tuples [((start_time, end_time), text), ...]
    """
    WHISPER_MODEL = load_model(model_size)
    result = transcribe_timestamped(WHISPER_MODEL, audio_filename, verbose=False, fp16=False)
    return get_captions_with_time(result)

# -------------------------
# Helper functions
# -------------------------

def split_words_by_size(words, max_caption_size):
    half_caption_size = max_caption_size / 2
    captions = []
    while words:
        caption = words[0]
        words = words[1:]
        while words and len(caption + ' ' + words[0]) <= max_caption_size:
            caption += ' ' + words[0]
            words = words[1:]
            if len(caption) >= half_caption_size and words:
                break
        captions.append(caption)
    return captions

def get_timestamp_mapping(whisper_analysis):
    index = 0
    location_to_timestamp = {}
    for segment in whisper_analysis['segments']:
        for word in segment['words']:
            new_index = index + len(word['text']) + 1
            location_to_timestamp[(index, new_index)] = word['end']
            index = new_index
    return location_to_timestamp

def clean_word(word):
    return re.sub(r'[^\w\s\-_"\'\']', '', word)

def interpolate_time_from_dict(word_position, d):
    for key, value in d.items():
        if key[0] <= word_position <= key[1]:
            return value
    return None

def get_captions_with_time(whisper_analysis, max_caption_size=15, consider_punctuation=False):
    word_loc_to_time = get_timestamp_mapping(whisper_analysis)
    position = 0
    start_time = 0
    captions_pairs = []
    text = whisper_analysis['text']

    if consider_punctuation:
        sentences = re.split(r'(?<=[.!?]) +', text)
        words = [word for sentence in sentences for word in split_words_by_size(sentence.split(), max_caption_size)]
    else:
        words = text.split()
        words = [clean_word(word) for word in split_words_by_size(words, max_caption_size)]

    for word in words:
        position += len(word) + 1
        end_time = interpolate_time_from_dict(position, word_loc_to_time)
        if end_time and word:
            captions_pairs.append(((start_time, end_time), word))
            start_time = end_time

    return captions_pairs