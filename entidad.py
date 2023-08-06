import pygame
import random

# Dimensiones de la ventana gráfica
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores (formato RGB)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 'up':
            self.y -= 1
        elif direction == 'down':
            self.y += 1
        elif direction == 'left':
            self.x -= 1
        elif direction == 'right':
            self.x += 1

def check_collision(entities):
    positions = [(entity.x, entity.y) for entity in entities]
    return len(set(positions)) != len(entities)

def avoid_collision(entity, entities):
    directions = ['up', 'down', 'left', 'right']
    random.shuffle(directions)

    for direction in directions:
        temp_x, temp_y = entity.x, entity.y
        if direction == 'up':
            temp_y -= 1
        elif direction == 'down':
            temp_y += 1
        elif direction == 'left':
            temp_x -= 1
        elif direction == 'right':
            temp_x += 1

        if (temp_x, temp_y) not in [(ent.x, ent.y) for ent in entities]:
            entity.move(direction)
            break

def main(num_entities, num_steps):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Artificial Life")

    entities = [Entity(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(num_entities)]

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for entity in entities:
            avoid_collision(entity, entities)
            pygame.draw.circle(screen, RED, (entity.x, entity.y), 5)

        pygame.display.flip()
        clock.tick(10)

        if check_collision(entities):
            print("Collision occurred.")
            break

    pygame.quit()

if __name__ == "__main__":
    num_entities = 10
    num_steps = 1000
    main(num_entities, num_steps)
