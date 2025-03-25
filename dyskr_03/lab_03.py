import matplotlib.pyplot as plt
import numpy as np
import csv


def split_into_rules(album_number):
    rules = [int(album_number[:2]), int(album_number[2:4]), int(album_number[4:6]), 190]
    binary_rules = [format(rule, '08b') for rule in rules]  # potrzebujemy zapisu 8-bitowego
    return binary_rules


def apply_binary_rule(left, center, right, binary_rule):
    if left == 1 and center == 1 and right == 1:
        return int(binary_rule[0])
    elif left == 1 and center == 1 and right == 0:
        return int(binary_rule[1])
    elif left == 1 and center == 0 and right == 1:
        return int(binary_rule[2])
    elif left == 1 and center == 0 and right == 0:
        return int(binary_rule[3])
    elif left == 0 and center == 1 and right == 1:
        return int(binary_rule[4])
    elif left == 0 and center == 1 and right == 0:
        return int(binary_rule[5])
    elif left == 0 and center == 0 and right == 1:
        return int(binary_rule[6])
    elif left == 0 and center == 0 and right == 0:
        return int(binary_rule[7])


def cellular_automata(album_number, grid_size, num_iterations, boundary="p", selected_rule=0):
    binary_rules = split_into_rules(album_number)
    state = np.random.choice([0, 1], size=grid_size)
    # state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1]
    results = [state.copy()]

    binary_rule = binary_rules[selected_rule]

    for _ in range(num_iterations):
        new_state = state.copy()

        for j in range(grid_size):
            left, center, right = 0, state[j], 0
            if boundary == "p":  # zawijanie
                left = state[j - 1] if j > 0 else state[-1]
                center = state[j]
                right = state[(j + 1) % grid_size] if j < grid_size - 1 else state[0]

            elif boundary == "a":  # wokół zera
                left = state[j - 1] if j > 0 else 0
                center = state[j]
                right = state[j + 1] if j < grid_size - 1 else 0

            new_state[j] = apply_binary_rule(left, center, right, binary_rule)

        state = new_state.copy()
        results.append(state)

    return results


def save_to_csv(result, filename="results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(result)
    print(f"Wyniki zapisano do {filename}")


def load_from_csv(filename="results.csv"):
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        data = [list(map(int, row)) for row in reader]
    return np.array(data)


def display_as_image(data):
    num_rows, num_cols = data.shape
    new_data = np.zeros((num_rows, num_cols, 3))

    for i in range(num_rows):
        new_color = np.random.rand(3)

        for j in range(num_cols):
            if data[i, j] == 1:
                new_data[i, j] = [1.0, 1.0, 1.0]
            else:
                new_data[i, j] = new_color

    plt.imshow(new_data, interpolation="nearest")
    plt.axis("off")
    plt.show()


def main():
    album_number = input("Podaj swój numer albumu (6 cyfr): ").strip().lower()
    if len(album_number) != 6 or not album_number.isdigit():
        raise ValueError("Błędna liczba")

    grid_size = int(input("Podaj rozmiar siatki (liczba komórek): "))
    if grid_size < 0 or grid_size > 100:
        raise ValueError("Rozmiar siatki musi być w zakresie od 0 do 100.")

    num_iterations = int(input("Podaj liczbę iteracji: "))
    if num_iterations < 0 or num_iterations > 100:
        raise ValueError("Liczba iteracji musi być w zakresie od 0 do 100.")

    boundary_condition = input("Podaj typ warunku brzegowego p/a: ").strip().lower()
    if boundary_condition not in {"p", "a"}:
        raise ValueError("To ani p ani a :((")

    binary_rules = split_into_rules(album_number)
    print("Dostępne reguły:")
    for index, binary_rule in enumerate(binary_rules):
        decimal_rule = int(binary_rule, 2)  # z binarki
        print(f"{index + 1}: {decimal_rule} (binarnie: {binary_rule})")

    selected_rule = int(input("Wybierz regułę (1-4): ")) - 1
    if selected_rule not in range(4):
        raise ValueError("Niepoprawny wybór reguły (wybierz 1-4)")

    # grid_size = 19
    # num_iterations = 19

    result = cellular_automata(album_number, grid_size, num_iterations, boundary_condition, selected_rule)
    save_to_csv(result)

    data = load_from_csv("results.csv")
    display_as_image(data)

    for step, state in enumerate(result):
        print(f"Iteracja {step}: {''.join(map(str, state))}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
