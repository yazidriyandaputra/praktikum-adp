def input_data():
    data = []
    n = int(input("Masukkan jumlah praktikan: "))
    for i in range(n):
        print(f"\nPraktikan ke-{i+1}")
        nama = input("Nama\t\t\t: ").upper()
        nim = int(input("NIM\t\t\t: "))
        pretest = float(input("Nilai pretest\t\t: "))
        postest = float(input("Nilai postest\t\t: "))
        tugas = float(input("Nilai tugas/makalah\t: "))
        bonus = float(input("Nilai bonus\t\t: "))
        data.append([nama, nim, pretest, postest, tugas, bonus, 0.0, 0])
    return data

def hitung_rata2(data, indeks):
    total = 0
    for baris in data:
        total += baris[indeks]
    return total / len(data)

def hitung_nilai_akhir(data):
    for baris in data:
        pretest = baris[2]
        postest = baris[3]
        tugas = baris[4]
        bonus = baris[5]
        nilai_akhir = (0.25 * pretest) + (0.25 * postest) + (0.5 * tugas) + bonus
        baris[6] = nilai_akhir

def peringkat(data):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i][6] < data[j][6]:
                data[i], data[j] = data[j], data[i]
    for i in range(len(data)):
        data[i][7] = i + 1

def tampilkan_tabel(data):
    print(f" {'_'*59}")
    print(f"|{'Nama':^15}|{'NIM':^15}|{'Nilai Akhir':^15}|{'Peringkat':^10}|")
    print(f"|{'_'*15}|{'_'*15}|{'_'*15}|{'_'*10}|")
    for baris in data:
        print(f"|{baris[0]:^15}|{baris[1]:^15}|{baris[6]:^15.2f}|{baris[7]:^10}|")
    print(f"|{'_'*15}|{'_'*15}|{'_'*15}|{'_'*10}|")
    
    rata2_pretest = hitung_rata2(data,2)
    rata2_postest = hitung_rata2(data,3)
    rata2_tugas = hitung_rata2(data,4)
    rata2_nilai_akhir = hitung_rata2(data,6)

    print("\nRata-Rata Nilai Shift V")
    print(f"\n{'Rata-rata Pretest':<25}: {rata2_pretest:.2f}")
    print(f"{'Rata-rata Postest':<25}: {rata2_postest:.2f}")
    print(f"{'Rata-rata Tugas/Makalah':<25}: {rata2_tugas:.2f}")
    print(f"\n{'Rata-rata Nilai Akhir':<25}: {rata2_nilai_akhir:.2f}")

praktikan = input_data()
hitung_nilai_akhir(praktikan)
peringkat(praktikan)
tampilkan_tabel(praktikan)