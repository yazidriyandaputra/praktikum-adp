from os import system as clear_cmd
from os import name as os_name
from os.path import exists
import time
import random
from termcolor import colored, cprint
import pygame
import pyfiglet
import sys

# Konstanta
SAVE_FILE = "harvest_moon.txt"
MUSIC_FILE = "Harvest Moon_ Back to Nature  Spring  OST.mp3"
INTRO_MUSIC_FILE = "Harvest Moon_ Back to Nature  Opening  OST.mp3"

UANG_AWAL = 10
BIBIT_APEL_AWAL = 3
UKURAN_LAHAN_BARIS_AWAL = 2
UKURAN_LAHAN_KOLOM_AWAL = 2
KAPASITAS_AIR_AWAL = 4
UKURAN_LAHAN_MAKSIMAL = 5
KAPASITAS_AIR_MAKSIMAL = 15
BIAYA_UPGRADE_AIR = 75
PENGALI_BIAYA_PERLUASAN = 10
PINJAMAN_MAKSIMAL = 20

HARGA_BIBIT = {"apel": 5, "tomat": 12, "lettuce": 20}
HARGA_JUAL = {"apel": 2, "tomat": 4, "lettuce": 10}
HARI_TUMBUH = {"apel": 2, "tomat": 3, "lettuce": 4}
EMOJI_TANAMAN = {"apel": "🍎", "tomat": "🍅", "lettuce": "🥬"}

# Panjang header
TEXT_HEADER = "HARVEST MOON"
PANJANG_HEADER = 72

def bersihkan_layar():
    """Membersihkan layar terminal"""
    clear_cmd('cls' if os_name == 'nt' else 'clear')

def tampilkan_header(teks):
    """Menampilkan header dengan panjang konsisten"""
    cprint(f"\n{'=' * PANJANG_HEADER}", 'yellow')
    cprint(f"{teks.center(PANJANG_HEADER)}", 'yellow', attrs=['bold'])
    cprint(f"{'=' * PANJANG_HEADER}", 'yellow')

def tampilkan_pesan(teks, status="info"):
    """Menampilkan pesan dengan ikon dan warna yang sesuai"""
    if status == "success":
        cprint(f"✅ {teks}", 'green')
    elif status == "error":
        cprint(f"❌ {teks}", 'red')
    elif status == "info":
        cprint(f"ℹ {teks}", 'cyan')

def tekan_enter():
    """Menjeda permainan dan menunggu Enter"""
    cprint("\n[ Tekan Enter untuk melanjutkan... ]", 'white', 'on_grey')
    input()

def mainkan_musik_intro():
    """Memainkan musik intro jika tersedia"""
    try:
        if exists(INTRO_MUSIC_FILE):
            pygame.mixer.music.load(INTRO_MUSIC_FILE)
            pygame.mixer.music.play(-1)
            return True
    except Exception as e:
        tampilkan_pesan(f"Error memainkan musik intro: {str(e)}", "error")
    return False

def inisialisasi_musik():
    """Menginisialisasi musik latar"""
    try:
        if not exists(MUSIC_FILE):
            tampilkan_pesan(f"Peringatan: File musik '{MUSIC_FILE}' tidak ditemukan.", "error")
            return False
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        return True
    except Exception as e:
        tampilkan_pesan(f"Error inisialisasi musik: {str(e)}", "error")
        return False

def toggle_musik(data_pemain, musik_tersedia):
    """Menyalakan/mematikan musik"""
    if not musik_tersedia:
        tampilkan_pesan("Fungsi musik tidak tersedia.", "error")
        return
    if data_pemain.get("musik_nyala", False):
        pygame.mixer.music.stop()
        data_pemain["musik_nyala"] = False
        tampilkan_pesan("Musik dimatikan. 🔇", "info")
    else:
        pygame.mixer.music.play(loops=-1)
        data_pemain["musik_nyala"] = True
        tampilkan_pesan("Musik dinyalakan. 🎵", "info")

def game_baru():
    """Membuat data game baru"""
    lahan_awal = [[None] * UKURAN_LAHAN_KOLOM_AWAL for _ in range(UKURAN_LAHAN_BARIS_AWAL)]
    return {
        "uang": UANG_AWAL,
        "bibit": {"apel": BIBIT_APEL_AWAL, "tomat": 0, "lettuce": 0},
        "inventaris": {},
        "baris_lahan": UKURAN_LAHAN_BARIS_AWAL,
        "kolom_lahan": UKURAN_LAHAN_KOLOM_AWAL,
        "lahan": lahan_awal,
        "hari": 1,
        "hutang": 0,
        "kapasitas_air": KAPASITAS_AIR_AWAL,
        "sisa_air": KAPASITAS_AIR_AWAL,
        "tomat_terbuka": False,
        "lettuce_terbuka": False,
        "musik_nyala": True,
    }

