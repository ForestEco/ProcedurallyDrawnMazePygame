import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 15
FPS = 30

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Set up the clock
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

def generate_maze(width, height):
  maze = [[0 for _ in range(width)] for _ in range(height)]

  max_rect_size = min(width // 10, height // 10)

  for _ in range(width * height // max_rect_size):
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    w = random.randint(1, max_rect_size)
    h = random.randint(1, max_rect_size)

    overlaps = False
    for i in range(max(0, y - h // 2), min(height, y + h // 2 + 1)):
      for j in range(max(0, x - w // 2), min(width, x + w // 2 + 1)):
        if maze[i][j] == 1:
          overlaps = True
          break

    if not overlaps:
      for i in range(max(0, y - h // 2), min(height, y + h // 2 + 1)):
        for j in range(max(0, x - w // 2), min(width, x + w // 2 + 1)):
          maze[i][j] = 1

  return maze

# Define the size of the maze
mazeWd, mazeHt = 30, 30

# Generate the maze
maze = generate_maze(mazeWd, mazeHt)

# Print the maze
for row in maze:
    print(''.join([' ' if cell == 0 else '#' for cell in row]))

# Define the solid area
solidArea = [(x, y) for x in range(mazeWd) for y in range(mazeHt) if x in range(10, 20) and y in range(10, 20)]
# Make the solid area a wall
for x, y in solidArea:
    maze[y][x] = 5

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        if 0 <= self.x < len(maze[0]) and 0 <= self.y < len(maze):
            pygame.draw.rect(win, BLUE, (self.x * CELL_SIZE + 1, self.y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2))
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            if maze[new_y][new_x] != 1:
                self.x = new_x
                self.y = new_y

player = Player(1, 1)
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)

    if player.x == len(maze[0]) - 2 and player.y == len(maze) - 2:
        print("You win!")
        run = False

    WIN.fill(BLACK)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(WIN, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(WIN, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(WIN, RED, ((len(maze[0]) - 2) * CELL_SIZE, (len(maze) - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the outermost pixels of the entire maze
    pygame.draw.rect(WIN, WHITE, (0, 0, mazeWd * CELL_SIZE, mazeHt * CELL_SIZE), 5)

    # Draw a white rectangle around the maze
    player.draw(WIN)

    pygame.display.update()
pygame.quit()