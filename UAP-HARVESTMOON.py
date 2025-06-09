from os import system, name
from os.path import exists
import time
import random
from termcolor import colored, cprint
import pygame
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import shutil

Save_File = "harvest_moon.txt"
Musik_Utama = "Harvest Moon_ Back to Nature  Spring  OST.mp3"
Musik_Intro = "Harvest Moon_ Back to Nature  Opening  OST.mp3"

Uang_Awal = 10
Bibit_Apel_Awal = 3
Ukuran_Lahan_Baris_Awal = 2
Ukuran_Lahan_Kolom_Awal = 2
Kapasitas_Air_Upgrade = [4, 9, 16, 25]
Kapasitas_Air_Awal = Kapasitas_Air_Upgrade[0]
Kapasitas_Air_Maksimal = Kapasitas_Air_Upgrade[-1]
Biaya_Upgrade_Air = [15, 30, 50] 
Pinjaman_Maksimal = 30

Harga_Bibit = {"apel": 5, "tomat": 12, "lettuce": 20}
Harga_Jual = {"apel": 2, "tomat": 4, "lettuce": 10}
Hari_Tumbuh = {"apel": 2, "tomat": 3, "lettuce": 4}
Emoji_Tanaman = {"apel": "🍎", "tomat": "🍅", "lettuce": "🥬"}

Judul = "HARVEST MOON"
Panjang_Header = 72

def bersihkan_layar():
    """Membersihkan layar terminal"""
    system('cls' if name == 'nt' else 'clear')

def tampilkan_header(teks):
    """Menampilkan header dengan panjang konsisten"""
    cprint(f"\n{'=' * Panjang_Header}", 'yellow')
    cprint(f"{teks.center(Panjang_Header)}", 'yellow', attrs=["bold"])
    cprint(f"{'=' * Panjang_Header}", 'yellow')

def tampilkan_judul_besar(judul, warna='yellow'):
    """Menampilkan judul besar ASCII-art dengan warna tertentu"""
    judul_art = pyfiglet.figlet_format(judul)
    for baris in judul_art.splitlines():
        cprint(baris, warna, attrs=['bold'])

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
    pygame.mixer.init()
    pygame.mixer.music.load(Musik_Intro)
    pygame.mixer.music.play(-1)
    return True

def inisialisasi_musik():
    """Menginisialisasi musik latar"""
    pygame.mixer.init()
    pygame.mixer.music.load(Musik_Utama)
    return True

def key_musik(data_pemain):
    """Menyalakan/mematikan musik"""
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
    lahan_awal = []
    for _ in range(Ukuran_Lahan_Baris_Awal):
        baris_lahan = [None] * Ukuran_Lahan_Kolom_Awal
        lahan_awal.append(baris_lahan)

    return {
        "uang": Uang_Awal,
        "bibit": {"apel": Bibit_Apel_Awal, "tomat": 0, "lettuce": 0},
        "inventaris": {},
        "baris_lahan": Ukuran_Lahan_Baris_Awal,
        "kolom_lahan": Ukuran_Lahan_Kolom_Awal,
        "lahan": lahan_awal,
        "hari": 1,
        "hutang": 0,
        "kapasitas_air": Kapasitas_Air_Awal,
        "sisa_air": Kapasitas_Air_Awal,
        "tomat_terbuka": False,
        "lettuce_terbuka": False,
        "musik_nyala": True,
    }

def simpan_game(data_pemain):
    """Menyimpan progress game"""
    with open(Save_File, 'w') as f:
        for key, value in data_pemain.items():
            f.write(f"{key}:{repr(value)}\n")

def muat_game():
    """Memuat progress game"""
    if not exists(Save_File):
        return None
    data_pemain = {}
    with open(Save_File, 'r') as f:
        for line in f:
            if ':' in line:
                key, value_str = line.strip().split(':', 1)
                data_pemain[key] = eval(value_str)
    return data_pemain

