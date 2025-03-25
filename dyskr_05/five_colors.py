import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import Tk, Label
from PIL import Image, ImageTk


def classify_pixel_color(r, g, b):
    color_ranges = {
        "blue": {"base": (165, 203, 231), "tolerance": 10, "output": (173, 216, 230)},   # Niebieski - woda
        "green1": {"base": (180, 215, 159), "tolerance": 10, "output": (0, 150, 0)},     # Zielony - las
        "green2": {"base": (199, 215, 163), "tolerance": 10, "output": (0, 150, 0)},     # Zielony - jakis inny las nw
        "green3": {"base": (232, 239, 223), "tolerance": 10, "output": (255, 219, 77)},  # Żółty - rolne
        "orange": {"base": (242, 222, 206), "tolerance": 11, "output": (204, 85, 0)},    # Pomarańczowy - zabudowanie
        "beige": {"base": (255, 250, 240), "tolerance": 10, "output": (204, 255, 204)},  # Jasny zielony - łąka
    }
    white = (255, 255, 255)

    def is_in_range(color, base, tolerance):
        return all(abs(c - b) <= tolerance for c, b in zip(color, base))

    for color_key, color_data in color_ranges.items():
        if is_in_range((r, g, b), color_data["base"], color_data["tolerance"]):
            return color_data["output"]

    return white


def five_colors_image(input_path, output_path):
    image = Image.open(input_path)
    image = image.convert("RGB")
    pixels = image.load()

    img_array = np.zeros((image.height, image.width, 3), dtype=np.uint8)

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            new_color = classify_pixel_color(r, g, b)
            img_array[y, x] = new_color

    new_image = Image.fromarray(img_array)
    new_image.save(output_path)

    return new_image


def show_image_in_gui(image):
    root = tk.Tk()
    root.title("Mapa Pikseli")

    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.pack()

    def on_pixel_click(event):
        x = event.x
        y = event.y
        color = image.getpixel((x, y))
        print(f"Kliknięto na piksel: ({x}, {y}), Kolor: {color}")

    label.bind("<Button-1>", on_pixel_click)

    # Uruchomienie GUI
    root.mainloop()
