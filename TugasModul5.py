print("\n==========PROGRAM MANAJEMEN NILAI MAHASISWA==========")

list_nomor = []
list_nama = []
list_nilai = []

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
            if nomor > 0 and nomor not in list_nomor:
                    list_nomor.append(nomor)
                    break
            else:
                print("Input tidak valid.\nNomor harus > 0 dan harus berbeda dengan input sebelumnya!")
        while True:
            nama = input("Masukkan nama mahasiswa\t\t: ").upper()
            if nama not in list_nama:
                list_nama.append(nama)
                break
            else:
                print("Nama yang anda masukkan sudah ada.\nMasukkan nama lain")
        while True:
            nilai = float(input("Masukkan nilai mahasiswa\t: "))
            if 0 <= nilai <= 100:
                list_nilai.append(nilai)
                break
            else:
                print("Input tidak valid. Nilai harus berada dalam selang 0-100")
        print('\n"Data berhasil ditambahkan!"')

    elif menu == 2:
        if list_nomor == [] and list_nama == [] and list_nilai == []:
            print("\nData masih kosong! Masukkan data terlebih dahulu!")
            continue
        while True:
            nomor = int(input("\nMasukkan nomor yang ingin dihapus : "))
            if nomor > 0 and nomor in list_nomor:
                indeks = list_nomor.index(nomor)
                list_nomor.pop(indeks) 
                list_nama.pop(indeks)
                list_nilai.pop(indeks)
                print('\n"Data berhasil dihapus!"')
                break
            else:
                print("Input tidak valid.\nNomor harus > 0 dan ada di dalam data!")
    
    elif menu == 3:
        batas = len(list_nomor)
        if batas == 0:
            print("\nBelum ada data yang bisa ditampilkan!\nMasukkan data terlebih dahulu!")
        elif batas == 1:
            print('\n"Data berhasil dicetak!"')
            print(f" {'_'*39}")
            print(f"| {'NOMOR':^6} | {'NAMA':^20} | {'NILAI':^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
            print(f"| {list_nomor[0]:^6} | {list_nama[0]:^20} | {list_nilai[0]:^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
        else:
            print('\n"Data berhasil dicetak!"')
            while batas > 1:
                for i in range(batas-1):
                    if list_nilai[i] > list_nilai[i + 1]:
                        list_nomor[i], list_nomor[i + 1] = list_nomor[i + 1], list_nomor[i]
                        list_nama[i], list_nama[i + 1] = list_nama[i + 1], list_nama[i]
                        list_nilai[i], list_nilai[i + 1] = list_nilai[i + 1], list_nilai[i]
                batas -= 1
            batas = len(list_nomor)   
            print(f" {'_'*39}") 
            print(f"| {'NOMOR':^6} | {'NAMA':^20} | {'NILAI':^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
            for i in range(batas-1, -1, -1):
                print(f"| {list_nomor[i]:^6} | {list_nama[i]:^20} | {list_nilai[i]:^5} |")
            print(f"|{'_'*8}|{'_'*22}|{'_'*7}|")
    
    elif menu == 4:
        print("\nTerima kasih telah menggunakan program ini ^_^\n")
        break