def tampilkan_lahan(data_pemain):
    """Menampilkan kondisi lahan"""
    tampilkan_header("🏡 LADANGMU 🏡")
    cprint(f"Sisa Air Hari Ini: {data_pemain['sisa_air']}/{data_pemain['kapasitas_air']} 💧", 'blue')
    
    for i in range(data_pemain["baris_lahan"]):
        baris_tampilan = []
        for j in range(data_pemain["kolom_lahan"]):
            tanaman = data_pemain["lahan"][i][j]
            if tanaman is None:
                tampilan_str = colored("[🟫]", 'white', None)
            else:
                hari_tersisa = tanaman["hari_tumbuh"]
                emoji_tanaman = Emoji_Tanaman.get(tanaman["nama"], "❓")
                status_air = "" if tanaman.get("disiram") else colored("🚱", 'red')
                if hari_tersisa <= 0:
                    tampilan_str = colored(f"[{emoji_tanaman}P]", 'green', attrs=['bold'])
                elif hari_tersisa == Hari_Tumbuh.get(tanaman["nama"]):
                    tampilan_str = colored(f"[.🌱{status_air}]", 'yellow')
                else:
                    tampilan_str = colored(f"[🌿{status_air}]", 'cyan')
            baris_tampilan.append(tampilan_str)
        print(" ".join(baris_tampilan) + f"  B{i+1}")
    
    print("\n" + " ".join([f" K{k+1} " for k in range(data_pemain['kolom_lahan'])]))
    cprint("\nKeterangan: 🟫Kosong, 🌱Bibit, 🌿Tunas, P-Panen, 🚱Belum Disiram", 'grey')

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
            print(f" - {Emoji_Tanaman.get(bibit, '')} {bibit.capitalize()}: {jumlah}")
    
    baris_input = input(f"\nPilih baris (1-{data_pemain['baris_lahan']}) atau 0 untuk batal: ")
    if not baris_input.isdigit():
        tampilkan_pesan("Masukkan angka yang valid!", "error")
        return False
    baris = int(baris_input) - 1
    if baris == -1:
        return False

    kolom_input = input(f"Pilih kolom (1-{data_pemain['kolom_lahan']}): ")
    if not kolom_input.isdigit():
        tampilkan_pesan("Masukkan angka yang valid!", "error")
        return False
    kolom = int(kolom_input) - 1

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
        "hari_tumbuh": Hari_Tumbuh[bibit_ditanam],
        "disiram": False
    }
    data_pemain["bibit"][bibit_ditanam] -= 1
    tampilkan_pesan(f"Berhasil menanam {bibit_ditanam} di ({baris+1}, {kolom+1})!", "success")
    return True

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
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            time.sleep(1)
            continue
        if baris == -1:
            break
        try:
            kolom = int(input(f"Kolom (1-{data_pemain['kolom_lahan']}): ")) - 1
        except ValueError:
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            time.sleep(1)
            continue
        
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
                tampilkan_pesan(f"Kamu memanen {jumlah} {Emoji_Tanaman.get(nama_tanaman, '')} {nama_tanaman}!", "success")
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
            print(f" - {Emoji_Tanaman.get(bibit, '')} {bibit.capitalize()}: {jumlah} buah")
    
    cprint("\n--- Keranjang Panen ---", attrs=['bold'])
    if not data_pemain["inventaris"]:
        print("Kosong.")
    else:
        for item, jumlah in data_pemain["inventaris"].items():
            print(f" - {Emoji_Tanaman.get(item, '')} {item.capitalize()}: {jumlah} buah")

