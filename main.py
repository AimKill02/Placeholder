import pygame
import math


# Initialize Pygame
pygame.init()

# field dimensions
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game settings (Uneditable in game)
FPS = 60
PLAYER_SPEED_SPREAD = 5
PLAYER_SPEED_FOCUS = 2
BULLET_SPEED = 15
POWER_POINT = 0.00
SHOOT_DELAY = 50
POWER_CHANGE_DELAY = 200 

# Placeable Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player Image
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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]: # Prioritize Micro-Management & DPS
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_focus
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed_focus
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_focus
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_focus
        else: # Prioritize Movement Speed & Area Coverage
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed_spread
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed_spread
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed_spread
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_spread
  # Add to Player class
 # milliseconds

# Update method in Player
        current_time = pygame.time.get_ticks()
        if current_time - self.last_power_change >= POWER_CHANGE_DELAY:
            if keys[pygame.K_i] and self.power < 4.00:
                self.power += 1.00
                self.last_power_change = current_time
            if keys[pygame.K_o] and self.power > 0.00:
                self.power -= 1.00
                self.last_power_change = current_time

            
    def can_shoot(self):
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_shot_time >= SHOOT_DELAY:  # Check if enough time has passed since last shot
            return True
        return False

    def shoot(self,angle=270):
        bullet = Bullet(self.rect.centerx, self.rect.centery, math.radians(angle), BULLET_SPEED)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.last_shot_time = pygame.time.get_ticks()
        
    def shoot_focus(self):
        cluster_size = 3 + int(self.power)  # Cluster grows with power level
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



    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

    # Maintain framerate
    clock.tick(FPS)

# Quit pygame
running = False
pygame.quit()