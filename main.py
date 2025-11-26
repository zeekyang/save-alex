# Save Alex
# hello

import pygame
import sys

pygame.init()

# Game Settings

TILE = 32
LIGHT_RADIUS = 100
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save Alex")
clock = pygame.time.Clock()

# Maze Layout
# A = Alex start
# B = Black hole (goal)
# # = Wall
# space = open path
maze = [
    "##########",
    "#A     # #",
    "# ### ## #",
    "#   #    #",
    "### #### #",
    "#      B #",
    "##########"
]

rows = len(maze)
cols = len(maze[0])

# Find Starting Position
for y in range(rows):
    for x in range(cols):
        if maze[y][x] == "A":
            player_x, player_y = x, y
        if maze[y][x] == "B":
            blackhole_pos = (x, y)

# Helper Functions
def draw_maze():
    """Draw all maze tiles: walls and black hole."""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):

            # Walls
            if cell == "#":
                pygame.draw.rect(screen, (80, 80, 80),
                                 (x*TILE, y*TILE, TILE, TILE))

            # Black hole (goal)
            if cell == "B":
                center = (x*TILE + TILE//2, y*TILE + TILE//2)
                pygame.draw.circle(screen, (20, 0, 40), center, TILE//2)
                pygame.draw.circle(screen, (0, 0, 0), center, TILE//3)

def draw_player():
    """Draw Alex (green square)."""
    pygame.draw.rect(screen, (0, 255, 0),
                     (player_x*TILE, player_y*TILE, TILE, TILE))

def handle_movement():
    """Move character and prevent walking into walls."""
    global player_x, player_y

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0
    if keys[pygame.K_UP]:    dy = -1
    if keys[pygame.K_DOWN]:  dy = 1
    if keys[pygame.K_LEFT]:  dx = -1
    if keys[pygame.K_RIGHT]: dx = 1

    # Check tile collision
    new_x = player_x + dx
    new_y = player_y + dy

    if maze[new_y][new_x] != "#":
        player_x = new_x
        player_y = new_y

def draw_lighting():
    # Dark overlay with a circular hole around the player.
    dark = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 230))  # mostly opaque darkness

    # Position of light
    px = player_x*TILE + TILE//2
    py = player_y*TILE + TILE//2

    # Cut a hole
    pygame.draw.circle(dark, (0, 0, 0, 0), (px, py), LIGHT_RADIUS)

    # Small spotlight toward the black hole
    bx = blackhole_pos[0]*TILE + TILE//2
    by = blackhole_pos[1]*TILE + TILE//2
    pygame.draw.line(dark, (0, 0, 0, 0), (px, py), (bx, by), 40)

    screen.blit(dark, (0, 0))

def check_win():
    """Return True if player reached the black hole."""
    return (player_x, player_y) == blackhole_pos

# Game Loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update movement
    handle_movement()

    # Draw map & player
    screen.fill((0, 0, 0))
    draw_maze()
    draw_player()

    # Lighting (must come last)
    draw_lighting()

    pygame.display.flip()

    # Win condition
    if check_win():
        print("Alex escaped the dimension! You win!")
        pygame.time.delay(1500)
        running = False

pygame.quit()
sys.exit()
