import edge_tts
from langdetect import detect

async def generate_audio(text, outputFilename):
    # Auto detect language
    lang = detect(text)
    voice = "en-AU-WilliamNeural" if lang == "en" else "id-ID-GadisNeural"
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(outputFilename)