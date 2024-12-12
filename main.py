import pygame
import math

# Initialize Pygame
pygame.init()

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

# Placeable Colors (For Now as Sprites is unavaliable)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player Image
player_image = pygame.Surface((50, 50))
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
            bullets.empty()  # Clear all bullets
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
    def draw(self):
        if self.active:
            radius = (self.duration - self.timer + 1) * 10
            pygame.draw.circle(screen, BLUE, self.player.rect.center, radius, 5)

# Player
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
        self.bomb = Bomb(self)  # Bomb mechanic instance
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
        current_time = pygame.time.get_ticks()
        if current_time - self.last_power_change >= POWER_CHANGE_DELAY:
            if keys[pygame.K_i] and self.power <= 4.00:
                self.power += 1.00
                self.last_power_change = current_time
            if keys[pygame.K_o] and self.power >= 0.00:
                self.power -= 1.00
                self.last_power_change = current_time
        self.bomb.update()
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
    def trigger_bomb(self):
        self.bomb.activate()
    def draw_hitbox(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            pygame.draw.circle(screen, WHITE, self.rect.center, 15)

# Setup sprites and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
bullets = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and player.can_shoot():
        if keys[pygame.K_LSHIFT]:  # Focused Shot
            player.shoot_focus()
        else:  # Spread Shot
            spread_angles = [270]
            if player.power >= 1.00:
                spread_angles += [260, 280]
            if player.power >= 2.00:
                spread_angles += [255, 285]
            if player.power >= 3.00:
                spread_angles += [240, 300]
            if player.power >= 4.00:
                spread_angles += [250, 290]
            for angle in spread_angles:
                player.shoot(angle=angle)

    if keys[pygame.K_z]:  # Trigger the bomb
        player.trigger_bomb()
    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)
    player.bomb.draw()
    player.draw_hitbox()
    # Refresh the display
    pygame.display.flip()
    # Maintain framerate
    clock.tick(FPS)
# Quit pygame
pygame.quit()