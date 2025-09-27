
import edge_tts
import asyncio

async def generate_audio(text, outputFilename, voice="en-AU-WilliamNeural"):
    """
    Generate TTS audio using edge-tts.

    Parameters:
        text (str): Text to convert to speech
        outputFilename (str): Path to save mp3
        voice (str): Voice name, e.g., 'en-AU-WilliamNeural' or 'id-ID-GadisNeural'
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(outputFilename)

# Helper function for synchronous calls
def generate_audio_sync(text, outputFilename, voice="en-AU-WilliamNeural"):
    asyncio.run(generate_audio(text, outputFilename, voice))