Text-To-Video AI (Tanpa OpenAI)




Buat video dari naskah/storyboard tanpa OpenAI.

Audio: edge-tts

Timed captions: whisper-timestamped

Background video: Pexels

Render video: MoviePy

Bisa dijalankan via Terminal atau Streamlit GUI



---

🔹 Fitur Utama

Input naskah manual atau dari file .txt

Generate audio TTS dari naskah

Generate timed captions otomatis

Cari dan gunakan background video dari Pexels

Render video final (rendered_video.mp4) di lokal



---

💻 Instalasi

1. Clone repositori:



git clone <repo-url>
cd Text-To-Video-NoOpenAI

2. Install dependencies:



pip install -r requirements.txt

3. Install ImageMagick agar TextClip MoviePy berjalan:



Linux: sudo apt install imagemagick

Windows: download installer ImageMagick



---

🚀 Cara Pakai

1. Terminal / Command Line

python main.py

Pilih input naskah: file naskah.txt atau manual

Video final akan tersimpan sebagai rendered_video.mp4


2. Streamlit GUI

streamlit run main_streamlit.py

Masukkan naskah di text area

Klik Generate Video

Video final akan muncul langsung di browser



---

⚙️ Konfigurasi

Pexels API Key: masukkan di main.py


PEXELS_API_KEY = "YOUR_PEXELS_API_KEY"

File naskah opsional: naskah.txt



---

📂 Struktur Folder

Text-To-Video-NoOpenAI/
├── main.py
├── main_streamlit.py
├── naskah.txt
├── requirements.txt
└── utility/
    ├── audio/
    │   └── audio_generator.py
    ├── captions/
    │   └── timed_captions_generator.py
    ├── video/
    │   ├── background_video_generator.py
    │   └── video_search_query_generator.py
    └── render/
        └── render_engine.py


---

⚠️ Catatan

Semua rendering terjadi di lokal

Background video diambil dari Pexels

Tidak ada OpenAI API, semua naskah bisa input manual



---