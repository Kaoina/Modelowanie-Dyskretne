import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
import five_colors
import closing_operation
import pixelized

FIRE_COLOR = (255, 0, 0)  # Czerwony dla ognia
BURNT_COLOR = (50, 50, 50)  # Ciemnoszary dla spalonych obszarów


def simulate_fire(image, ignition_point, steps=200, scale_factor=5, humidity=0.5):
    new_width = image.width // scale_factor
    new_height = image.height // scale_factor
    scaled_image = image.resize((new_width, new_height), Image.Resampling.NEAREST)

    img_array = np.array(scaled_image)
    height, width, _ = img_array.shape

    STATE_UNBURNABLE = 0  # Zapalne
    STATE_FLAMMABLE = 1  # Zie palne
    STATE_BURNING = 2  # Płonie
    STATE_BURNT = 3  # Spalony

    flammable_colors = {
        (0, 150, 0): 0.7,    # Las
        (255, 219, 77): 0.3, # Pola
        (204, 255, 204): 0.6, # Łąki
        (204, 85, 0): 0.9    # Budynki
    }

    cell_states = np.full((height, width), STATE_UNBURNABLE, dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            color = tuple(img_array[y, x])
            if color in flammable_colors:
                cell_states[y, x] = STATE_FLAMMABLE

    x, y = ignition_point
    x = x // scale_factor
    y = y // scale_factor  # Skalowanie punktu zapłonu

    # PODPALAMY LETSGOOO
    if cell_states[y, x] == STATE_FLAMMABLE:
        cell_states[y, x] = STATE_BURNING

    frames = []

    for step in range(steps):
        new_burning = []

        for y in range(height):
            for x in range(width):
                if cell_states[y, x] == STATE_BURNING:
                    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if cell_states[ny, nx] == STATE_FLAMMABLE:
                                color = tuple(img_array[ny, nx])
                                base_prob = flammable_colors.get(color, 0)

                                humidity_effect = 1 - (humidity * 0.3)
                                prob = base_prob * humidity_effect

                                if np.random.rand() < prob:
                                    new_burning.append((ny, nx))

                    cell_states[y, x] = STATE_BURNT
                    img_array[y, x] = BURNT_COLOR

        for ny, nx in new_burning:
            cell_states[ny, nx] = STATE_BURNING
            img_array[ny, nx] = FIRE_COLOR

        upscaled_img = Image.fromarray(img_array).resize(
            (image.width, image.height), Image.Resampling.NEAREST
        )
        frames.append(upscaled_img)

        if not new_burning and step >= 10:
            break

    return frames


def animate_fire(frames, duration=100):
    root = tk.Tk()
    root.title("Symulacja Pożaru")
    label = tk.Label(root)
    label.pack()

    def update_frame(index):
        if index < len(frames):
            photo = ImageTk.PhotoImage(frames[index])
            label.config(image=photo)
            label.image = photo
            root.after(duration, update_frame, index + 1)
        else:
            print("Symulacja zakończona.")
            root.destroy()

    update_frame(0)
    root.mainloop()


def select_ignition_point(image_path, callback):
    root = tk.Tk()
    root.title("Wybierz punkt zapłonu")
    img = Image.open(image_path)
    photo = ImageTk.PhotoImage(img)

    selected_point = None
    coords_label = tk.Label(root, text="Współrzędne: (X, Y)")
    coords_label.pack()

    def on_click(event):
        nonlocal selected_point
        x, y = event.x, event.y
        print(f"Wybrano punkt zapłonu: ({x}, {y})")
        selected_point = (x, y)
        coords_label.config(text=f"Współrzędne: ({x}, {y})")
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        draw.rectangle([selected_point[0]-5, selected_point[1]-5, selected_point[0]+5, selected_point[1]+5], outline="yellow", width=3)
        photo_copy = ImageTk.PhotoImage(img_copy)
        label.config(image=photo_copy)
        label.image = photo_copy

    def on_start():
        if selected_point:
            humidity = humidity_slider.get()
            root.destroy()
            callback(selected_point, humidity)
        else:
            print("Nie wybrano punktu zapłonu!")

    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

    start_button = tk.Button(root, text="Start", command=on_start)
    start_button.pack()

    humidity_slider = tk.Scale(root, from_=0, to_=1, resolution=0.01, orient=tk.HORIZONTAL, label="Wilgotność")
    humidity_slider.set(0.5)
    humidity_slider.pack()

    label.bind("<Button-1>", on_click)
    root.mainloop()


def main():
    # file_path = 'Dobczyce_podmokłe.png'
    # file_path = 'Weglowka.png'
    file_path = "eksport.png"  # Palimy AGH

    # Operacja zamknięcia
    closing_path = 'closed_image.png'
    closing_operation.closing_operation(file_path, closing_path, size=5)

    # Redukcja kolorów
    narrow_path = 'narrow_image.png'
    narrow_image = five_colors.five_colors_image(closing_path, narrow_path)

    # Redukcja pixeli
    pixelized_path = 'pixelized_image.png'
    pixelized_image = pixelized.display_image(narrow_path, pixelized_path)

    def start_simulation(ignition_point, humidity):
        frames = simulate_fire(narrow_image, ignition_point, humidity=humidity)

        animate_fire(frames)

    select_ignition_point(pixelized_path, start_simulation)


if __name__ == "__main__":
    main()
