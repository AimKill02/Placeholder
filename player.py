import pygame
import math

# Field dimensions
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game settings (Uneditable in-game)
FPS = 60
PLAYER_SPEED_SPREAD = 5
PLAYER_SPEED_FOCUS = 2
BULLET_SPEED = 15
POWER_POINT = 0.00
SHOOT_DELAY = 50
POWER_CHANGE_DELAY = 200
player_pos = [WIDTH // 2, HEIGHT - 50]
bombs = 3
bomb_active = False
bomb_duration = 60  # Duration of bomb effect in frames
bomb_timer = 0

# Placeable Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


player_image = pygame.Surface((25, 25))
player_image.fill(GREEN)

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, speed):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed

    def update(self):
        # Move bullet in the direction of the angle
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed

        # Remove bullet if it goes off-screen
        if not screen.get_rect().colliderect(self.rect):
            self.kill()

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
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed_spread = PLAYER_SPEED_SPREAD
        self.speed_focus = PLAYER_SPEED_FOCUS
        self.last_shot_time = 0
        self.power = POWER_POINT
        self.last_power_change = 0
        self.bomb = None  # Reference to the current bomb

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # Prioritize Micro-Management & DPS
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_focus
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed_focus
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_focus
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_focus
        else:  # Prioritize Movement Speed & Area Coverage
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_spread
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed_spread
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_spread
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_spread

        # Handle power changes 
        # FIXME: Please add an item point that increase power
        # FIXME: Please Remove controllable power change via buttons upon Alternate power gathering is made
        current_time = pygame.time.get_ticks()
        if current_time - self.last_power_change >= POWER_CHANGE_DELAY:
            if keys[pygame.K_i] and self.power <= 4.00:
                self.power += 1.00
                self.last_power_change = current_time
            if keys[pygame.K_o] and self.power >= 0.00:
                self.power -= 1.00
                self.last_power_change = current_time

        # Handle bomb
        if keys[pygame.K_z]:  # Trigger the bomb
            player.trigger_bomb()

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= SHOOT_DELAY

    def shoot(self, angle=270):
        bullet = Bullet(self.rect.centerx, self.rect.centery, math.radians(angle), BULLET_SPEED)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.last_shot_time = pygame.time.get_ticks()

    def shoot_focus(self):
        cluster_size = 1 + int(self.power)  # Cluster grows with power level
        spacing = 20  # Spacing gets tighter with power

        for i in range(-(cluster_size // 2), (cluster_size // 2) + 1):
            offset_x = i * spacing
            bullet = Bullet(self.rect.centerx + offset_x, self.rect.centery, math.radians(270), BULLET_SPEED)
            all_sprites.add(bullet)
            bullets.add(bullet)

        self.last_shot_time = pygame.time.get_ticks()

# Setup sprites and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()