def simpan_game(data_pemain):
    """Menyimpan progress game"""
    with open(SAVE_FILE, 'w') as f:
        for key, value in data_pemain.items():
            f.write(f"{key}:{repr(value)}\n")

def muat_game():
    """Memuat progress game"""
    if not exists(SAVE_FILE):
        return None
    data_pemain = {}
    with open(SAVE_FILE, 'r') as f:
        for line in f:
            if ':' in line:
                key, value_str = line.strip().split(':', 1)
                try:
                    data_pemain[key] = eval(value_str)
                except Exception:
                    tampilkan_pesan(f"Peringatan: data '{key}' rusak dan diabaikan.", "error")
                    continue
    return data_pemain

def tampilkan_lahan(data_pemain):
    """Menampilkan kondisi lahan"""
    tampilkan_header("🏡 LAHANMU 🏡")
    cprint(f"Sisa Air Hari Ini: {data_pemain['sisa_air']}/{data_pemain['kapasitas_air']} 💧", 'blue')
    
    for i in range(data_pemain["baris_lahan"]):
        baris_tampilan = []
        for j in range(data_pemain["kolom_lahan"]):
            tanaman = data_pemain["lahan"][i][j]
            if tanaman is None:
                tampilan_str = colored("[🟫]", 'white', 'on_grey')
            else:
                hari_tersisa = tanaman["hari_tumbuh"]
                emoji_tanaman = EMOJI_TANAMAN.get(tanaman["nama"], "❓")
                status_air = "" if tanaman.get("disiram") else colored("🚱", 'red')
                if hari_tersisa <= 0:
                    tampilan_str = colored(f"[{emoji_tanaman}P]", 'green', attrs=['bold'])
                elif hari_tersisa == HARI_TUMBUH.get(tanaman["nama"]):
                    tampilan_str = colored(f"[.🌱{status_air}]", 'yellow')
                else:
                    tampilan_str = colored(f"[🌿{status_air}]", 'cyan')
            baris_tampilan.append(tampilan_str)
        print(" ".join(baris_tampilan) + f"  Baris {i+1}")
    
    print("\n" + " ".join([f" Kol {k+1} " for k in range(data_pemain['kolom_lahan'])]))
    cprint("\nKeterangan: 🟫Kosong, .🌱Bibit, 🌿Tunas, P-Panen, 🚱Belum Disiram", 'grey')

def tanam_bibit(data_pemain):
    """Menanam bibit di lahan"""
    bersihkan_layar()
    tampilkan_lahan(data_pemain)
    tampilkan_header("🌱 TANAM BIBIT 🌱")
    
    if not any(v > 0 for v in data_pemain["bibit"].values()):
        tampilkan_pesan("Kamu tidak punya bibit!", "error")
        return False
    
    tampilkan_pesan("Bibit yang kamu miliki:", "info")
    for bibit, jumlah in data_pemain["bibit"].items():
        if jumlah > 0:
            print(f" - {EMOJI_TANAMAN.get(bibit, '')} {bibit.capitalize()}: {jumlah}")
    
    try:
        baris = int(input(f"\nPilih baris (1-{data_pemain['baris_lahan']}) atau 0 untuk batal: ")) - 1
        if baris == -1:
            return False
        kolom = int(input(f"Pilih kolom (1-{data_pemain['kolom_lahan']}): ")) - 1
        bibit_ditanam = input("Pilih bibit yang ingin ditanam: ").lower()
        
        if bibit_ditanam not in data_pemain["bibit"] or data_pemain["bibit"][bibit_ditanam] <= 0:
            tampilkan_pesan(f"Kamu tidak punya bibit {bibit_ditanam}!", "error")
            return False
            
        if not (0 <= baris < data_pemain["baris_lahan"] and 0 <= kolom < data_pemain["kolom_lahan"]):
            tampilkan_pesan("Lokasi tidak valid!", "error")
            return False
            
        if data_pemain["lahan"][baris][kolom] is not None:
            tampilkan_pesan("Lokasi ini sudah terisi!", "error")
            return False
            
        data_pemain["lahan"][baris][kolom] = {
            "nama": bibit_ditanam,
            "hari_tumbuh": HARI_TUMBUH[bibit_ditanam],
            "disiram": False
        }
        data_pemain["bibit"][bibit_ditanam] -= 1
        tampilkan_pesan(f"Berhasil menanam {bibit_ditanam} di ({baris+1}, {kolom+1})!", "success")
        return True
        
    except ValueError:
        tampilkan_pesan("Masukkan angka yang valid!", "error")
        return False

