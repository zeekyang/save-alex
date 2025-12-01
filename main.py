# Save Alex
import pygame
import sys

pygame.init()

# Game Settings
TILE = 55
LIGHT_RADIUS = 100
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
FPS = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save Alex")
clock = pygame.time.Clock()

# Maze Layout
maze = [
    "############################",
    "#A      # ##  ##         # #",
    "# ## ##        # ## # # ## #",
    "   #### # #### #### # #    #",
    " #            ###   ###### #",
    " #  ###### # ##   # ##     #",
    " #  ###  # #   ## #### ## ##",
    " #    # ## #####    #    ###",
    "####### ##     # ### # #   #",
    "####   #   ### #   # ### # #",
    "##  ##   ####  # ### #   # #",
    "###### ######### # # # #####",
    "#                    #    B#",
    "############################"
]

rows = len(maze)
cols = len(maze[0])

# Load Images
player_image = pygame.image.load("Alex.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (TILE, TILE))

blackhole_image = pygame.image.load("black_hole.png").convert_alpha()
blackhole_image = pygame.transform.scale(blackhole_image, (TILE, TILE))

asteroid_img = pygame.image.load("asteroid.png").convert_alpha()
asteroid_img = pygame.transform.scale(asteroid_img, (TILE, TILE))

space_bg = pygame.image.load("space.png").convert_alpha()
space_bg = pygame.transform.scale(space_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Helper Functions
def reset_player_position():
    global player_x, player_y, blackhole_pos
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == "A":
                player_x, player_y = x, y
            if maze[y][x] == "B":
                blackhole_pos = (x, y)

reset_player_position()

screen.blit(space_bg, (0, 0))

def draw_maze():
    # Draw walls (asteroids) and Black Hole location.
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            world_x = x * TILE
            world_y = y * TILE

            if cell == "#":
                screen.blit(asteroid_img, (world_x, world_y))
            if cell == "B":
                screen.blit(blackhole_image, (world_x, world_y))




def draw_player():
    screen.blit(player_image, (player_x * TILE, player_y * TILE))


def handle_movement():
    # Move player one tile per frame
    global player_x, player_y
    keys = pygame.key.get_pressed()

    dx, dy = 0, 0

    # Check vertical first
    if keys[pygame.K_UP]:
        dy = -1
    elif keys[pygame.K_DOWN]:
        dy = 1
    # Only check horizontal if no vertical input
    elif keys[pygame.K_LEFT]:
        dx = -1
    elif keys[pygame.K_RIGHT]:
        dx = 1

    # New proposed position
    new_x = player_x + dx
    new_y = player_y + dy

    # Check collisions
    if maze[new_y][new_x] != "#":
        player_x = new_x
        player_y = new_y



def draw_lighting():
    dark = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dark.fill((0, 0, 0, 250))

    px = player_x*TILE + TILE//2
    py = player_y*TILE + TILE//2
    pygame.draw.circle(dark, (0, 0, 0, 0), (px, py), LIGHT_RADIUS)

    bx = blackhole_pos[0]*TILE + TILE//2
    by = blackhole_pos[1]*TILE + TILE//2
    pygame.draw.line(dark, (0, 0, 0, 0), (px, py), (bx, by), 40)

    screen.blit(dark, (0, 0))


def check_win():
    return (player_x, player_y) == blackhole_pos

# Screens (Title, Intro, Game Over)

def title_screen():
    font = pygame.font.SysFont(None, 120)
    small_font = pygame.font.SysFont(None, 50)

    while True:
        screen.fill((0, 0, 0))

        title = font.render("SAVE ALEX", True, (255, 255, 255))
        prompt = small_font.render("Press ENTER to Start", True, (180, 180, 180))

        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 300))
        screen.blit(prompt, (SCREEN_WIDTH//2 - prompt.get_width()//2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

def blackhole_animation():
    # Short animation of Alex being pulled into the black hole
    duration = 40
    px = player_x * TILE + TILE // 2
    py = player_y * TILE + TILE // 2

    bx = blackhole_pos[0] * TILE + TILE // 2
    by = blackhole_pos[1] * TILE + TILE // 2

    for i in range(duration):
        screen.fill((0, 0, 0))
        draw_maze()

        # Interpolate position
        t = i / duration
        ax = px + (bx - px) * t
        ay = py + (by - py) * t

        # Shrink the player
        size = int(TILE * (1 - t))
        if size < 5:
            size = 5

        scaled_player = pygame.transform.scale(player_image, (size, size))
        screen.blit(scaled_player, (ax - size//2, ay - size//2))

        # Black hole stays in place
        screen.blit(blackhole_image, (blackhole_pos[0] * TILE, blackhole_pos[1] * TILE))

        pygame.display.flip()
        pygame.time.delay(25)

    # Flash white
    flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    flash.fill((255, 255, 255))
    screen.blit(flash, (0, 0))
    pygame.display.flip()
    pygame.time.delay(300)


def introduction_scene():
    # Story explanation
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    story_lines = [
        "Alex is lost in a parallel dimension.",
        "",
        "His only escape is a nearby black hole.",
        "",
        "The black hole absorbs almost all light...",
        "but Alex somehow produces a faint glow of his own.",
        "",
        "This small light allows him to see only a tiny area around himself,",
        "and a faint beam that points toward the black hole.",
        "",
        "Use ARROW KEYS to navigate through the asteroid field,",
        "and reach the black hole to escape this dimension.",
        "",
        "Press ENTER to begin."
    ]

    while True:
        screen.fill((0, 0, 0))

        y = 75
        for line in story_lines:
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y))
            y += 50

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


def game_over_screen():
    font = pygame.font.SysFont(None, 100)
    small_font = pygame.font.SysFont(None, 40)

    while True:
        screen.fill((0, 0, 0))

        message = font.render("You Saved Alex!", True, (255, 255, 255))
        restart = small_font.render("Press R to Play Again or Q to Quit", True, (180, 180, 180))

        screen.blit(message, (SCREEN_WIDTH//2 - message.get_width()//2, 300))
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_player_position()
                    return "RESTART"
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()


# Main Game Flow

title_screen()
introduction_scene()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_movement()

    screen.blit(space_bg, (0, 0))
    draw_maze()
    draw_player()
    draw_lighting()

    pygame.display.flip()

    if check_win():
        blackhole_animation()
        result = game_over_screen()
        if result == "RESTART":
            continue
        else:
            running = False

pygame.quit()
sys.exit()
