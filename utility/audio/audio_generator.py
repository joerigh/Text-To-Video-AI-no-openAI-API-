import edge_tts
import asyncio

async def generate_audio(text, outputFilename, voice="en-AU-WilliamNeural"):
    """
    Generate TTS audio using edge-tts.
    voice: pilih voice sesuai bahasa ('en-AU-WilliamNeural' atau 'id-ID-GadisNeural')
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(outputFilename)