def siram_tanaman(data_pemain):
    """Menyiram tanaman di lahan"""
    while True:
        bersihkan_layar()
        tampilkan_lahan(data_pemain)
        tampilkan_header("💧 MENYIRAM TANAMAN 💧")
        
        if data_pemain["sisa_air"] <= 0:
            tampilkan_pesan("Air kamu sudah habis hari ini!", "error")
            time.sleep(2)
            break
            
        tampilkan_pesan(f"Sisa air: {data_pemain['sisa_air']}/{data_pemain['kapasitas_air']}", "info")
        print("Pilih tanaman untuk disiram (masukkan 0 untuk selesai)")
        
        try:
            baris = int(input(f"Baris (1-{data_pemain['baris_lahan']}): ")) - 1
            if baris == -1:
                break
            kolom = int(input(f"Kolom (1-{data_pemain['kolom_lahan']}): ")) - 1
            
            if not (0 <= baris < data_pemain["baris_lahan"] and 0 <= kolom < data_pemain["kolom_lahan"]):
                tampilkan_pesan("Lokasi tidak valid!", "error")
                time.sleep(1)
                continue
                
            tanaman = data_pemain["lahan"][baris][kolom]
            if not tanaman:
                tampilkan_pesan("Tidak ada tanaman di sini!", "error")
                time.sleep(1)
                continue
                
            if tanaman.get("disiram"):
                tampilkan_pesan("Tanaman ini sudah disiram!", "info")
                time.sleep(1)
                continue
                
            tanaman["disiram"] = True
            data_pemain["sisa_air"] -= 1
            tampilkan_pesan(f"Berhasil menyiram {tanaman['nama']} di ({baris+1}, {kolom+1})!", "success")
            time.sleep(1)
            
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            time.sleep(1)

def tidur(data_pemain):
    """Memajukan waktu ke hari berikutnya dan mengembalikan notifikasi tanaman layu"""
    tampilkan_header("🌙 WAKTUNYA TIDUR 🌙")
    cprint("Selamat malam...", 'grey')
    time.sleep(1.5)
    cprint("ZzzZzz...", 'grey')
    time.sleep(1.5)
    bersihkan_layar()
    
    # Pergantian hari
    data_pemain["hari"] += 1
    data_pemain["sisa_air"] = data_pemain["kapasitas_air"]
    
    # Pertumbuhan dan layu tanaman
    notifikasi_layu = []
    for idx_baris, baris in enumerate(data_pemain["lahan"]):
        for idx_kolom, tanaman in enumerate(baris):
            if tanaman:
                if tanaman.get("disiram"):
                    tanaman["hari_tumbuh"] -= 1
                    tanaman["disiram"] = False
                else:
                    notifikasi_layu.append(
                        f"Pak Budi 😢: Tanaman {tanaman['nama']} di ({idx_baris+1},{idx_kolom+1}) layu karena tidak disiram."
                    )
                    data_pemain["lahan"][idx_baris][idx_kolom] = None

    tampilkan_pesan(f"Selamat pagi! Hari ke-{data_pemain['hari']} dimulai.", "success")
    tampilkan_pesan(f"Air telah diisi ulang ({data_pemain['kapasitas_air']} 💧).", "info")
    return notifikasi_layu

def panen(data_pemain):
    """Memanen tanaman yang sudah siap"""
    tampilkan_header("🧺 WAKTU PANEN 🧺")
    ada_panen = False
    
    for i in range(data_pemain["baris_lahan"]):
        for j in range(data_pemain["kolom_lahan"]):
            tanaman = data_pemain["lahan"][i][j]
            if tanaman and tanaman["hari_tumbuh"] <= 0:
                ada_panen = True
                nama_tanaman = tanaman["nama"]
                jumlah = random.randint(2, 5)
                data_pemain["inventaris"][nama_tanaman] = data_pemain["inventaris"].get(nama_tanaman, 0) + jumlah
                tampilkan_pesan(f"Kamu memanen {jumlah} {EMOJI_TANAMAN.get(nama_tanaman, '')} {nama_tanaman}!", "success")
                data_pemain["lahan"][i][j] = None
                
                # Membuka bibit baru
                if nama_tanaman == "apel" and not data_pemain.get("tomat_terbuka", False):
                    data_pemain["tomat_terbuka"] = True
                    tampilkan_pesan("Kamu membuka bibit Tomat baru!", "info")
                elif nama_tanaman == "tomat" and not data_pemain.get("lettuce_terbuka", False):
                    data_pemain["lettuce_terbuka"] = True
                    tampilkan_pesan("Kamu membuka bibit Lettuce baru!", "info")
    
    if not ada_panen:
        tampilkan_pesan("Tidak ada tanaman yang siap panen.", "error")

