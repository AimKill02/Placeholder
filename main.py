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
BLACK = (0, 0, 0)

# Initialize Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Hell Game")
clock = pygame.time.Clock()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = dx * 25
        self.dy = dy * 25

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
            
class Enemy_Bullet(pygame.sprite.Sprite):
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

# Power Drop class (new class for power collection)
class PowerDrop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move downwards to simulate falling
        self.rect.y += 2
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Bomb mechanic
class Bomb:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.timer = 0
        self.duration = 60  # Frames

    def activate(self):
        if not self.active and self.player.power >= 1.00:  # Ensure bomb is available
            self.active = True
            self.timer = self.duration
            self.player.power -= 1.00  # Deduct power for using the bomb
            enemy_bullets.empty()  # Clear all bullets
            for enemy in enemies:
                enemy.take_damage(enemy.health)  # Instantly destroy all enemies

    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False

    def draw(self):
        if self.active:
            radius = (self.duration - self.timer + 1) * 10
            pygame.draw.circle(screen, BLUE, self.player.rect.center, radius, 5)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed_spread = 5
        self.speed_focus = 7
        self.last_shot_time = 0
        self.power = 0.00
        self.last_power_change = 0
        self.bomb = Bomb(self)  # Bomb mechanic instance

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:  # Focus mode
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_focus
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed_focus
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_focus
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed_focus
        else:  # Spread mode
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_spread
            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.x += self.speed_spread
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_spread
            if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += self.speed_spread

        # Handle power changes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_power_change >= 200:
            if keys[pygame.K_i] and self.power <= 4.00:
                self.power += 1.00
                self.last_power_change = current_time
            if keys[pygame.K_o] and self.power >= 0.00:
                self.power -= 1.00
                self.last_power_change = current_time

        self.bomb.update()

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= 50

    def shoot(self, angle=270):
        bullet = Bullet(self.rect.centerx, self.rect.centery, math.cos(math.radians(angle)), math.sin(math.radians(angle)))
        all_sprites.add(bullet)
        player_bullets.add(bullet)
        self.last_shot_time = pygame.time.get_ticks()

    def shoot_focus(self):
        cluster_size = 1 + int(self.power)  # Cluster grows with power level
        spacing = 20  # Spacing gets tighter with power
        for i in range(-(cluster_size // 2), (cluster_size // 2) + 1):
            offset_x = i * spacing
            bullet = Bullet(self.rect.centerx + offset_x, self.rect.centery, 0, -1)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
        self.last_shot_time = pygame.time.get_ticks()

    def trigger_bomb(self):
        self.bomb.activate()

    def draw_hitbox(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            pygame.draw.circle(screen, RED, self.rect.center, 15)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, pattern_type):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.health = 10  # Enemy health
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
        # Aim bullets at the player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        dx /= distance
        dy /= distance
        bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, dx, dy)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

    def shoot_spiral_pattern(self):
        for i in range(0, 360, 45):
            angle_rad = math.radians(i + self.pattern_angle)
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)
        self.pattern_angle += 10

    def shoot_radial_burst(self):
        for i in range(0, 360, 30):
            angle_rad = math.radians(i)
            dx = math.cos(angle_rad) * 2
            dy = math.sin(angle_rad) * 2
            bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, dx, dy)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            # Drop power when enemy is destroyed
            power_drop = PowerDrop(self.rect.centerx, self.rect.centery)
            all_sprites.add(power_drop)
            power_drops.add(power_drop)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
power_drops = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

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
        for i in range(5):
            enemy = Enemy(100 + i * 120, 150, 2)
            all_sprites.add(enemy)
            enemies.add(enemy)
    elif wave == 3:
        for i in range(4):
            enemy = Enemy(150 + i * 100, 100, 3)
            all_sprites.add(enemy)
            enemies.add(enemy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls for shooting and bomb
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and player.can_shoot():
        if keys[pygame.K_LSHIFT]:  # Focused Shot
            player.shoot_focus()
        else:  # Spread Shot
            player.shoot()

    if keys[pygame.K_z]:  # Trigger the bomb
        player.trigger_bomb()

    # Update all sprites
    all_sprites.update()

    # Check collisions
    for bullet in player_bullets:
        collided_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in collided_enemies:
            enemy.take_damage(1)
            bullet.kill()

    # Check power collection
    for power_drop in power_drops:
        if pygame.sprite.collide_rect(player, power_drop):
            player.power += 1.00
            power_drop.kill()

    # Spawn waves
    if not enemies:  # If no enemies are left
        wave_timer += 1
        if wave_timer > 60:  # Small delay between waves
            current_wave += 1
            spawn_wave(current_wave)
            wave_timer = 0

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    player.bomb.draw()
    player.draw_hitbox()
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
