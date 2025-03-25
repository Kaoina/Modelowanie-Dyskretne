import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def sciemnij_obraz(image_array, procent):
    wsp_sciemniajacy = (100 - procent) / 100.0
    przyciemniony_obraz = image_array * wsp_sciemniajacy

    przyciemniony_obraz[przyciemniony_obraz < 0] = 0  # wartości mniejsze od 0 na 0
    przyciemniony_obraz[przyciemniony_obraz > 255] = 255  # wartości większe od 255 na 255
    przyciemniony_obraz = przyciemniony_obraz.astype(np.uint8)

    return przyciemniony_obraz


def rozjasnij_obraz_krokowo(image_array, procent):
    wsp_rozjasniajacy = (100 + procent) / 100.0
    obraz_kopia = image_array * wsp_rozjasniajacy

    obraz_kopia[obraz_kopia < 0] = 0
    obraz_kopia[obraz_kopia > 255] = 255
    obraz_kopia = obraz_kopia.astype(np.uint8)

    return obraz_kopia


def binaryzacja_obraz(image_array, prog):
    prog_wartosc = 255 * (prog / 100.0)

    binarny_obraz = []

    for wiersz in image_array:
        nowy_wiersz = []
        for piksel in wiersz:
            if piksel > prog_wartosc:
                nowy_wiersz.append(255)
            else:
                nowy_wiersz.append(0)
        binarny_obraz.append(nowy_wiersz)

    return binarny_obraz


def wczytaj_obraz_z_txt(nazwa_pliku):
    with open(nazwa_pliku, 'r') as file:
        lines = file.readlines()

        # strip - usuwa białe znaki na poczatku i koncu kazdej lini
        # split - dzieli linie na poszczególne elementy ktore są oddzielone białymi znakami
        # map(int, ..) konwert ciag na int
        image_array = [list(map(int, line.strip().split())) for line in lines]

    # lista list -> dwuwumiarowa tablica
    return np.array(image_array, dtype=np.uint8)


def wczytaj_obraz_z_jpg(nazwa_pliku):
    # Odczytujemy obraz za pomocą Pillow i konwertujemy na tablicę NumPy
    obraz = Image.open(nazwa_pliku).convert('L')  # 'L' to konwersja do skali szarości
    image_array = np.array(obraz)
    return image_array


def wyswietl_obraz(image_array):
    plt.imshow(image_array, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()


def main():
    nazwa_pliku = 'Mapa_MD_no_terrain_low_res_Gray.txt'
    # obraz = wczytaj_obraz_z_txt(nazwa_pliku)

    nazwa_pliku = 'mr-incredible.jpg'  # Podaj nazwę pliku JPG
    obraz = wczytaj_obraz_z_jpg(nazwa_pliku)

    wyswietl_obraz(obraz)

    while True:
        print("Wybierz operacje:")
        print("1: Przyciemnianie obrazu")
        print("2: Rozjaśnianie obrazu")
        print("3: Binaryzacja obrazu")
        print("4: Wyświetl orginanlny obraz")
        print("5: Zakończ")

        wybor = input("Wybierz operację: ")

        if wybor == '1':
            procent = int(input("Podaj procent przyciemnienia (od 1 do 99): "))
            while not (1 <= procent <= 99):
                print("Procent musi być w zakresie od 1 do 99. Spróbuj ponownie")
                procent = int(input("Podaj procent przyciemnienia (od 1 do 99): "))
            przyciemniony_obraz = sciemnij_obraz(obraz, procent)
            wyswietl_obraz(przyciemniony_obraz)

        elif wybor == '2':

            liczba_krokow = 3
            obraz_kopia = obraz.copy()

            for i in range(1, liczba_krokow + 1):
                procent = int(input(f'Krok {i}: Podaj procent rozjaśnienia (od 10 do 20): '))
                while not (10 <= procent <= 20):
                    print("Procent musi być w zakresie od 10 do 20. Spróbuj ponownie")
                    procent = int(input(f'Krok {i}: Podaj procent rozjaśnienia (od 10 do 20): '))

                obraz_kopia = rozjasnij_obraz_krokowo(obraz_kopia, procent)
                wyswietl_obraz(obraz_kopia)

        elif wybor == '3':
            prog = int(input("Podaj próg binaryzacji (od 1 do 99%): "))
            while not (1 <= prog <= 99):
                print("Procent binaryzacji musi być w zakresie od 1 do 99")
                prog = int(input("Podaj próg binaryzacji (od 1 do 99%): "))

            obraz_binarny = binaryzacja_obraz(obraz, prog)
            wyswietl_obraz(obraz_binarny)

            if np.all(obraz_binarny == 255):
                print("Obraz jest cały biały")

        elif wybor == '4':
            wyswietl_obraz(obraz)

        elif wybor == '5':
            break

        else:
            print("Błędny wybór")


if __name__ == "__main__":
    main()
