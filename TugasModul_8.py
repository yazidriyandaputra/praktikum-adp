def set_file():
    file = open(data_keuangan,'a')
    file.close()

def memuat_data():
    data = []
    file = open(data_keuangan,'r')
    baris = file.readlines()
    file.close()
    for line in baris:
        tanggal, keterangan, jumlah, tipe = line.strip().split('|')
        data.append({
            'tanggal': tanggal,
            'keterangan': keterangan,
            'jumlah': int(jumlah),
            'tipe': tipe
        })
    return data

def simpan_data(data):
    file = open(data_keuangan,'w')
    for item in data:
        line = f"{item['tanggal']}|{item['keterangan']}|{item['jumlah']}|{item['tipe']}\n"
        file.write(line)
    file.close()

def tampilkan_menu():
    print("\n" + "="*45)
    print(f"{"APLIKASI CATATAN KEUANGAN":^45}")
    print("="*45)
    print("1. ➕ Tambah Data Keuangan")
    print("2. 🗑️  Hapus Data Keuangan")
    print("3. 📋 Tampilkan Semua Data")
    print("4. 📤 Keluar")
    print("="*45)

def tambah_data(data):
    tanggal = input("Tanggal (YYYY-MM-DD): ")
    keterangan = input("Keterangan: ")
    jumlah = int(input("Jumlah Uang: "))
    tipe = input("Tipe (pemasukan/pengeluaran): ").lower()
    
    if tipe != 'pemasukan' and tipe != 'pengeluaran':
        print("❌ Error\nTipe tidak valid. Harus 'pemasukan' atau 'pengeluaran'")
        return

    data.append({
        "tanggal": tanggal,
        "keterangan": keterangan,
        "jumlah": jumlah,
        "tipe": tipe
    })

    simpan_data(data)
    print("✅ Data berhasil ditambahkan!")

def hapus_data(data):
    if len(data) == 0:
        print("📭 Tidak ada data untuk dihapus")
        return

    tampilkan_data(data)

    indeks = int(input("\nMasukkan nomor data yang ingin dihapus: "))
    indeks -= 1
    if indeks < 0 or indeks >= len(data):
        print("❌ Error\nNomor tidak valid")
        return

    del data[indeks]
    simpan_data(data)
    print("🗑️  Data berhasil dihapus!")

def tampilkan_data(data):
    if len(data) == 0:
        print("📭 Belum ada data yang dapat ditampilkan")
        return
    print("📋 Data Keuangan:")
    for i in range(len(data)):
        item = data[i]
        print(f"{i+1}. [{item['tanggal']}] {item['tipe'].upper()} - {item['keterangan']} : Rp{item['jumlah']:,}")

data_keuangan = "data_keuangan.txt"
set_file()
data = memuat_data()
while True:
    tampilkan_menu()
    pilihan = input("Pilih menu (1/2/3/4): ")
    print()
    if pilihan == '1':
        tambah_data(data)
    elif pilihan == '2':
        hapus_data(data)
    elif pilihan == '3':
        tampilkan_data(data)
    elif pilihan == '4':
        print("Terima kasih sudah menggunakan program ini!\nSampai jumpa👋")
        break
    else:
        print("❌ Error\nPilihan tidak valid")