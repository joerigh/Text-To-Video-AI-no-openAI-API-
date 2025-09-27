import edge_tts
import asyncio

async def _generate_tts_async(text, output_file):
    communicate = edge_tts.Communicate(text, voice="id-ID-ArdiNeural")
    await communicate.save(output_file)

def generate_audio(text, output_file="audio_tts.wav"):
    asyncio.run(_generate_tts_async(text, output_file))