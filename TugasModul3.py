print("\n============= PEUBAH ACAK POISSON ===========\n")

while True :
    lambda_t = float(input("Masukkan nilai λt : "))
    if lambda_t > 0 :
        break
    else:
        print("Input anda tidak valid. Masukkan nilai λt > 0")

print("")

while True :
    M = int(input("Masukkan nilai M  : "))
    if M >= 0 :
        break
    else:
        print("Input anda tidak valid. Masukkan nilai M >= 0")

print('''\n=============================================
               HASIL PERHITUNGAN
=============================================\n''')

e = 2.71828
fakt = 1

for n in range (M + 1) :
    if n > 0 :
        fakt *= n
    P_n = (1 / (e ** lambda_t)) * ((lambda_t ** n) / fakt)
    print(f"{n + 1}. P(N(t) = {n}) = {P_n:.5f}\n")

print("=================== SELESAI! =================\n")
