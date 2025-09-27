# utility/script/script_generator.py

def generate_script_manual(user_input_text):
    """
    Fungsi manual: Ambil input script user dan kembalikan dict
    Format sama seperti versi OpenAI, supaya kompatibel dengan app.py
    """
    return {"script": user_input_text.strip()}