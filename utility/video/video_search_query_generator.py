def getVideoSearchQueriesTimed(script_text, timed_captions):
    # Sederhana: ambil beberapa kata penting dari naskah
    search_terms = []
    for segment in timed_captions:
        _, _, text = segment
        words = text.split()
        if words:
            search_terms.append(words[0])
    return search_terms

def merge_empty_intervals(video_urls):
    # Implementasi sederhana
    return video_urls