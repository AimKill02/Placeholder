# guess AI invading past data now
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bullet Hell Bomb Mechanic")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game variables
player_pos = [WIDTH // 2, HEIGHT - 50]
player_speed = 5
bullets = []
bombs = 3
bomb_active = False
bomb_duration = 60  # Duration of bomb effect in frames
bomb_timer = 0

# Functions
def draw_player():
    pygame.draw.rect(screen, BLUE, (*player_pos, 30, 30))

def spawn_bullet(x, y, speed):
    bullets.append({"pos": [x, y], "speed": speed})

def update_bullets():
    for bullet in bullets[:]:
        bullet["pos"][1] += bullet["speed"]
        if bullet["pos"][1] > HEIGHT:
            bullets.remove(bullet)

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, RED, bullet["pos"], 5)

def activate_bomb():
    global bomb_active, bomb_timer, bullets
    if bombs > 0:
        bomb_active = True
        bomb_timer = bomb_duration
        bullets.clear()  # Clear all bullets on the screen

def draw_bomb_effect():
    if bomb_timer > 0:
        radius = (bomb_duration - bomb_timer + 1) * 10
        pygame.draw.circle(screen, WHITE, player_pos, radius, 5)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - 30:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:  # Fire bullets
        spawn_bullet(player_pos[0] + 15, player_pos[1], -5)
    if keys[pygame.K_x] and not bomb_active:  # Activate bomb
        activate_bomb()

    # Bomb logic
    if bomb_active:
        draw_bomb_effect()
        bomb_timer -= 1
        if bomb_timer <= 0:
            bomb_active = False
            bombs -= 1

    # Update bullets
    update_bullets()

    # Draw everything
    draw_player()
    draw_bullets()
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
