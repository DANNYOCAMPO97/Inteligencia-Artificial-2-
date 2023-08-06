import numpy as np
import random
import matplotlib.pyplot as plt

# Parámetros de la simulación
num_agents = 10
num_food_sources = 10
grid_size = 10
max_steps = 100

# Clase Agente
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        # Movimiento aleatorio en una de las 8 direcciones posibles
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)])
        self.x = (self.x + dx) % grid_size
        self.y = (self.y + dy) % grid_size

    def calculate_distance(self, x, y):
        # Calcula la distancia euclidiana desde el agente hasta un punto dado (x, y)
        return np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

# Clase Comida
class FoodSource:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Inicialización de agentes y fuentes de comida
agents = [Agent(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_agents)]
food_sources = [FoodSource(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_food_sources)]

# Función para dibujar el gráfico
def draw_simulation():
    plt.clf()
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)

    # Dibuja las fuentes de comida
    for food in food_sources:
        plt.plot(food.x, food.y, 'go', markersize=10)

    # Dibuja los agentes
    for agent in agents:
        plt.plot(agent.x, agent.y, 'bo')

    plt.pause(0.1)

# Simulación
plt.ion()  # Activa el modo interactivo para mostrar el gráfico en tiempo real

for step in range(max_steps):
    for agent in agents:
        # El agente selecciona la comida más cercana y se mueve hacia ella
        if len(food_sources) > 0:
            closest_food = min(food_sources, key=lambda food: agent.calculate_distance(food.x, food.y))
            agent.move()

            # Si el agente alcanza una fuente de comida, la elimina
            if (agent.x, agent.y) == (closest_food.x, closest_food.y):
                food_sources.remove(closest_food)

    # Los agentes comparten información sobre la comida restante
    food_coords = [(food.x, food.y) for food in food_sources]
    for agent in agents:
        agent_coords = (agent.x, agent.y)
        for food_coord in food_coords:
            # Simula aprendizaje social: los agentes comparten información sobre las coordenadas de la comida
            # Cuanto más cerca esté un agente de la comida, mayor será la probabilidad de que comparta esa información
            distance_to_food = agent.calculate_distance(food_coord[0], food_coord[1])
            sharing_probability = 1 / (distance_to_food + 0.1)  # Se suma 0.1 para evitar divisiones por cero
            if random.random() < sharing_probability:
                agent.x, agent.y = food_coord

    draw_simulation()

plt.ioff()  # Desactiva el modo interactivo al final de la simulación
plt.show()  # Muestra el gráfico final