def tampilkan_inventaris(data_pemain):
    """Menampilkan inventaris pemain"""
    tampilkan_header("🎒 INVENTARIS 🎒")
    tampilkan_pesan(f"Uang: ${data_pemain['uang']} 💰 | Hutang: ${data_pemain['hutang']} 🏦", "info")
    
    cprint("\n--- Kantong Bibit ---", attrs=['bold'])
    bibit_dimiliki = {b: j for b, j in data_pemain["bibit"].items() if j > 0}
    if not bibit_dimiliki:
        print("Kosong.")
    else:
        for bibit, jumlah in bibit_dimiliki.items():
            print(f" - {EMOJI_TANAMAN.get(bibit, '')} {bibit.capitalize()}: {jumlah} buah")
    
    cprint("\n--- Keranjang Panen ---", attrs=['bold'])
    if not data_pemain["inventaris"]:
        print("Kosong.")
    else:
        for item, jumlah in data_pemain["inventaris"].items():
            print(f" - {EMOJI_TANAMAN.get(item, '')} {item.capitalize()}: {jumlah} buah")

def jual_hasil(data_pemain):
    """Menjual hasil panen"""
    tampilkan_header("💸 JUAL HASIL PANEN 💸")
    if not data_pemain["inventaris"]:
        tampilkan_pesan("Keranjang panenmu kosong!", "error")
        return
    
    tampilkan_pesan("Isi keranjang panenmu:", "info")
    for item, jumlah in data_pemain["inventaris"].items():
        print(f"- {EMOJI_TANAMAN.get(item, '')} {item.capitalize()}: {jumlah} (Harga: ${HARGA_JUAL[item]}/buah)")
    
    item_dijual = input("\nApa yang ingin kamu jual? (atau 'batal'): ").lower()
    if item_dijual == 'batal':
        return
        
    if item_dijual in data_pemain["inventaris"] and data_pemain["inventaris"][item_dijual] > 0:
        try:
            jumlah = int(input(f"Berapa banyak {item_dijual}? "))
            if 0 < jumlah <= data_pemain["inventaris"][item_dijual]:
                pendapatan = HARGA_JUAL[item_dijual] * jumlah
                data_pemain["uang"] += pendapatan
                data_pemain["inventaris"][item_dijual] -= jumlah
                if data_pemain["inventaris"][item_dijual] == 0:
                    del data_pemain["inventaris"][item_dijual]
                tampilkan_pesan(f"Berhasil menjual {jumlah} {item_dijual} dan dapat ${pendapatan}!", "success")
            else:
                tampilkan_pesan("Jumlah tidak valid.", "error")
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")
    else:
        tampilkan_pesan("Item tidak ada di inventaris.", "error")

def perluas_lahan(data_pemain):
    """Memperluas lahan pertanian"""
    tampilkan_header("🏞️ PERLUAS LAHAN 🏞️")
    if data_pemain["baris_lahan"] >= UKURAN_LAHAN_MAKSIMAL:
        tampilkan_pesan("Lahanmu sudah maksimal!", "info")
        return
        
    biaya = (data_pemain["baris_lahan"] * data_pemain["kolom_lahan"]) * PENGALI_BIAYA_PERLUASAN
    ukuran_baru = f"{data_pemain['baris_lahan'] + 1}x{data_pemain['kolom_lahan'] + 1}"
    tampilkan_pesan(f"Biaya perluasan menjadi {ukuran_baru} adalah ${biaya}", "info")
    
    pilihan = input("Perluas lahan? (y/n) ").lower()
    if pilihan == 'y':
        if data_pemain["uang"] >= biaya:
            data_pemain["uang"] -= biaya
            data_pemain["baris_lahan"] += 1
            data_pemain["kolom_lahan"] += 1
            
            # Membuat lahan baru yang lebih besar
            lahan_lama = data_pemain["lahan"]
            lahan_baru = [[None] * data_pemain["kolom_lahan"] for _ in range(data_pemain["baris_lahan"])]
            
            # Menyalin tanaman dari lahan lama
            for i in range(len(lahan_lama)):
                for j in range(len(lahan_lama[0])):
                    lahan_baru[i][j] = lahan_lama[i][j]
                    
            data_pemain["lahan"] = lahan_baru
            tampilkan_pesan("Lahan berhasil diperluas!", "success")
        else:
            tampilkan_pesan("Uang tidak cukup.", "error")

