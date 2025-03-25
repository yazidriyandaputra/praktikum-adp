print("\nSelamat Datang di Sistem Reservasi tiket Konser")
print("Ukuran Kursi 17 x 6")

print("\nTampilan Layout Kursi : \n")
for i in range(17):
    for j in range((i * 7) + 1, ((i + 1) * 7) + 1):
        print(f"{j:3}", end=" ")
    print()
print('''\n* baris 1-2   : kategori VVIP
  baris 3-5   : kategori VIP
  baris 6-15  : kategori Reguler
  baris 16-17 : kategori Ekonomi
''')

print('''Harga tiket
 ________________________
| VVIP     | Rp2,000,000 |
|__________|_____________|
| VIP      | Rp1,500,000 |
|__________|_____________|
| Reguler  | Rp1,000,000 |
|__________|_____________|
| Ekonomi  | Rp500,000   |
|__________|_____________|''')

vvip = 14
vip = 21
reguler = 70
ekonomi = 14

kursi_dipesan = ""

print("\n============  HALAMAN PEMESANAN  ==============")
while True:
    tiket = int(input("\nMasukkan jumlah tiket yang ingin dipesan : "))
    if 1 <= tiket <= 119:
        break
    else:
        print("Input anda tidak valid!")
for k in range(1, tiket + 1):
    print(f"\nPemesanan ke-{k}")
    nama = input("Masukkan nama Anda : ").upper()
    no_telepon = int(input("Masukkan nomor telepon Anda : +62"))
    while True:
        no_kursi = int(input("Masukkan nomor kursi yang ingin dipesan : "))
        if f"({no_kursi})" in kursi_dipesan:
            print("kursi ini sudah dipesan! Pilih kursi lain.")
            continue
        if 1 <= no_kursi <= 14:
            kategori = "VVIP"
            harga = 2000000
            vvip -= 1
        elif 15 <= no_kursi <= 35:
            kategori = "VIP"
            harga = 1500000
            vip -= 1
        elif 36 <= no_kursi <= 105:
            kategori = "Reguler"
            harga = 1000000
            reguler -= 1
        elif 106 <= no_kursi <= 119:
            kategori = "Ekonomi"
            harga = 500000
            ekonomi -= 1 
        else:
            print("Input anda tidak valid!. Masukkan nomor kursi 1-119")
            continue
        kursi_dipesan += f"({no_kursi})"
        password = input("Masukkan password untuk akses ke konser : ")
        print("\n=============  STRUK PEMESANAN  ===============")
        print(f"Nama               :    {nama}")
        print(f"Nomor Telepon      :    +62{no_telepon}")
        print(f"Nomor Kursi        :    {no_kursi}")
        print(f"Kategori           :    {kategori}")
        print(f"Harga              :    Rp{harga:,}")
        print(f"Password           :    {password}")
        print("===============================================")
        break

print("\nSisa Kursi per Kategori")
print(f"VVIP          : {vvip}")
print(f"VIP           : {vip}")
print(f"Reguler       : {reguler}")
print(f"Ekonomi       : {ekonomi}")

print("\nLayout Kursi Setelah Pemesanan : \n")
for i in range(17):
    for j in range((i * 7) + 1, ((i + 1) * 7) + 1):
        if f"({j})" in kursi_dipesan:
            print("  O", end=" ")
        else:
            print(f"{j:3}", end=" ")
    print()
print('\n* kursi yang sudah dipesan ditandai dengan "O"')

print("\nTerima kasih telah melakukan reservasi!\n")