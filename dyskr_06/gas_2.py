import pygame
import numpy as np

# Ustawienia okna symulacji
SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 600
EXTRA_SPACE = 80  # Dodatkowa przestrzeń na przycisk
CELL_DIMENSION = 15  # Wymiary komórki
GRID_COLS = SCREEN_WIDTH // CELL_DIMENSION
GRID_ROWS = SCREEN_HEIGHT // CELL_DIMENSION

# Kolory
BACKGROUND = (0, 0, 0)
PARTICLE = (0, 255, 0)
BARRIER = (255, 255, 255)
BUTTON = (34, 139, 34)
BUTTON_TEXT = (255, 255, 255)

# Symulacja D2Q4
DIRECTIONS = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # Dół, lewo, góra, prawo
TAU = 1
WEIGHT_VALUES = [0.25, 0.25, 0.25, 0.25]

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + EXTRA_SPACE))  # Zwiększona wysokość
pygame.display.set_caption("Symulacja LBM")
clock = pygame.time.Clock()

# Ustawienia przycisku
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = SCREEN_HEIGHT + (EXTRA_SPACE - BUTTON_HEIGHT) // 2  # Poza obszarem symulacji


def setup_simulation():
    f_in = np.zeros((GRID_COLS, GRID_ROWS, 4))
    f_eq = np.zeros_like(f_in)
    f_out = np.zeros_like(f_in)
    concentration_grid = np.zeros((GRID_COLS, GRID_ROWS))
    barrier_grid = np.zeros((GRID_ROWS, GRID_COLS), dtype=bool)

    barrier_x_position = GRID_COLS // 2
    for y in range(GRID_ROWS):
        barrier_grid[y, barrier_x_position] = True

    concentration_grid[:, :] = 0.0
    concentration_grid[:GRID_COLS // 2, :] = 1.0
    for i in range(4):
        f_in[:, :, i] = concentration_grid * WEIGHT_VALUES[i]

    return f_in, f_eq, f_out, concentration_grid, barrier_grid


# Rysowanie siatki i bariery
def render_grid_and_wall(concentration_grid, barrier_grid):
    screen.fill(BACKGROUND)

    for x in range(GRID_COLS):
        for y in range(GRID_ROWS):
            if barrier_grid[y, x]:
                pygame.draw.rect(screen, BARRIER, (x * CELL_DIMENSION, y * CELL_DIMENSION, CELL_DIMENSION, CELL_DIMENSION))
            else:
                color_intensity = int(255 * concentration_grid[x, y])
                color = (min(color_intensity, 143), min(color_intensity, 188), min(color_intensity, 143))
                pygame.draw.rect(screen, color, (x * CELL_DIMENSION, y * CELL_DIMENSION, CELL_DIMENSION, CELL_DIMENSION))


# Rysowanie przycisku
def render_button(text):
    pygame.draw.rect(screen, BUTTON, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(text_surface, text_rect)


# Funkcje symulacji (streaming, collision itp.)
def stream_particles(f_out, barrier_grid):
    f_in = np.zeros_like(f_out)

    for i, (dx, dy) in enumerate(DIRECTIONS):
        src_x = np.clip(np.arange(GRID_COLS) - dx, 0, GRID_COLS - 1)
        src_y = np.clip(np.arange(GRID_ROWS) - dy, 0, GRID_ROWS - 1)
        f_in[:, :, i] = f_out[src_x[:, None], src_y, i]

    for i, (dx, dy) in enumerate(DIRECTIONS):
        bounce_dir = (i + 2) % 4
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                if barrier_grid[y, x]:
                    f_in[x, y, i] = f_out[x, y, bounce_dir]

    return f_in


def calculate_equilibrium(concentration_grid):
    f_eq = np.zeros((GRID_COLS, GRID_ROWS, 4))
    for i, _ in enumerate(DIRECTIONS):
        f_eq[:, :, i] = WEIGHT_VALUES[i] * concentration_grid
    return f_eq


def update_concentration(f_in):
    return np.sum(f_in, axis=2)


def apply_collision(f_in, f_eq):
    return f_in + (f_eq - f_in) / TAU


# Główna pętla symulacji
def run_simulation():
    f_in, f_eq, f_out, concentration_grid, barrier_grid = setup_simulation()
    running = True
    simulation_active = False
    fps = 60

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if BUTTON_X <= mouse_x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouse_y <= BUTTON_Y + BUTTON_HEIGHT:
                    simulation_active = True
                    for dy in range(-16, 18):
                        barrier_grid[GRID_ROWS // 2 + dy, GRID_COLS // 2] = False

        if simulation_active:
            f_eq = calculate_equilibrium(concentration_grid)
            f_out = apply_collision(f_in, f_eq)
            f_in = stream_particles(f_out, barrier_grid)
            concentration_grid = update_concentration(f_in)

        render_grid_and_wall(concentration_grid, barrier_grid)
        render_button("Start")
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
