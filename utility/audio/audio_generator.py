import edge_tts
import asyncio
from langdetect import detect

async def generate_audio(text, outputFilename, auto_detect=True):
    """
    Generate TTS audio using edge-tts.

    Parameters:
    - text: script teks
    - outputFilename: file output mp3
    - auto_detect: jika True, voice akan dipilih sesuai bahasa (ID/EN)
    """

    # Pilih voice
    if auto_detect:
        lang_code = detect(text)  # 'id' = Indonesian, 'en' = English
        voice = "id-ID-GadisNeural" if lang_code == "id" else "en-AU-WilliamNeural"
    else:
        voice = "en-AU-WilliamNeural"

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(outputFilename)