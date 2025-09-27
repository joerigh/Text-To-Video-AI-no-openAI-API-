# video_search_query_generator.py (deep-translator version)
from deep_translator import GoogleTranslator
from utility.utils import log_response, LOG_TYPE_SCRIPT
import re
from collections import Counter

def getVideoSearchQueriesTimed_manual(script, captions_timed, keywords_manual=None):
    timed_keywords = []
    for i, ((t1, t2), caption_text) in enumerate(captions_timed):
        if keywords_manual and i < len(keywords_manual):
            kws = keywords_manual[i]
        else:
            kws = extract_keywords_from_text(caption_text)
        kws_en = [translate_to_english(kw) for kw in kws]
        timed_keywords.append([[t1, t2], kws_en])
    log_response(LOG_TYPE_SCRIPT, script, timed_keywords)
    return timed_keywords

def extract_keywords_from_text(text, top_n=5):
    words = re.findall(r'\b\w+\b', text.lower())
    stopwords = set(["the","and","is","are","a","of","to","in","for","with","that","on","as","by","at"])
    words = [w for w in words if w not in stopwords]
    counts = Counter(words)
    keywords = [w for w,_ in counts.most_common(top_n)]
    return keywords

def translate_to_english(word):
    try:
        return GoogleTranslator(source='auto', target='en').translate(word)
    except:
        return word