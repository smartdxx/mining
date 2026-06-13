import os
import sys
import zipfile
import urllib.request
import subprocess

# --- SOZLAMALAR ---
# Monero (XMR) hamyon manzili (Buni o'zingiznikiga almashtiring)
WALLET_ADDRESS = "Your_Wallet_Address"
# Mayning puli (Pool) - Monero uchun eng barqarorlaridan biri
POOL_URL = "xmr.pool.gntl.co.uk:3333" 
# Mayner nomi (Kompyuteringiz nomi)
WORKER_NAME = "Python_Miner_CPU"

# Fayllar nomi va manzillari
XMRIG_VERSION = "6.21.0"
ZIP_URL = f"https://github.com/xmrig/xmrig/releases/download/v{XMRIG_VERSION}/xmrig-{XMRIG_VERSION}-msvc-win64.zip"
ZIP_NAME = "xmrig.zip"
EXTRACT_DIR = "xmrig_miner"

def download_miner():
    """Tayyor maynerni GitHub-dan yuklab olish"""
    if not os.path.exists(ZIP_NAME) and not os.path.exists(EXTRACT_DIR):
        print("⏳ Mayning dvigateli yuklab olinmoqda (GitHub)... \nBu bir necha daqiqa olishi mumkin.")
        try:
            urllib.request.urlretrieve(ZIP_URL, ZIP_NAME)
            print("✅ Yuklab olindi.")
        except Exception as e:
            print(f"❌ Yuklab olishda xatolik: {e}")
            sys.exit(1)

def extract_miner():
    """Zip arxivni ochish"""
    if os.path.exists(ZIP_NAME) and not os.path.exists(EXTRACT_DIR):
        print("📦 Arxivdan chiqarilmoqda...")
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall(EXTRACT_DIR)
        print("✅ Tayyor.")
        # Keraksiz zip faylni o'chiramiz
        os.remove(ZIP_NAME)

def start_mining():
    """Maynerni parametrlar bilan ishga tushirish"""
    # Ichki jildga kirish (arxiv tuzilishiga qarab)
    inner_path = os.path.join(EXTRACT_DIR, f"xmrig-{XMRIG_VERSION}")
    executable_path = os.path.join(inner_path, "xmrig.exe")
    
    if not os.path.exists(executable_path):
        # Agar jild tuzilishi boshqacha bo'lsa, to'g'ridan-to'g'ri qidiradi
        executable_path = os.path.join(EXTRACT_DIR, "xmrig.exe")

    print("\n🚀 Mayning jarayoni boshlanmoqda!")
    print(f"📋 Pool: {POOL_URL}")
    print(f"💼 Hamyon: {WALLET_ADDRESS[:10]}...{WALLET_ADDRESS[-10:]}")
    print("---------------------------------------------------------")
    print("Diqqat: Mayningni to'xtatish uchun CTRL + C tugmalarini bosing.\n")

    # XMRig buyruqlari (Parametrlar)
    # -o : Pool manzili
    # -u : Hamyon manzili va worker nomi
    # -p : parol (ko'pincha x yoki bo'sh qoldiriladi)
    cmd = [
        executable_path,
        "-o", POOL_URL,
        "-u", f"{WALLET_ADDRESS}.{WORKER_NAME}",
        "-p", "x"
    ]

    try:
        # Maynerni ishga tushiramiz va uning natijasini konsolda ko'rsatamiz
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Mayning foydalanuvchi tomonidan to'xtatildi.")
    except Exception as e:
        print(f"\n❌ Ishga tushirishda xatolik yuz berdi: {e}")

if __name__ == "__main__":
    # 1. Dvigatelni yuklash
    download_miner()
    # 2. Arxivdan ochish
    extract_miner()
    # 3. Mayningni boshlash
    start_mining()