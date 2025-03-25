import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def wczytaj_obraz(nazwa_pliku):
    obraz = Image.open(nazwa_pliku).convert('L')
    image_array = np.array(obraz)
    return image_array


def wyswietl_obraz(image_array):
    plt.imshow(image_array, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()


def dylatacja(image_array, r):
    dyl_obr = np.zeros_like(image_array)
    rows, cols = image_array.shape

    for i in range(rows):
        for j in range(cols):
            neighborhood = []

            for ni in range(i - r, i + r + 1):
                for nj in range(j - r, j + r + 1):
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighborhood.append(image_array[ni, nj])
                    else:
                        neighborhood.append(255)
            dyl_obr[i, j] = min(neighborhood)

    return dyl_obr


def erozja(image_array, r):
    ero_obr = np.zeros_like(image_array)
    rows, cols = image_array.shape

    for i in range(rows):
        for j in range(cols):
            neighborhood = []

            for ni in range(i - r, i + r + 1):
                for nj in range(j - r, j + r + 1):
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighborhood.append(image_array[ni, nj])
                    else:
                        neighborhood.append(0)

            ero_obr[i, j] = max(neighborhood)
    return ero_obr


def otwarcie(image_array, r):
    eroded = erozja(image_array, r)
    opened = dylatacja(eroded, r)
    return opened


def zamkniecie(image_array, r):
    dilated = dylatacja(image_array, r)
    closed = erozja(dilated, r)
    return closed


def wczytaj_maske_z_kodu():
    print("Wybierz rodzaj maski: ")
    print("1: Maska Gaussa")
    print("2: Maska upper pass")
    print("3: Maska low pass")
    print("4: Maska chyba Gauss ale o r=3")
    wybor = input("Podaj wybor: ")
    maska = None

    if wybor == '1':
        maska = np.array([[1, 2, 1],
                          [2, 4, 2],
                          [1, 2, 1]]) / 16
    elif wybor == '2':
        maska = np.array([[-1, -1, -1],
                          [-1, 9, -1],
                          [-1, -1, -1]])
    elif wybor == '3':
        maska = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]]) / 9
    elif wybor == '4':
        maska = np.array([[1, 1, 2, 2, 2, 1, 1],
                          [1, 2, 2, 4, 2, 2, 1],
                          [2, 2, 4, 8, 4, 2, 2],
                          [2, 4, 8, 16, 8, 4, 2],
                          [2, 2, 4, 8, 4, 2, 2],
                          [1, 2, 2, 4, 2, 2, 1],
                          [1, 1, 2, 2, 2, 1, 1]])

    else:
        print("Błędny wybór")

    return maska


def wczytaj_maske_z_pliku():
    print("Wybierz rodzaj maski(txt): ")
    print("1: Maska Gaussa 1r")
    print("1: Maska Gaussa 2r")
    print("3: Maska Sobel")
    print("4: Maska co ją sobie wymyslilam")
    nazwa_pliku = None

    wybor = input("Podaj wybor: ")

    if wybor == '1':
        nazwa_pliku = 'gaus_1.txt'
    elif wybor == '2':
        nazwa_pliku = 'gaus_2.txt'
    elif wybor == '3':
        nazwa_pliku = 'sobel.txt'
    elif wybor == '4':
        nazwa_pliku = 'maska_kreatywna.txt'
    else:
        print("Błędny wybór")

    with open(nazwa_pliku, 'r') as f:
        maska = np.loadtxt(f)
    return maska


def konwolucja(image_array, maska):
    kon_obr = np.zeros_like(image_array)

    rows, cols = image_array.shape
    mask_size = maska.shape[0]
    ext_pix = mask_size // 2

    for i in range(rows):
        for j in range(cols):
            neighbourhood = []
            for ni in range(-ext_pix, ext_pix + 1):
                for nj in range(-ext_pix, ext_pix + 1):
                    if 0 <= i + ni < rows and 0 <= j + nj < cols:
                        neighbourhood.append(image_array[i + ni, j + nj] * maska[ni + ext_pix, nj + ext_pix])
                    else:
                        neighbourhood.append(0)
            kon_obr[i, j] = sum(neighbourhood)

    return kon_obr


def main():
    nazwa_pliku = 'Mapa_MD_no_terrain_low_res_Gray.bmp'
    # nazwa_pliku = 'frogs.bmp'
    # nazwa_pliku = 'frogy.bmp'
    # nazwa_pliku = 'frog_bw.bmp'
    obraz = wczytaj_obraz(nazwa_pliku)
    wyswietl_obraz(obraz)

    while True:
        print("Wybierz operacje:")
        print("1: Dylatacja")
        print("2: Erozja")
        print("3: Otwarcie morfologiczne")
        print("4: Zamknięcie morfologiczne")
        print("5: Konwolucja (maski z kodu)")
        print("6: Konwolucja (maski z pliku)")
        print("7: Wyświetl orginanlny obraz")
        print("8: Zakończ")
        wybor = input("Wybierz operację: ")

        if wybor == '1':
            r = int(input("Wybierz promien: "))
            obraz_dylatowany = dylatacja(obraz, r)
            wyswietl_obraz(obraz_dylatowany)

        elif wybor == '2':
            r = int(input("Wybierz promien: "))
            obraz_erozjowany = erozja(obraz, r)
            wyswietl_obraz(obraz_erozjowany)

        elif wybor == '3':
            r = int(input("Wybierz promien: "))
            obraz_otwarty = otwarcie(obraz, r)
            wyswietl_obraz(obraz_otwarty)

        elif wybor == '4':
            r = int(input("Wybierz promien: "))
            obraz_zamkniety = zamkniecie(obraz, r)
            wyswietl_obraz(obraz_zamkniety)

        elif wybor == '5':
            maska = wczytaj_maske_z_kodu()
            print(maska)

            obraz_po_konwolucji = konwolucja(obraz, maska)
            wyswietl_obraz(obraz_po_konwolucji)

        elif wybor == '6':
            maska = wczytaj_maske_z_pliku()
            print(maska)

            obraz_po_konwolucji = konwolucja(obraz, maska)
            wyswietl_obraz(obraz_po_konwolucji)

        elif wybor == '7':
            wyswietl_obraz(obraz)

        elif wybor == '8':
            break

        else:
            print("Błędny wybór")


if __name__ == "__main__":
    main()
