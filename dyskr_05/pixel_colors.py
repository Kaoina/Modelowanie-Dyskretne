from PIL import Image, ImageTk
import tkinter as tk


def get_pixel_color(event):
    x, y = event.x, event.y

    pixel_color = image.getpixel((x, y))

    color_label.config(text=f"Kolor piksela: {pixel_color}")


image_path = 'reduced_colors_image.png'
image = Image.open(image_path).convert('RGB')

root = tk.Tk()
root.title("Sprawdź kolor piksela")

tk_image = ImageTk.PhotoImage(image)

image_label = tk.Label(root, image=tk_image)
image_label.pack()

color_label = tk.Label(root, text="Kliknij w obraz, aby sprawdzić kolor piksela.")
color_label.pack()

image_label.bind("<Button-1>", get_pixel_color)

root.mainloop()