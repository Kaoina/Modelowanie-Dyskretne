import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import tkinter as tk
from PIL import Image, ImageTk
import automat_conway


def random_grid(rows, cols, prob_alive=0.2):
    grid = np.random.choice([0, 1], size=(rows, cols), p=[1 - prob_alive, prob_alive])
    return grid


def save_grid_png_black_and_white(grid, iteration, output_folder="life_images"):
    plt.imshow(grid, cmap=mcolors.ListedColormap(['white', 'black']))
    plt.axis('off')
    plt.savefig(f"{output_folder}/life_{iteration}.png", bbox_inches='tight', pad_inches=0)
    plt.close()


def create_gif_from_pngs(num_iterations, output_folder="life_images", gif_name="game_of_life.gif"):
    images = [Image.open(f"{output_folder}/life_{i}.png") for i in range(num_iterations)]
    images[0].save(gif_name, save_all=True, append_images=images[1:], loop=0)


def game_of_life(rows=50, cols=50, iterations=50, prob_alive=0.2):
    grid = random_grid(rows, cols, prob_alive)

    for i in range(iterations):
        save_grid_png_black_and_white(grid, i)
        grid = automat_conway.update_grid(grid, boundary_condition='reflective')

    create_gif_from_pngs(iterations)


def display_gif(gif_path):
    root = tk.Tk()
    root.title("Gra w życie")

    gif_image = Image.open(gif_path)
    frames = []

    try:
        while True:
            frame = ImageTk.PhotoImage(gif_image.copy())
            frames.append(frame)
            gif_image.seek(len(frames))
    except EOFError:
        pass

    label = tk.Label(root)
    label.pack()

    def update_frame(index):
        frame = frames[index]
        label.config(image=frame)
        root.after(300, update_frame, (index + 1) % len(frames))  # co 300ms

    root.after(0, update_frame, 0)

    root.mainloop()


# main
game_of_life(rows=200, cols=200, iterations=20, prob_alive=0.3)
file_path = "game_of_life.gif"
display_gif(file_path)