def jual_hasil(data_pemain):
    """Menjual hasil panen"""
    tampilkan_header("💸 JUAL HASIL PANEN 💸")
    if not data_pemain["inventaris"]:
        tampilkan_pesan("Keranjang panenmu kosong!", "error")
        return
    
    tampilkan_pesan("Isi keranjang panenmu:", "info")
    for item, jumlah in data_pemain["inventaris"].items():
        print(f"- {Emoji_Tanaman.get(item, '')} {item.capitalize()}: {jumlah} (Harga: ${Harga_Jual[item]}/buah)")
    
    item_dijual = input("\nApa yang ingin kamu jual? (atau 'batal'): ").lower()
    if item_dijual == 'batal':
        return
        
    if item_dijual in data_pemain["inventaris"] and data_pemain["inventaris"][item_dijual] > 0:
        jumlah_input = input(f"Berapa banyak {item_dijual}? ")
        if not jumlah_input.isdigit():
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            return
        jumlah = int(jumlah_input)
        if 0 < jumlah <= data_pemain["inventaris"][item_dijual]:
            pendapatan = Harga_Jual[item_dijual] * jumlah
            data_pemain["uang"] += pendapatan
            data_pemain["inventaris"][item_dijual] -= jumlah
            if data_pemain["inventaris"][item_dijual] == 0:
                del data_pemain["inventaris"][item_dijual]
            tampilkan_pesan(f"Berhasil menjual {jumlah} {item_dijual} dan dapat ${pendapatan}!", "success")
        else:
            tampilkan_pesan("Jumlah tidak valid.", "error")
    else:
        tampilkan_pesan("Item tidak ada di inventaris.", "error")

def perluas_lahan(data_pemain):
    """Memperluas lahan pertanian"""
    tampilkan_header("🏞️ PERLUAS LAHAN 🏞️")
    if data_pemain["baris_lahan"] >= Kapasitas_Air_Upgrade[-1]:
        tampilkan_pesan("Lahanmu sudah maksimal!", "info")
        return
        
    biaya = (data_pemain["baris_lahan"] * data_pemain["kolom_lahan"]) * 10
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
            
        jumlah_input = input(f"Jumlah pinjaman (maks ${Pinjaman_Maksimal}): ")
        if not jumlah_input.isdigit():
            tampilkan_pesan("Masukkan angka yang valid!", "error")
            return
        jumlah = int(jumlah_input)
        if 0 < jumlah <= Pinjaman_Maksimal:
            data_pemain["uang"] += jumlah
            data_pemain["hutang"] += jumlah
            tampilkan_pesan(f"Berhasil meminjam ${jumlah}.", "success")
        else:
            tampilkan_pesan(f"Jumlah pinjaman tidak valid.", "error")
            
    elif pilihan == '2':
        if data_pemain["hutang"] == 0:
            tampilkan_pesan("Kamu tidak punya hutang.", "info")
            return
            
        jumlah = int(input(f"Jumlah pembayaran (maks ${data_pemain['hutang']}): "))
        if 0 < jumlah <= data_pemain["uang"]:
            bayar = min(jumlah, data_pemain["hutang"])
            data_pemain["uang"] -= bayar
            data_pemain["hutang"] -= bayar
            tampilkan_pesan(f"Berhasil membayar hutang ${bayar}.", "success")
        else:
            tampilkan_pesan("Uang tidak cukup atau jumlah tidak valid.", "error")

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
            for bibit, harga in Harga_Bibit.items():
                if (bibit == "tomat" and not data_pemain.get("tomat_terbuka")) or \
                   (bibit == "lettuce" and not data_pemain.get("lettuce_terbuka")):
                    continue
                print(f"- {Emoji_Tanaman.get(bibit, '')} {bibit.capitalize()}: ${harga}")
            
            bibit_dibeli = input("\nApa yang ingin kamu beli? (atau 'batal'): ").lower()
            if bibit_dibeli == 'batal':
                continue
                
            if bibit_dibeli in Harga_Bibit:
                # Cek apakah bibit sudah terbuka
                if (bibit_dibeli == "tomat" and not data_pemain.get("tomat_terbuka")) or \
                   (bibit_dibeli == "lettuce" and not data_pemain.get("lettuce_terbuka")):
                    tampilkan_pesan("Bibit tidak tersedia atau belum terbuka.", "error")
                    tekan_enter()
                    break
                jumlah_input = input(f"Berapa banyak bibit {bibit_dibeli}? ")
                if not jumlah_input.isdigit():
                    tampilkan_pesan("Masukkan angka yang valid!", "error")
                    continue
                jumlah = int(jumlah_input)
                if jumlah <= 0:
                    tampilkan_pesan("Jumlah harus positif.", "error")
                else:
                    total = Harga_Bibit[bibit_dibeli] * jumlah
                    if data_pemain["uang"] >= total:
                        data_pemain["uang"] -= total
                        data_pemain["bibit"][bibit_dibeli] += jumlah
                        tampilkan_pesan(f"Berhasil membeli {jumlah} bibit {bibit_dibeli}!", "success")
                    else:
                        tampilkan_pesan("Uang tidak cukup.", "error")
            else:
                tampilkan_pesan("Bibit tidak tersedia.", "error")
            tekan_enter()
            break
            
        elif pilihan == '2':
            bersihkan_layar()
            tampilkan_header("💧 UPGRADE AIR 💧")
            kapasitas_sekarang = data_pemain.get("kapasitas_air", Kapasitas_Air_Awal)
            if kapasitas_sekarang >= Kapasitas_Air_Maksimal:
                tampilkan_pesan("Kapasitas air sudah maksimal!", "info")
            else:
                # Cari tingkat upgrade berikutnya
                idx_sekarang = Kapasitas_Air_Upgrade.index(kapasitas_sekarang)
                kapasitas_baru = Kapasitas_Air_Upgrade[idx_sekarang + 1]
                biaya_upgrade = Biaya_Upgrade_Air[idx_sekarang]
                tampilkan_pesan(f"Kapasitas saat ini: {kapasitas_sekarang} 💧", "info")
                tampilkan_pesan(f"Upgrade ke: {kapasitas_baru} 💧", "info")
                tampilkan_pesan(f"Biaya: ${biaya_upgrade} 💰", "info")
                
                konfirmasi = input("Apakah ingin upgrade? (y/n): ").lower()
                if konfirmasi == 'y':
                    if data_pemain['uang'] >= biaya_upgrade:
                        data_pemain['uang'] -= biaya_upgrade
                        data_pemain['kapasitas_air'] = kapasitas_baru
                        data_pemain['sisa_air'] = kapasitas_baru
                        tampilkan_pesan("Kapasitas air berhasil di-upgrade!", "success")
                    else:
                        tampilkan_pesan("Uang tidak cukup untuk upgrade.", "error")
            tekan_enter()
            break
        elif pilihan == '3':
            break

