import tkinter as tk
import numpy as np
import csv
import glob
import automat_conway


def create_initial_grid(rows, cols):
    return np.zeros((rows, cols), dtype=int)


def random_grid(rows, cols, prob_alive=0.2):
    grid = np.random.choice([0, 1], size=(rows, cols), p=[1 - prob_alive, prob_alive])
    return grid


# Funkcje interfejsu
def toggle_cell(event):
    cell_x, cell_y = event.x // cell_size, event.y // cell_size
    if 0 <= cell_x < cols and 0 <= cell_y < rows:
        initial_grid[cell_y, cell_x] = 1 - initial_grid[cell_y, cell_x]
        draw_cell(cell_x, cell_y)


def draw_cell(x, y):
    x1, y1 = x * cell_size, y * cell_size  # lewy górny
    x2, y2 = x1 + cell_size, y1 + cell_size  # prawy dolny
    color = "black" if initial_grid[y, x] == 1 else "white"
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")


def draw_grid():
    canvas.delete("all")
    for r in range(rows):
        for c in range(cols):
            color = "black" if initial_grid[r, c] == 1 else "white"
            canvas.create_rectangle(c * cell_size, r * cell_size, (c + 1) * cell_size, (r + 1) * cell_size,
                                    fill=color, outline="pink")


def run_simulation_step():
    global initial_grid

    initial_grid = automat_conway.update_grid(initial_grid, boundary_condition.get())

    draw_grid()

    if running_simulation:
        root.after(100, run_simulation_step)  # Opóźnienie 100 ms


# Funkcje do zarządzania plikami CSV

def load_grid_from_csv(file_path):
    global initial_grid, rows, cols
    with open(file_path, mode='r') as csvfile:
        reader = csv.reader(csvfile)
        loaded_grid = [list(map(int, row)) for row in reader]
    rows, cols = len(loaded_grid), len(loaded_grid[0])
    initial_grid = np.array(loaded_grid)
    draw_grid()


def save_grid_to_csv(grid, file_path):
    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in grid:
            writer.writerow(row)


def update_csv_file_list():
    csv_files = glob.glob("*.csv")
    csv_file_dropdown['menu'].delete(0, 'end')
    for file in csv_files:
        csv_file_dropdown['menu'].add_command(label=file, command=lambda f=file: csv_file_var.set(f))


# Funkcja zapisu i uruchomienia symulacji
def save_and_run():
    filename = file_name_entry.get() + ".csv"
    save_grid_to_csv(initial_grid, filename)
    update_csv_file_list()
    start_simulation()


# Funkcja do uruchomienia symulacji
def start_simulation():
    global running_simulation
    running_simulation = True
    run_simulation_step()


def stop_simulation():
    global running_simulation
    running_simulation = False


# Funkcja generująca losową siatkę
def generate_random_grid():
    global initial_grid
    initial_grid = random_grid(rows, cols, prob_alive=0.2)
    draw_grid()


# GUI w tkinter

# Ustawienia okna
root = tk.Tk()
root.title("Game of Life - Ustawienia początkowe")

# Ustawienie okna na pełny ekran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

rows, cols = 100, 100
initial_grid = create_initial_grid(rows, cols)
cell_size = 15

# Lewa ramka z ustawieniami
left_frame = tk.Frame(root, width=300, height=screen_height)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(left_frame, text="Ustawienia", font=("Arial", 16)).pack(pady=10)

tk.Label(left_frame, text="Wybierz plik CSV jako początkową siatkę:").pack(pady=5)
csv_file_var = tk.StringVar(value="Wybierz plik")
csv_file_dropdown = tk.OptionMenu(left_frame, csv_file_var, ())
csv_file_dropdown.pack(pady=5)
update_csv_file_list()

load_button = tk.Button(left_frame, text="Załaduj siatkę", command=lambda: load_grid_from_csv(csv_file_var.get()))
load_button.pack(pady=5)

boundary_condition = tk.StringVar(value="periodic")  # Domyślny warunek brzegowy
tk.Label(left_frame, text="Wybierz warunek brzegowy:").pack(pady=5)

periodic_button = tk.Radiobutton(left_frame, text="Periodyczny", variable=boundary_condition, value="periodic")
periodic_button.pack()

reflective_button = tk.Radiobutton(left_frame, text="Odbijający", variable=boundary_condition, value="reflective")
reflective_button.pack()

tk.Label(left_frame, text="Nazwa pliku CSV:").pack(pady=5)
file_name_entry = tk.Entry(left_frame)
file_name_entry.pack(pady=5)

save_button = tk.Button(left_frame, text="Zapisz i Uruchom", command=save_and_run)
save_button.pack(pady=10)

# Przycisk do generowania losowej siatki
random_grid_button = tk.Button(left_frame, text="Losowa Siatka", command=generate_random_grid)
random_grid_button.pack(pady=10)

# Prawa ramka z wizualizacją
right_frame = tk.Frame(root, width=screen_width - 300, height=screen_height)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(right_frame, width=cols * cell_size, height=rows * cell_size, bg="white")
canvas.pack(pady=20)
canvas.bind("<Button-1>", toggle_cell)

# Przycisk do zatrzymania symulacji
stop_button = tk.Button(left_frame, text="Zatrzymaj symulację", command=stop_simulation)
stop_button.pack(pady=10)

# Rysowanie początkowej siatki
draw_grid()

root.mainloop()
