import os
from deep_translator import GoogleTranslator
from utility.utils import log_response, LOG_TYPE_GPT
import re

PEXELS_API_KEY = os.environ.get('PEXELS_KEY')

# List stopwords sederhana (extendable)
STOPWORDS = set([
    "di", "dan", "yang", "dari", "ke", "pada", "untuk", "the", "a", "an", "of", "in", "on", "with", "is"
])

def clean_word(word):
    return re.sub(r'[^\w\s]', '', word.lower())

def extract_keywords(sentence, lang='en'):
    """
    Ambil kata penting dan gabungkan menjadi keyword visual (1-2 kata per keyword)
    """
    words = [clean_word(w) for w in sentence.split() if clean_word(w) and clean_word(w) not in STOPWORDS]

    keywords = []
    i = 0
    while i < len(words):
        if i + 1 < len(words):
            keywords.append(f"{words[i]} {words[i+1]}")
            i += 2
        else:
            keywords.append(words[i])
            i += 1

    # Jika bahasa bukan Inggris, translate ke Inggris
    if lang != 'en':
        translated = []
        for kw in keywords:
            try:
                t = GoogleTranslator(source='auto', target='en').translate(kw)
                translated.append(t)
            except:
                translated.append(kw)
        keywords = translated

    return keywords

def getVideoSearchQueriesTimed_manual(script, timed_captions, manual_keywords=[]):
    """
    Generate keywords per caption segment, auto detect language
    manual_keywords optional override
    """
    result = []
    lang_code = 'en'
    try:
        from langdetect import detect
        lang_code = detect(script)
    except:
        lang_code = 'en'

    for idx, ((t1, t2), caption) in enumerate(timed_captions):
        if manual_keywords and idx < len(manual_keywords):
            kws = manual_keywords[idx]
        else:
            kws = extract_keywords(caption, lang=lang_code)
        result.append([[t1, t2], kws])

    return result