def bank(data_pemain):
    """Menu transaksi bank"""
    tampilkan_header("🏦 BANK WAKANDA 🏦")
    tampilkan_pesan(f"Hutangmu saat ini: ${data_pemain['hutang']}", "info")
    print("\n1. 💵 Pinjam Uang\n2. 🧾 Bayar Hutang\n3. 🔙 Kembali")
    
    pilihan = input("> ")
    if pilihan == '1':
        if data_pemain["hutang"] > 0:
            tampilkan_pesan("LUNASI dulu hutang sebelumnya!", "error")
            return
            
        try:
            jumlah = int(input(f"Jumlah pinjaman (maks ${PINJAMAN_MAKSIMAL}): "))
            if 0 < jumlah <= PINJAMAN_MAKSIMAL:
                data_pemain["uang"] += jumlah
                data_pemain["hutang"] += jumlah
                tampilkan_pesan(f"Berhasil meminjam ${jumlah}.", "success")
            else:
                tampilkan_pesan(f"Jumlah pinjaman tidak valid.", "error")
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            
    elif pilihan == '2':
        if data_pemain["hutang"] == 0:
            tampilkan_pesan("Kamu tidak punya hutang.", "info")
            return
            
        try:
            jumlah = int(input(f"Jumlah pembayaran (maks ${data_pemain['hutang']}): "))
            if 0 < jumlah <= data_pemain["uang"]:
                bayar = min(jumlah, data_pemain["hutang"])
                data_pemain["uang"] -= bayar
                data_pemain["hutang"] -= bayar
                tampilkan_pesan(f"Berhasil membayar hutang ${bayar}.", "success")
            else:
                tampilkan_pesan("Uang tidak cukup atau jumlah tidak valid.", "error")
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")

def pasar(data_pemain):
    """Menu pasar untuk membeli bibit dan upgrade"""
    while True:
        bersihkan_layar()
        tampilkan_header("🛒 PASAR 🛒")
        tampilkan_pesan(f"Uangmu saat ini: ${data_pemain['uang']} 💰", "info")
        print("\n1. Beli Bibit Tanaman 🌱\n2. Upgrade Kapasitas Air 💧\n3. Selesai")
        
        pilihan = input("> ")
        if pilihan == '1':
            bersihkan_layar()
            tampilkan_header("🌱 BELI BIBIT 🌱")
            for bibit, harga in HARGA_BIBIT.items():
                if (bibit == "tomat" and not data_pemain.get("tomat_terbuka")) or \
                   (bibit == "lettuce" and not data_pemain.get("lettuce_terbuka")):
                    continue
                print(f"- {EMOJI_TANAMAN.get(bibit, '')} {bibit.capitalize()}: ${harga}")
            
            bibit_dibeli = input("\nApa yang ingin kamu beli? (atau 'batal'): ").lower()
            if bibit_dibeli == 'batal':
                continue
                
            if bibit_dibeli in HARGA_BIBIT:
                # Cek apakah bibit sudah terbuka
                if (bibit_dibeli == "tomat" and not data_pemain.get("tomat_terbuka")) or \
                   (bibit_dibeli == "lettuce" and not data_pemain.get("lettuce_terbuka")):
                    tampilkan_pesan("Bibit tidak tersedia atau belum terbuka.", "error")
                    tekan_enter()
                    break
                try:
                    jumlah = int(input(f"Berapa banyak bibit {bibit_dibeli}? "))
                    if jumlah <= 0:
                        tampilkan_pesan("Jumlah harus positif.", "error")
                    else:
                        total = HARGA_BIBIT[bibit_dibeli] * jumlah
                        if data_pemain["uang"] >= total:
                            data_pemain["uang"] -= total
                            data_pemain["bibit"][bibit_dibeli] += jumlah
                            tampilkan_pesan(f"Berhasil membeli {jumlah} bibit {bibit_dibeli}!", "success")
                        else:
                            tampilkan_pesan("Uang tidak cukup.", "error")
                except ValueError:
                    tampilkan_pesan("Masukkan angka yang valid!", "error")
            else:
                tampilkan_pesan("Bibit tidak tersedia.", "error")
            tekan_enter()
            break
            
        elif pilihan == '2':
            bersihkan_layar()
            tampilkan_header("💧 UPGRADE AIR 💧")
            if data_pemain.get("kapasitas_air", KAPASITAS_AIR_AWAL) >= KAPASITAS_AIR_MAKSIMAL:
                tampilkan_pesan("Kapasitas air sudah maksimal!", "info")
            else:
                tampilkan_pesan(f"Kapasitas saat ini: {data_pemain['kapasitas_air']} 💧", "info")
                tampilkan_pesan(f"Upgrade ke: {KAPASITAS_AIR_MAKSIMAL} 💧", "info")
                tampilkan_pesan(f"Biaya: ${BIAYA_UPGRADE_AIR} 💰", "info")
                
                konfirmasi = input("Apakah ingin upgrade? (y/n): ").lower()
                if konfirmasi == 'y':
                    if data_pemain['uang'] >= BIAYA_UPGRADE_AIR:
                        data_pemain['uang'] -= BIAYA_UPGRADE_AIR
                        data_pemain['kapasitas_air'] = KAPASITAS_AIR_MAKSIMAL
                        data_pemain['sisa_air'] = KAPASITAS_AIR_MAKSIMAL
                        tampilkan_pesan("Kapasitas air berhasil di-upgrade!", "success")
                    else:
                        tampilkan_pesan("Uang tidak cukup untuk upgrade.", "error")
            tekan_enter()
            break
            
        elif pilihan == '3':
            break

