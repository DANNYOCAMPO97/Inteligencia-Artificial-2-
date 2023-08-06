import numpy as np
import random
import tkinter as tk

# Definir el número de filas y columnas de la matriz
ROWS = 5
COLS = 5

# Tamaño de la población
POPULATION_SIZE = 50

# Probabilidad de mutación
MUTATION_RATE = 0.2

# Número máximo de generaciones
MAX_GENERATIONS = 100

def create_random_individual():
    row = random.randint(0, ROWS - 1)
    col = random.randint(0, COLS - 1)
    return (row, col)

def fitness(individual, matrix):
    row, col = individual
    return abs(matrix[row][col] - np.max(matrix))

def selection(population, matrix):
    fitness_values = [fitness(individual, matrix) for individual in population]
    total_fitness = sum(fitness_values)
    probabilities = [fitness_value / total_fitness for fitness_value in fitness_values]

    selected = random.choices(population, probabilities, k=len(population))
    return selected

def crossover(parent1, parent2):
    split_point = random.randint(0, len(parent1))
    child1 = parent1[:split_point] + parent2[split_point:]
    child2 = parent2[:split_point] + parent1[split_point:]
    return child1, child2

def mutation(individual):
    row, col = individual

    if random.random() < MUTATION_RATE:
        # Realizar una mutación en la fila
        row = random.randint(0, ROWS - 1)

    if random.random() < MUTATION_RATE:
        # Realizar una mutación en la columna
        col = random.randint(0, COLS - 1)

    return (row, col)

def genetic_algorithm(matrix):
    population = [create_random_individual() for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        population = selection(population, matrix)

        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutation(child1), mutation(child2)])

        population = new_population

    best_individual = min(population, key=lambda individual: fitness(individual, matrix))
    return best_individual

# Función para mostrar la matriz en una ventana gráfica
def display_matrix(matrix, best_position):
    root = tk.Tk()
    root.title("Matriz y posición del número máximo")

    # Crear una tabla para mostrar la matriz
    for i in range(ROWS):
        for j in range(COLS):
            label = tk.Label(root, text=str(matrix[i][j]), padx=20, pady=10)
            label.grid(row=i, column=j)

            if (i, j) == best_position:
                # Resaltar la posición del número máximo con un color diferente
                label.config(bg="yellow")

    root.mainloop()

if __name__ == "__main__":
    # Ejemplo de matriz de números
    matrix = np.random.randint(0, 100, size=(ROWS, COLS))
    print("Matriz:")
    print(matrix)

    best_position = genetic_algorithm(matrix)
    print("Coordenadas del número máximo:", best_position)
    print("Número máximo:", matrix[best_position[0]][best_position[1]])

    # Mostrar la matriz en una ventana gráfica
    display_matrix(matrix, best_position)
