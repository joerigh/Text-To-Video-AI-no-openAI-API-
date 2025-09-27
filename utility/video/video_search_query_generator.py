# utility/video/video_searc_query_generator.py

import os
from googletrans import Translator
from utility.utils import log_response, LOG_TYPE_SCRIPT

translator = Translator()

def getVideoSearchQueriesTimed_manual(script, captions_timed, keywords_manual=None):
    """
    Prepare timed keywords for video search.
    - captions_timed: output dari generate_timed_captions
    - keywords_manual: list of list, optional, per caption segment
    Output: list [ [ [t1, t2], [kw1, kw2, ...] ], ... ]
    """

    timed_keywords = []

    for i, ((t1, t2), caption_text) in enumerate(captions_timed):
        # Jika ada input manual keyword
        if keywords_manual and i < len(keywords_manual):
            kws = keywords_manual[i]
        else:
            # Auto extract keywords dari caption text
            kws = extract_keywords_from_text(caption_text)
        # Translate ke bahasa Inggris
        kws_en = [translate_to_english(kw) for kw in kws]
        timed_keywords.append([[t1, t2], kws_en])

    # Logging
    log_response(LOG_TYPE_SCRIPT, script, timed_keywords)
    return timed_keywords

# -------------------------
# Helper functions
# -------------------------

import re
from collections import Counter

def extract_keywords_from_text(text, top_n=5):
    # Bersihkan tanda baca
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(["the","and","is","are","a","of","to","in","for","with","that","on","as","by","at"])
    words = [w for w in words if w not in stopwords]
    counts = Counter(words)
    keywords = [w for w,_ in counts.most_common(top_n)]
    return keywords

def translate_to_english(word):
    try:
        trans = translator.translate(word, src='auto', dest='en').text
        return trans
    except:
        return word