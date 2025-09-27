import edge_tts
import asyncio

async def generate_audio(text, output_file="audio_tts.wav", voice="id-ID-ArdiNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Audio berhasil dibuat: {output_file}")