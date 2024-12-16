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
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.shoot_timer = 0
        self.pattern_angle = 0  # Angle for complex bullet patterns

    def update(self):
        # Move the enemy in a sinusoidal pattern
        self.rect.x += math.sin(pygame.time.get_ticks() / 500) * 5

        # Shoot bullets periodically
        self.shoot_timer += 1
        if self.shoot_timer > 30:  # Shoot every 30 frames
            self.shoot_bullet_pattern()
            self.shoot_timer = 0

    def shoot_bullet_pattern(self):
        # Create a spiraling bullet pattern
        for i in range(0, 360, 45):
            angle_rad = math.radians(i + self.pattern_angle)
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Create a radial burst of bullets
        for i in range(0, 360, 30):
            angle_rad = math.radians(i - self.pattern_angle)
            dx = math.cos(angle_rad) * 2  # Faster bullets
            dy = math.sin(angle_rad) * 2
            bullet = Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            bullets.add(bullet)

        # Increment pattern angle for dynamic patterns
        self.pattern_angle += 10

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx * 5  # Bullet speed
        self.dy = dy * 5

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Remove bullet if it goes off-screen
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

# Create an enemy
enemy = Enemy(SCREEN_WIDTH // 2, 100)
all_sprites.add(enemy)
enemies.add(enemy)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw
    screen.fill((0, 0, 0))  # Clear the screen
    all_sprites.draw(screen)

    # Refresh the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
