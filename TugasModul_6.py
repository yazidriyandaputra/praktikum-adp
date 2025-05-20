while True:
    n = int(input("\nMasukkan banyak koordinat : "))
    if n > 0:
        break
    else:
        print("Banyak koordinat harus > 0!")
koor = []
for i in range(n):
    print(f"\nKoordinat ke-{i+1}")
    x = int(input("Masukkan x : "))
    y = int(input("Masukkan y : "))
    koor.append([x,y])
print()
p = len(koor)
print(f" {'_'*42}")
print(f"|{'Titik Pertama':^15}|{'Titik Kedua':^15}|{'Jarak':^10}|")
print(f"|{'_'*15}|{'_'*15}|{'_'*10}|")
for i in range(p):
    for j in range(i+1, p):
        jarak = (((koor[i][0] - koor[j][0]) ** 2) +
                 ((koor[i][1] - koor[j][1]) ** 2)) ** 0.5
        titik_1 = f"({koor[i][0]},{koor[i][1]})"
        titik_2 = f"({koor[j][0]},{koor[j][1]})"
        print(f"|{titik_1:^15}|{titik_2:^15}|{jarak:^10.2f}|")
print(f"|{'_'*15}|{'_'*15}|{'_'*10}|")