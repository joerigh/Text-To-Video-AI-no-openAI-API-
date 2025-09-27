import asyncio
import edge_tts


async def _generate_audio_async(text: str, output_file: str, voice: str = "en-US-AriaNeural"):
    """
    Generate audio dari teks menggunakan Microsoft Edge TTS.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)


def generate_audio(text: str, output_file: str = "audio_tts.wav", voice: str = "en-US-AriaNeural"):
    """
    Wrapper sinkron supaya bisa dipanggil langsung dari script utama.
    """
    asyncio.run(_generate_audio_async(text, output_file, voice))
    return output_file
