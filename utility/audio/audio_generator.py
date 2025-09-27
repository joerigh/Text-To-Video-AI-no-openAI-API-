import edge_tts
import asyncio

async def generate_audio(script_text, output_file):
    tts = edge_tts.Communicate(script_text, "id-ID-AriaNeural")
    await tts.save(output_file)