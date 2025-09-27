# Easy-Text-To-Video-AI 🎬✨  

**Easy-Text-To-Video-AI** adalah project sederhana yang mengubah teks menjadi video otomatis dengan dukungan:  
- 🎙️ **Text-to-Speech (TTS)** → mengubah naskah jadi suara  
- 📝 **Timed Caption Generator** → membuat subtitle otomatis dengan timestamp  
- 🎥 **MoviePy + FFmpeg** → merangkai audio, teks, dan gambar jadi video  
- 🤖 **OpenAI API** (opsional) → bisa dipakai untuk auto naskah / perbaikan teks  

---

## 📂 Struktur Project
```
Easy-Text-To-Video-AI/
│── main.py
│── requirements.txt
│── .env
│── utils/
│   ├── __init__.py
│   ├── timed_caption_generator.py   # modul subtitle otomatis ✅
│   └── (utility lainnya)
```

---

## ⚙️ Instalasi

1. **Clone repository**  
   ```bash
   git clone https://github.com/username/Easy-Text-To-Video-AI.git
   cd Easy-Text-To-Video-AI
   ```

2. **Buat environment (opsional tapi direkomendasikan)**  
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg** (wajib)  
   - **Windows**: download dari https://ffmpeg.org/download.html → tambahkan ke PATH  
   - **Linux/Mac**:  
     ```bash
     sudo apt install ffmpeg   # Ubuntu/Debian
     brew install ffmpeg       # Mac (Homebrew)
     ```

5. **Buat file `.env`** (untuk API key OpenAI / TTS)  
   ```
   OPENAI_API_KEY=sk-xxxxxxxx
   ```

---

## 🚀 Cara Menjalankan

### 1. Jalankan script utama
```bash
python main.py
```

### 2. Input naskah
- Bisa ketik langsung di terminal / UI (jika pakai Streamlit).  
- Atau buat file `naskah.txt` lalu load di `main.py`.

### 3. Hasil
- File video otomatis tersimpan di folder `output/` dengan audio + subtitle.

---

## 📝 Fitur Timed Caption Generator

Di `utils/timed_caption_generator.py` tersedia fungsi untuk membuat subtitle otomatis dengan timestamp.

### Contoh penggunaan:
```python
from utils.timed_caption_generator import generate_timed_captions

captions = [
    {"start": 0.0, "end": 2.0, "text": "Halo dunia"},
    {"start": 2.1, "end": 4.0, "text": "Ini teks kedua"},
]

timed_text = generate_timed_captions(captions)
print(timed_text)
```

### Output:
```
[0.00 - 2.00] Halo dunia
[2.10 - 4.00] Ini teks kedua
```

---

## 📌 Catatan
- Pastikan **FFmpeg** sudah bisa dipanggil dari terminal (`ffmpeg -version`).  
- Kalau error `AttributeError: 'dict' object has no attribute 'start'`, sekarang sudah fix: modul akan otomatis mengubah dict jadi object.  

---

## 👨‍💻 Kontribusi
Pull Request terbuka untuk fitur baru seperti:  
- Support video background otomatis  
- Auto translate subtitle  
- Export subtitle ke `.srt`

---

## 📜 Lisensi
MIT License © 2025  
