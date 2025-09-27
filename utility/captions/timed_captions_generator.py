# utils/timed_caption_generator.py

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
    Generate teks caption dengan timing.
    captions bisa berupa list of dict atau list of Caption object.
    """
    captions = normalize_captions(captions)

    output = []
    for cap in captions:
        line = f"[{cap.start:.2f} - {cap.end:.2f}] {cap.text}"
        output.append(line)

    return "\n".join(output)


def text_to_captions(text: str, step: float = 2.0):
    """
    Ubah input teks mentah (string) menjadi list of dict caption.
    step = durasi per baris (default 2 detik).
    """
    lines = text.split("\n")
    captions = []
    for i, line in enumerate(lines):
        if line.strip():
            captions.append({
                "start": i * step,
                "end": (i + 1) * step,
                "text": line.strip()
            })
    return captions


# -----------------------------
# Tes mandiri
if __name__ == "__main__":
    sample_text = "Halo dunia\nIni teks kedua\nBaris ketiga"
    caps = text_to_captions(sample_text, step=2.0)
    print(generate_timed_captions(caps))