import sys
import subprocess
import importlib.util

def install_package(package):
    """Install package via pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def check_module(module_name):
    """Check if module can be imported."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None

def install_ffmpeg():
    """Install ffmpeg if on Termux/Linux."""
    import platform, os
    system = platform.system()
    if system == "Linux":
        if os.path.exists("/data/data/com.termux/files/usr/bin/pkg"):
            # Termux
            subprocess.call(["pkg", "install", "-y", "ffmpeg"])
        else:
            # Debian/Ubuntu
            subprocess.call(["sudo", "apt", "update"])
            subprocess.call(["sudo", "apt", "install", "-y", "ffmpeg"])
    elif system == "Darwin":
        # MacOS (brew)
        subprocess.call(["brew", "install", "ffmpeg"])
    else:
        print("Pastikan ffmpeg sudah terinstall secara manual di Windows.")

def main():
    print("=== Install/Upgrade pip ===")
    install_package("pip")

    print("=== Install MoviePy ===")
    install_package("moviepy")

    print("=== Install ffmpeg jika perlu ===")
    install_ffmpeg()

    print("=== Cek import moviepy.editor ===")
    try:
        import moviepy.editor as mpy
        print("✅ MoviePy OK! moviepy.editor sudah bisa diimport.")
    except ModuleNotFoundError:
        print("❌ Masih error: moviepy.editor tidak ditemukan!")

if __name__ == "__main__":
    main()