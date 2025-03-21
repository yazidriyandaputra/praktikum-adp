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
P_n = (1 / (e ** lambda_t))

for n in range (M + 1) :
    print(f"{n + 1}. P(N(t) = {n}) = {P_n:.5f}\n")
    P_n *= lambda_t / (n + 1) 

print("=================== SELESAI! =================\n")