def pengaturan(data_pemain, musik_tersedia):
    """Menu pengaturan game"""
    bersihkan_layar()
    tampilkan_header("⚙️ PENGATURAN ⚙️")
    status_musik = "ON 🎵" if data_pemain.get("musik_nyala", False) else "OFF 🔇"
    print(f"1. Musik: {status_musik}\n2. Kembali")
    
    pilihan = input("\nPilih opsi: ")
    if pilihan == '1':
        toggle_musik(data_pemain, musik_tersedia)

def tampilkan_loading(teks="Memuat...", durasi=2):
    """Menampilkan loading bar dengan info-info tentang game di bawah bar, info tampil acak (5 info berbeda) selama bar berjalan"""
    bersihkan_layar()
    # Tampilkan ASCII art HARVEST MOON
    ascii_art = pyfiglet.figlet_format(TEXT_HEADER)
    print(ascii_art)
    cprint("=" * PANJANG_HEADER, 'yellow')
    cprint("Selamat Datang di".center(PANJANG_HEADER), 'yellow', attrs=['bold'])
    cprint("HARVEST MOON".center(PANJANG_HEADER), 'cyan', attrs=['bold', 'underline'])
    cprint("=" * PANJANG_HEADER, 'yellow')
    print()
    cprint(teks.center(PANJANG_HEADER), 'magenta')
    print()
    bar_length = 30

    # Daftar info game
    info_list = [
        "Tips: Siram tanamanmu setiap hari agar tidak layu!",
        "Kamu bisa memperluas lahan untuk menanam lebih banyak.",
        "Jual hasil panen di pasar untuk mendapatkan uang.",
        "Upgrade kapasitas air agar bisa menyiram lebih banyak tanaman.",
        "Pak Budi selalu siap membantumu di desa ini.",
        "Tanaman yang tidak disiram akan layu saat kamu tidur.",
        "Kamu bisa meminjam uang di bank jika kehabisan modal.",
        "Panen tanaman saat sudah matang untuk membuka bibit baru.",
        "Jangan lupa simpan permainanmu secara berkala!",
        "Setiap tanaman punya waktu tumbuh yang berbeda.",
    ]
    # Ambil 5 info acak tanpa duplikat
    info_pilihan = random.sample(info_list, 5)
    delay = 0.5  # Per step, total waktu ~15 detik

    # Bagi bar menjadi 5 bagian, setiap bagian tampilkan info berbeda
    steps_per_info = (bar_length + 1) // 5
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = '█' * i + '-' * (bar_length - i)
        bar_str = f"[{bar}] {percent}%"
        # Pilih info berdasarkan bagian bar
        info_idx = min(i // steps_per_info, 4)
        info = info_pilihan[info_idx]
        # Bar loading di tengah
        print(' ' * ((PANJANG_HEADER - len(bar_str)) // 2) + bar_str)
        # Info di bawah bar, tetap di tengah
        print(' ' * ((PANJANG_HEADER - len(info)) // 2) + colored(info, 'cyan'))
        # Kembali ke atas bar untuk update (2 baris ke atas)
        if i != bar_length:
            print(f"\033[F\033[F", end='')  # ANSI escape: move cursor up 2 lines
        sys.stdout.flush()
        time.sleep(delay)
    time.sleep(1)

def tampilkan_tutorial(menu_items, baris_menu, kolom_lebar, PANJANG_HEADER, data_pemain):
    """Menampilkan tutorial di bawah menu aksi, satu dialog per tampilan"""
    dialog = [
        ("Pak Budi", "😊", "Halo! Namaku Pak Budi, aku akan membantumu bertani di desa ini."),
        ("Pak Budi", "😮", "Di sini kamu bisa menanam bibit, menyiram tanaman, dan memanen hasilnya."),
        ("Pak Budi", "😅", "Jangan lupa untuk selalu menyiram tanamanmu setiap hari agar tidak layu!"),
        ("Pak Budi", "👍", "Kamu juga bisa memperluas lahan, membeli bibit baru, dan mengelola barangmu di inventaris."),
        ("Pak Budi", "💡", "Jika butuh uang, kamu bisa menjual hasil panenmu di pasar atau meminjam uang di bank."),
        ("Pak Budi", "😃", "Selamat bertani dan semoga sukses!"),
    ]
    for nama, ekspresi, kalimat in dialog:
        bersihkan_layar()
        status = f"🗓 HARI KE-{data_pemain['hari']} | 💰 UANG: ${data_pemain['uang']} | 🏦 HUTANG: ${data_pemain['hutang']} "
        cprint(status.center(PANJANG_HEADER), 'white', 'on_blue')
        tampilkan_lahan(data_pemain)
        tampilkan_header("PILIH AKSI")
        for i in range(baris_menu):
            kolom_kiri = menu_items[i]
            kolom_kanan = menu_items[i + baris_menu] if i + baris_menu < len(menu_items) else ""
            menu_line = f"{kolom_kiri.ljust(kolom_lebar)}{kolom_kanan.ljust(kolom_lebar)}"
            print(menu_line[:PANJANG_HEADER])
        print()
        cprint(f"{nama} {ekspresi}:", 'yellow', end=" ")
        print(kalimat)
        cprint("[Tekan Enter untuk lanjut]", 'white', 'on_grey')
        input()

def main():
    """Fungsi utama game"""
    # Inisialisasi
    bersihkan_layar()
    pygame.mixer.init()
    
    # Coba mainkan musik intro
    try:
        if exists(INTRO_MUSIC_FILE):
            pygame.mixer.music.load(INTRO_MUSIC_FILE)
            pygame.mixer.music.play(-1)
    except:
        pass
    
    data_pemain = None
    tutorial_sudah = False  # <-- Inisialisasi di sini

    # Menu awal
    intro_berjalan = mainkan_musik_intro()
    while data_pemain is None:
        bersihkan_layar()
        ascii_art = pyfiglet.figlet_format(TEXT_HEADER)
        print(ascii_art)
        cprint("=" * PANJANG_HEADER, 'yellow')
        cprint("Selamat Datang di".center(PANJANG_HEADER), 'yellow', attrs=['bold'])
        cprint("HARVEST MOON".center(PANJANG_HEADER), 'cyan', attrs=['bold', 'underline'])
        cprint("=" * PANJANG_HEADER, 'yellow')
        cprint("Petualangan bertani dan berbisnis dimulai di sini.".center(PANJANG_HEADER), 'cyan')
        cprint("Pilih menu di bawah untuk memulai:".center(PANJANG_HEADER), 'magenta')
        print()
        cprint("  1. 🎮  Mulai Permainan Baru", 'white', 'on_green')
        cprint("  2. 💾  Lanjutkan Permainan", 'white', 'on_blue')
        print()
        cprint("Gunakan angka 1/2 lalu tekan Enter untuk memilih.".center(PANJANG_HEADER), 'grey')
        
        pilihan = input("> ")
        if pilihan == '1':
            if exists(SAVE_FILE):
                cprint("Memulai game baru akan menghapus data lama.", 'yellow')
                konfirmasi = input("Lanjutkan? (y/n) ").lower()
                if konfirmasi == 'y':
                    tampilkan_loading("Membuat game baru...")  # Loading tampil dulu, musik tetap jalan
                    if intro_berjalan:
                        pygame.mixer.music.stop()
                    data_pemain = game_baru()
                    # tutorial_sudah tetap False untuk game baru
            else:
                tampilkan_loading("Membuat game baru...")
                if intro_berjalan:
                    pygame.mixer.music.stop()
                data_pemain = game_baru()
        elif pilihan == '2':
            tampilkan_loading("Memuat game...")
            data_pemain = muat_game()
            if data_pemain:
                if intro_berjalan:
                    pygame.mixer.music.stop()
                tampilkan_pesan("Game berhasil dimuat!", "success")
                time.sleep(1.5)
                tutorial_sudah = True  # <-- Set True agar tutorial tidak tampil saat load game
            else:
                # Jika tidak ada data tersimpan, tetap mainkan musik intro
                tampilkan_pesan("Tidak ada data game tersimpan.", "error")
                if not intro_berjalan:
                    intro_berjalan = mainkan_musik_intro()
                time.sleep(1.5)
                bersihkan_layar()
        else:
            tampilkan_pesan("Pilihan tidak valid.", "error")
            time.sleep(1.2)
            bersihkan_layar()
    
    # Inisialisasi musik utama
    musik_tersedia = inisialisasi_musik()
    if musik_tersedia and data_pemain.get("musik_nyala", True):
        try:
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.play(loops=-1)
        except:
            tampilkan_pesan("Gagal memulai musik latar.", "error")
    
    # Game loop utama
    sedang_berjalan = True
    notifikasi_layu = []
    while sedang_berjalan:
        bersihkan_layar()
        status = f"🗓 HARI KE-{data_pemain['hari']} | 💰 UANG: ${data_pemain['uang']} | 🏦 HUTANG: ${data_pemain['hutang']} "
        cprint(status.center(PANJANG_HEADER), 'white', 'on_blue')
        tampilkan_lahan(data_pemain)
        
        # Menu utama
        tampilkan_header("PILIH AKSI")
        menu_items = [
            "1. 🌱 Tanam Bibit", "2. 🛒 Pasar", "3. 💧 Siram Tanaman", "4. 🧺 Panen",
            "5. 💸 Jual Hasil", "6. 🎒 Inventaris", "7. 🏞️  Perluas Lahan",
            "8. 😴 Tidur", "9. 🏦 Bank", "10. ⚙️ Pengaturan",
            f"11. 💾 Simpan & Keluar{' ' * (PANJANG_HEADER - 27)}"
        ]
        baris_menu = 6
        kolom_lebar = PANJANG_HEADER // 2
        for i in range(baris_menu):
            kolom_kiri = menu_items[i]
            kolom_kanan = menu_items[i + baris_menu] if i + baris_menu < len(menu_items) else ""
            menu_line = f"{kolom_kiri.ljust(kolom_lebar)}{kolom_kanan.ljust(kolom_lebar)}"
            print(menu_line[:PANJANG_HEADER])

        # Tampilkan tutorial di bagian bawah menu aksi (bukan halaman sendiri)
        if not tutorial_sudah:
            tampilkan_tutorial(menu_items, baris_menu, kolom_lebar, PANJANG_HEADER, data_pemain)
            tutorial_sudah = True

        # Tampilkan notifikasi tanaman layu di bawah menu aksi
        if notifikasi_layu:
            for notif in notifikasi_layu:
                cprint(notif, 'yellow')
            tekan_enter()
            notifikasi_layu.clear()

        aksi = input("> ")
        
        if aksi == '1':
            tanam_bibit(data_pemain)
            tekan_enter()
        elif aksi == '2':
            pasar(data_pemain)
        elif aksi == '3':
            siram_tanaman(data_pemain)
        elif aksi == '4':
            panen(data_pemain)
            tekan_enter()
        elif aksi == '5':
            jual_hasil(data_pemain)
            tekan_enter()
        elif aksi == '6':
            tampilkan_inventaris(data_pemain)
            tekan_enter()
        elif aksi == '7':
            perluas_lahan(data_pemain)
            tekan_enter()
        elif aksi == '8':
            notifikasi_layu = tidur(data_pemain)
            simpan_game(data_pemain)
        elif aksi == '9':
            bank(data_pemain)
            tekan_enter()
        elif aksi == '10':
            pengaturan(data_pemain, musik_tersedia)
            tekan_enter()
        elif aksi == '11':
            simpan_game(data_pemain)
            tampilkan_pesan("Game berhasil disimpan. Sampai jumpa! 👋", "success")
            sedang_berjalan = False
            time.sleep(2)
        else:
            tampilkan_pesan("Aksi tidak valid!", "error")
            time.sleep(1)
    
    # Berhentikan musik saat keluar
    if musik_tersedia:
        pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
