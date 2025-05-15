print("\n==========PROGRAM MANAJEMEN NILAI MAHASISWA==========")

NOMOR = []
NAMA = []
NILAI = []

while True:

    print('''\nMENU\n
1. Tambah Data
2. Hapus Data
3. Tampilkan Data
4. Keluar\n''')

    while True:
        menu = int(input("Pilih menu 1-4 : "))
        if 1 <= menu <= 4:
            break
        else:
            print("Input tidak valid. Pilih menu 1-4!")

    if menu == 1:
        while True:
            nomor = int(input("\nMasukkan nomor mahasiswa\t: "))
            if nomor > 0 and nomor not in NOMOR:
                    NOMOR.append(nomor)
                    break
            else:
                print("Input tidak valid.\nNomor harus > 0 dan harus berbeda dengan input sebelumnya!")
        while True:
            nama = input("Masukkan nama mahasiswa\t\t: ").upper()
            if nama not in NAMA:
                NAMA.append(nama)
                break
            else:
                print("Nama yang anda masukkan sudah ada.\nMasukkan nama lain")
        while True:
            nilai = float(input("Masukkan nilai mahasiswa\t: "))
            if 0 <= nilai <= 100:
                NILAI.append(nilai)
                break
            else:
                print("Input tidak valid. Nilai harus berada dalam selang 0-100")
        print('\n"Data berhasil ditambahkan!"')

    elif menu == 2:
        if NOMOR == [] and NAMA == [] and NILAI == []:
            print("\nData masih kosong! Masukkan data terlebih dahulu!")
            continue
        while True:
            nomor = int(input("\nMasukkan nomor yang ingin dihapus : "))
            if nomor > 0 and nomor in NOMOR:
                indeks = NOMOR.index(nomor)
                NOMOR.pop(indeks) 
                NAMA.pop(indeks)
                NILAI.pop(indeks)
                print('\n"Data berhasil dihapus!"')
                break
            else:
                print("Input tidak valid.\nNomor harus > 0 dan ada di dalam data!")
    
    elif menu == 3:
        batas = len(NOMOR)
        if batas == 0:
            print("\nBelum ada data yang bisa ditampilkan!\nMasukkan data terlebih dahulu!")
        elif batas == 1:
            print('\n"Data berhasil dicetak!"')
            print(f" {'_'*39}")
            print(f"| {'NOMOR':^6} | {'NAMA':^20} | {'NILAI':^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
            print(f"| {NOMOR[0]:^6} | {NAMA[0]:^20} | {NILAI[0]:^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
        else:
            print('\n"Data berhasil dicetak!"')
            while batas > 1:
                for i in range(batas-1):
                    if NILAI[i] > NILAI[i + 1]:
                        NOMOR[i], NOMOR[i + 1] = NOMOR[i + 1], NOMOR[i]
                        NAMA[i], NAMA[i + 1] = NAMA[i + 1], NAMA[i]
                        NILAI[i], NILAI[i + 1] = NILAI[i + 1], NILAI[i]
                batas -= 1
            batas = len(NOMOR)   
            print(f" {'_'*39}") 
            print(f"| {'NOMOR':^6} | {'NAMA':^20} | {'NILAI':^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
            for i in range(batas-1, -1, -1):
                print(f"| {NOMOR[i]:^6} | {NAMA[i]:^20} | {NILAI[i]:^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
    
    elif menu == 4:
        print("\nTerima kasih telah menggunakan program ini ^_^\n")
        break