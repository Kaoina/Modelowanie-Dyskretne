import pygame
import random

# Ustawienia
WIDTH, HEIGHT = 1400, 700
CELL_SIZE = 8
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = (HEIGHT - 50) // CELL_SIZE  # Zostaw miejsce na przyciski
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (170, 170, 170)
BUTTON_TEXT_COLOR = (0, 0, 0)

DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LGA Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Wczytaj tło
background_image = pygame.image.load("sky2.jpg")  # Zamień na ścieżkę do Twojego pliku
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


def create_wall(grid):
    mid_x = 20
    mid_y_start = 25
    mid_y_end = 35
    for y in range(GRID_HEIGHT):
        if y < mid_y_start or y >= mid_y_end:
            grid[mid_x][y] = [-1, -1, -1, -1]


def initialize_grid(density=0.3):
    grid = [[[0, 0, 0, 0] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    for x in range(19):
        for y in range(GRID_HEIGHT):
            for d in range(4):
                if random.random() < density:
                    grid[x][y][d] = 1
    return grid


def draw_grid(grid):
    # Rysuj tło
    screen.blit(background_image, (0, 0))

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            cx, cy = x * CELL_SIZE, y * CELL_SIZE
            if grid[x][y] == [-1, -1, -1, -1]:  # Ściana
                pygame.draw.rect(screen, WHITE, (cx, cy, CELL_SIZE, CELL_SIZE))
            else:
                for d, (dx, dy) in enumerate(DIRECTIONS):
                    if grid[x][y][d] == 1:
                        # Rysowanie cząstek jako kół
                        center_x = cx + CELL_SIZE // 2
                        center_y = cy + CELL_SIZE // 2
                        radius = CELL_SIZE // 3
                        pygame.draw.circle(screen, BLACK, (center_x, center_y), radius)


def draw_buttons():
    # Rysowanie białego tła pod przyciskami
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 50, WIDTH, 50))

    # Definicja przycisków
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 40, 80, 30)
    stop_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 40, 80, 30)

    # Obsługa koloru przycisków na podstawie położenia myszy
    mouse_pos = pygame.mouse.get_pos()
    start_color = BUTTON_HOVER_COLOR if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
    stop_color = BUTTON_HOVER_COLOR if stop_button.collidepoint(mouse_pos) else BUTTON_COLOR

    # Rysowanie przycisków
    pygame.draw.rect(screen, start_color, start_button)
    pygame.draw.rect(screen, stop_color, stop_button)

    # Dodanie tekstu na przyciski
    start_text = font.render("Start", True, BUTTON_TEXT_COLOR)
    stop_text = font.render("Stop", True, BUTTON_TEXT_COLOR)
    screen.blit(start_text, (WIDTH // 2 - 90, HEIGHT - 35))
    screen.blit(stop_text, (WIDTH // 2 + 30, HEIGHT - 35))

    return start_button, stop_button


def streaming(grid):
    new_grid = [[[0, 0, 0, 0] for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == [-1, -1, -1, -1]:
                new_grid[x][y] = [-1, -1, -1, -1]
            else:
                for d, (dx, dy) in enumerate(DIRECTIONS):
                    if grid[x][y][d] == 1:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                            if grid[nx][ny] == [-1, -1, -1, -1]:
                                new_grid[x][y][(d + 2) % 4] = 1
                            else:
                                new_grid[nx][ny][d] = 1
                        else:
                            new_grid[x][y][(d + 2) % 4] = 1
    return new_grid


def collision(grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] != [-1, -1, -1, -1]:
                incoming = grid[x][y]
                if incoming == [1, 0, 1, 0]:
                    grid[x][y] = [0, 1, 0, 1]
                elif incoming == [0, 1, 0, 1]:
                    grid[x][y] = [1, 0, 1, 0]
    return grid


def add_wall_on_click(grid, pos):
    x, y = pos
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        if grid[grid_x][grid_y] == [-1, -1, -1, -1]:
            grid[grid_x][grid_y] = [0, 0, 0, 0]  # Usuń ścianę
        else:
            grid[grid_x][grid_y] = [-1, -1, -1, -1]  # Dodaj ścianę


start_grid = initialize_grid(density=0.5)
create_wall(start_grid)

running = True
simulating = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                pos = event.pos
                start_button, stop_button = draw_buttons()
                if start_button.collidepoint(pos):
                    simulating = True
                elif stop_button.collidepoint(pos):
                    simulating = False
                else:
                    add_wall_on_click(start_grid, pos)

    if simulating:
        start_grid = streaming(start_grid)
        start_grid = collision(start_grid)

    draw_grid(start_grid)
    draw_buttons()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
