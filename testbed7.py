import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

# Dummy Target class
class DummyTarget(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pattern_type):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.shoot_timer = 0
        self.pattern_angle = 0
        self.movement_timer = 0
        self.pattern_type = pattern_type

    def update(self):
        # Move based on pattern type
        self.movement_timer += 1
        if self.pattern_type == 1:
            self.rect.x += math.sin(pygame.time.get_ticks() / 500) * 5
        elif self.pattern_type == 2:
            self.rect.y += math.cos(pygame.time.get_ticks() / 300) * 3
        elif self.pattern_type == 3:
            self.rect.x += math.sin(self.movement_timer / 30) * 4
            self.rect.y += math.cos(self.movement_timer / 30) * 4

        # Shoot bullets periodically
        self.shoot_timer += 1
        if self.shoot_timer > 30:
            if self.pattern_type == 1:
                self.shoot_aimed_bullets()
            elif self.pattern_type == 2:
                self.shoot_spiral_pattern()
            elif self.pattern_type == 3:
                self.shoot_radial_burst()
            self.shoot_timer = 0

    def shoot_aimed_bullets(self):
        # Aim bullets at the target
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        dx /= distance
        dy /= distance
        bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def shoot_spiral_pattern(self):
        for i in range(0, 360, 45):
            angle_rad = math.radians(i + self.pattern_angle)
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            bullets.add(bullet)
        self.pattern_angle += 10

    def shoot_radial_burst(self):
        for i in range(0, 360, 30):
            angle_rad = math.radians(i)
            dx = math.cos(angle_rad) * 2
            dy = math.sin(angle_rad) * 2
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx * 5
        self.dy = dy * 5

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create a dummy target
target = DummyTarget(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
all_sprites.add(target)

# Wave manager
wave_timer = 0
current_wave = 0

def spawn_wave(wave):
    if wave == 1:
        for i in range(3):
            enemy = Enemy(200 + i * 150, 100, 1)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 2:
        for i in range(4):
            enemy = Enemy(150 + i * 150, 50, 2)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 3:
        for i in range(5):
            enemy = Enemy(100 + i * 100, 150, 3)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 4:
        for i in range(3):
            enemy = Enemy(200 + i * 150, 100, random.choice([1, 2, 3]))
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 5:
        for i in range(6):
            enemy = Enemy(50 + i * 120, 50, 1)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 6:
        for i in range(4):
            enemy = Enemy(100 + i * 150, 200, 2)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 7:
        for i in range(3):
            enemy = Enemy(200 + i * 150, 100, 3)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 8:
        for i in range(5):
            enemy = Enemy(100 + i * 100, 100, random.choice([1, 2, 3]))
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 9:
        for i in range(6):
            enemy = Enemy(50 + i * 120, 50, random.choice([1, 2]))
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 10:
        for i in range(7):
            enemy = Enemy(50 + i * 100, 50, random.choice([1, 2, 3]))
            all_sprites.add(enemy)
            enemies.add(enemy)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update wave logic
    if len(enemies) == 0:
        wave_timer += 1
        if wave_timer > 120:  # Wait 2 seconds between waves
            current_wave += 1
            if current_wave <= 10:
                spawn_wave(current_wave)
            wave_timer = 0

    # Update
    all_sprites.update()

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