def pengaturan(data_pemain):
    """Menu pengaturan game"""
    bersihkan_layar()
    tampilkan_header("⚙️ PENGATURAN ⚙️")
    status_musik = "ON 🎵" if data_pemain.get("musik_nyala", False) else "OFF 🔇"
    print(f"1. Musik: {status_musik}\n2. Kembali")
    
    pilihan = input("\nPilih opsi: ")
    if pilihan == '1':
        key_musik(data_pemain)

def tampilkan_loading(teks="Memuat...", durasi=2):
    """Menampilkan loading bar dengan info-info tentang game di bawah bar, info tampil acak (5 info berbeda) selama bar berjalan"""
    bersihkan_layar()

    # Tampilkan ASCII art HARVEST MOON
    judul_art = pyfiglet.figlet_format(Judul)
    for baris in judul_art.splitlines():
        cprint(baris, 'yellow', attrs=['bold'])
    cprint("=" * Panjang_Header, 'yellow')
    cprint("Selamat Datang di".center(Panjang_Header), 'yellow', attrs=['bold'])
    cprint("HARVEST MOON".center(Panjang_Header), 'yellow', attrs=['bold', 'underline'])
    cprint("=" * Panjang_Header, 'yellow')
    print()
    cprint(teks.center(Panjang_Header), 'magenta')
    print()

    panjang_bar = 40

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

    delay = 0.2  # Delay per langkah
    langkah_per_info = 8

    for i in range(panjang_bar + 1):
        percent = int((i / panjang_bar) * 100)
        bar = '█' * i + '-' * (panjang_bar - i)
        bar_str = f"[{bar}] {percent}%".center(Panjang_Header)

        # Pilih info berdasarkan bagian bar
        info_idx = min(i // langkah_per_info, 4)
        info = info_pilihan[info_idx]
        info_str = colored(info.center(Panjang_Header), 'cyan')

        # Tampilkan bar dan info
        print(bar_str)
        print(info_str)

        # Geser kursor ke atas 2 baris untuk menimpa
        if i != panjang_bar:
            print("\033[F\033[F", end='')

        time.sleep(delay)

    time.sleep(1)

def tampilkan_tutorial(menu_items, baris_menu, kolom_lebar, Panjang_Header, data_pemain):
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
        cprint(status.center(Panjang_Header), 'white', 'on_blue')
        tampilkan_lahan(data_pemain)
        tampilkan_header("PILIH AKSI")
        for i in range(baris_menu):
            kolom_kiri = menu_items[i]
            kolom_kanan = menu_items[i + baris_menu] if i + baris_menu < len(menu_items) else ""
            menu_line = f"{kolom_kiri.ljust(kolom_lebar)}{kolom_kanan.ljust(kolom_lebar)}"
            print(menu_line[:Panjang_Header])
        print()
        cprint(f"{nama} {ekspresi}:", 'yellow', end=" ")
        print(kalimat)
        cprint("[Tekan Enter untuk lanjut]", 'white', 'on_grey')
        input()

def menu_awal():
    """Menampilkan menu awal dan mengembalikan data_pemain baru atau hasil load"""
    console = Console()
    intro_berjalan = mainkan_musik_intro()
    data_pemain = None
    tutorial_sudah = False
    width = shutil.get_terminal_size((80, 20)).columns
    while data_pemain is None:
        bersihkan_layar()
        # Tampilkan judul besar dengan fungsi khusus
        judul_game = pyfiglet.figlet_format(Judul)
        judul_lines = judul_game.splitlines()
        judul_width = max(len(baris) for baris in judul_lines)
        tampilkan_judul_besar(Judul, warna='yellow')
        # Panel menu awal, lebar mengikuti judul, isi rata tengah
        panel_text = (
            "[bold yellow]Selamat Datang di[/bold yellow]\n"
            "[bold cyan]HARVEST MOON[/bold cyan]\n\n"
            "[cyan]Petualangan bertani dan berbisnis dimulai di sini.[/cyan]\n"
            "[magenta]Pilih menu di bawah untuk memulai:[/magenta]\n\n"
            "[white on green] 1. 🎮  Mulai Permainan Baru [/white on green]\n"
            "[white on blue]  2. 💾  Lanjutkan Permainan  [/white on blue]\n\n"
            "[grey]Masukkan angka 1/2 lalu tekan Enter untuk memilih.[/grey]"
        )
        panel_width = min(judul_width, width - 4)
        console.print(
            Panel(
                Align.center(panel_text),
                style="bold blue",
                width=panel_width,
                border_style="bright_yellow"
            )
        )
        pilihan = input("> ")
        if pilihan == '1':
            if exists(Save_File):
                console.print("[yellow]Memulai game baru akan menghapus data lama.[/yellow]")
                konfirmasi = input("Lanjutkan? (y/n) ").lower()
                if konfirmasi == 'y':
                    tampilkan_loading("Membuat game baru...")
                    if intro_berjalan:
                        pygame.mixer.music.stop()
                    tampilkan_pesan("Game berhasil dimuat!", "success")
                    time.sleep(1.5)   
                    data_pemain = game_baru()
            else:
                tampilkan_loading("Membuat game baru...")
                if intro_berjalan:
                    pygame.mixer.music.stop()
                tampilkan_pesan("Game berhasil dimuat!", "success")
                time.sleep(1.5)
                data_pemain = game_baru()
        elif pilihan == '2':
            tampilkan_loading("Memuat game...")
            data_pemain = muat_game()
            if data_pemain:
                if intro_berjalan:
                    pygame.mixer.music.stop()
                tampilkan_pesan("Game berhasil dimuat!", "success")
                time.sleep(1.5)
                tutorial_sudah = True
            else:
                tampilkan_pesan("Tidak ada data game tersimpan.", "error")
                if not intro_berjalan:
                    intro_berjalan = mainkan_musik_intro()
                time.sleep(1.5)
                bersihkan_layar()
        else:
            tampilkan_pesan("Pilihan tidak valid.", "error")
            time.sleep(1.2)
            bersihkan_layar()
    return data_pemain, tutorial_sudah

def tampilkan_menu_aksi(data_pemain, tutorial_sudah, notifikasi_layu):
    """Menampilkan menu aksi utama dan mengembalikan aksi yang dipilih"""
    bersihkan_layar()
    status = f"🗓 HARI KE-{data_pemain['hari']} | 💰 UANG: ${data_pemain['uang']} | 🏦 HUTANG: ${data_pemain['hutang']} "
    cprint(status.center(Panjang_Header), 'white', 'on_blue')
    tampilkan_lahan(data_pemain)
    tampilkan_header("PILIH AKSI")
    menu_items = [
        "1. 🌱 Tanam Bibit", "2. 🛒 Pasar", "3. 💧 Siram Tanaman", "4. 🧺 Panen",
        "5. 💸 Jual Hasil", "6. 🎒 Inventaris", "7. 🏞️  Perluas Lahan",
        "8. 😴 Tidur", "9. 🏦 Bank", "10.⚙️ Pengaturan",
        f"11. 💾 Simpan & Keluar{' ' * (Panjang_Header - 27)}"
    ]
    baris_menu = 6
    kolom_lebar = Panjang_Header // 2
    for i in range(baris_menu):
        kolom_kiri = menu_items[i]
        kolom_kanan = menu_items[i + baris_menu] if i + baris_menu < len(menu_items) else ""
        menu_line = f"{kolom_kiri.ljust(kolom_lebar)}{kolom_kanan.ljust(kolom_lebar)}"
        print(menu_line[:Panjang_Header])

    # Tampilkan tutorial di bagian bawah menu aksi (bukan halaman sendiri)
    if not tutorial_sudah:
        tampilkan_tutorial(menu_items, baris_menu, kolom_lebar, Panjang_Header, data_pemain)
        tutorial_sudah = True

    # Tampilkan notifikasi tanaman layu di bawah menu aksi
    if notifikasi_layu:
        for notif in notifikasi_layu:
            cprint(notif, 'yellow')
        tekan_enter()
        notifikasi_layu.clear()

    aksi = input("> ")
    return aksi, tutorial_sudah

def proses_aksi(aksi, data_pemain):
    """Memproses aksi yang dipilih user dan mengembalikan notifikasi_layu jika ada"""
    notifikasi_layu = []
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
        pengaturan(data_pemain)
        tekan_enter()
    elif aksi == '11':
        simpan_game(data_pemain)
        tampilkan_pesan("Game berhasil disimpan. Sampai jumpa! 👋", "success")
        time.sleep(2)
        return "keluar"
    else:
        tampilkan_pesan("Aksi tidak valid!", "error")
        time.sleep(1)
    return notifikasi_layu

def main():
    """Fungsi utama game"""
    bersihkan_layar()
    tampilkan_judul_besar(Judul, warna='yellow')
    data_pemain, tutorial_sudah = menu_awal()
    inisialisasi_musik()
    if data_pemain.get("musik_nyala", True):
        pygame.mixer.music.load(Musik_Utama)
        pygame.mixer.music.play(loops=-1)

    sedang_berjalan = True
    notifikasi_layu = []
    while sedang_berjalan:
        aksi, tutorial_sudah = tampilkan_menu_aksi(data_pemain, tutorial_sudah, notifikasi_layu)
        hasil = proses_aksi(aksi, data_pemain)
        if hasil == "keluar":
            break
        elif isinstance(hasil, list):
            notifikasi_layu = hasil
        else:
            notifikasi_layu = []

    pygame.mixer.music.stop()

if __name__ == "__main__":
    main()
