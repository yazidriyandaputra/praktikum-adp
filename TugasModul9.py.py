from os import system
from time import sleep
from termcolor import cprint

pola_geser = [0, 1, 2, 2, 0, -1, -2, -2]

def bendera_naik(posisi):
    for i in range(15):
        if i < posisi:
            print('|')
        elif posisi <= i < posisi + 6:
            baris = i - posisi
            if baris < 3:
                cprint('|' + " " * 20, None, "on_red")
            else:
                cprint('|' + " " * 20, None, "on_white")
        else:
            print('|')

def bendera_berkibar(fase):
    for i in range(15):
        if i < 6:
            geser = pola_geser[(fase + i) % 8]
            if geser >= 0:
                line = " " * geser + " " * 20
            else:
                spasi_sisa = 20 + geser 
                line = " " * spasi_sisa
            if i < 3:
                cprint('|' + line, None, "on_red")
            else:
                cprint('|' + line, None, "on_white")
        else:
            print('|')

for langkah in range(10):
    posisi = 9 - langkah
    system('cls')
    bendera_naik(posisi)
    sleep(0.13)
fase = 0
while True:
    system('cls')
    bendera_berkibar(fase)
    fase += 1
    sleep(0.11)