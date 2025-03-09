# Tampilan 1

print("--------  DAFTAR MENU  ---------")
print("")
print("==========  Paket A1  ==========")
print("Nasi Goreng Ayam + Es Teh")
print("Harga : Rp.40.000")
print("==========  Paket A2  ==========")
print("Nasi Goreng Seafood + Es Teh")
print("Harga : Rp.35.000")
print("==========  Paket A3  ==========")
print("Nasi Goreng Spesial + Es Teh")
print("Harga : Rp.50.000")
print("==========  Paket  B  ==========")
print("Ayam Geprek + Nasi + Jus Mangga")
print("Harga : Rp.45.000")
print("==========  Paket  C  ==========")
print("Ayam Bakar + Nasi + Jus Jeruk")
print("Harga : Rp.42.000")
print("==========  Paket D1  ==========")
print("Mie Aceh Rebus + Jus Alpukat")
print("Harga : Rp.32.000")
print("==========  Paket D2  ==========")
print("Mie Aceh Goreng + Jus Alpukat")
print("Harga : Rp.30.000")
print("")

#Tampilan 2

print("-------------  HALAMAN PEMESANAN  -------------")
print("")
nama = input("Masukkan nama anda : ").upper()
telepon = (input("Masukkan nomor telepon anda : "))
alamat = input("Masukkan alamat pengiriman : ").upper()
print("")
paket = input("Pilih paket : ").upper()
if paket == "A1":
    isi = "Nasi Goreng Ayam + Es Teh"
    harga = 40000
elif paket == "A2":
    isi = "Nasi Goreng Seafood + Es Teh"
    harga = 35000
elif paket == "A3":
    isi = "Nasi Goreng Spesial + Es Teh"
    harga = 50000
elif paket == "B":
    isi = "Ayam Geprek + Nasi + Jus Mangga"
    harga = 45000
elif paket == "C":
    isi = "Ayam Bakar + Nasi + Jus Jeruk"
    harga = 42000
elif paket == "D1":
    isi = "Mie Aceh Rebus + Jus Alpukat"
    harga = 32000
elif paket == "D2":
    isi = "Mie Aceh Goreng + Jus Alpukat"
    harga = 30000
jumlah = int(input("Jumlah paket yang dipesan : "))
total_harga = harga * jumlah
pajak = total_harga * 0.1
if total_harga < 150000:
    ongkir = 25000
else:
    ongkir = 0
total_akhir = total_harga + pajak + ongkir

#Tampilan 3

print("")
print("--------------  STRUK PEMESANAN  --------------")
print("")
print(f"Nama              : {nama}")
print(f"Nomor Telepon     : {telepon}")
print(f"Alamat Pengiriman : {alamat}")
print("-----------------------------------------------")
print(f"Detail Pesanan    : Paket {paket}")
print(f"                    {isi}")
print(f"Jumlah            : {jumlah}")
print("-----------------------------------------------")
print(f"Total Harga       : Rp{total_harga:,}")
print(f"Pajak (10%)       : Rp{pajak:,}")
print(f"Biaya Pengiriman  : Rp{ongkir:,}")
print("-----------------------------------------------")
print(f"Total Akhir       : Rp.{total_akhir:,}")
print("")
print("TERIMA KASIH TELAH MEMESAN!")