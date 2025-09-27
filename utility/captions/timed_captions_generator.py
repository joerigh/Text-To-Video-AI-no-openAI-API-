class Caption:
    def __init__(self, start, end, text):
        self.start = start
        self.end = end
        self.text = text

def normalize_captions(captions):
    """
    Pastikan semua caption punya atribut .start, .end, .text
    meskipun awalnya berbentuk dict.
    """
    normalized = []
    for cap in captions:
        if isinstance(cap, dict):  # kalau dict -> ubah ke object
            normalized.append(Caption(
                cap.get("start", 0.0),
                cap.get("end", 0.0),
                cap.get("text", "")
            ))
        else:  # kalau sudah object, langsung pakai
            normalized.append(cap)
    return normalized

def generate_timed_captions(captions):
    """
    Contoh fungsi utama untuk mengenerate caption dengan timing.
    captions bisa berupa list of dict atau list of Caption object.
    """
    captions = normalize_captions(captions)

    output = []
    for cap in captions:
        line = f"[{cap.start:.2f} - {cap.end:.2f}] {cap.text}"
        output.append(line)

    return "\n".join(output)


# -----------------------------
# Contoh penggunaan
if __name__ == "__main__":
    sample_captions = [
        {"start": 0.0, "end": 2.0, "text": "Halo dunia"},
        {"start": 2.1, "end": 4.0, "text": "Ini teks kedua"},
    ]

    print(generate_timed_captions(sample_captions))