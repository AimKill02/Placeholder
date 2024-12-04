import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basic Bullet Hell Game')

# Game settings
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 15
ENEMY_SPEED = 2
ENEMY_BULLET_SPEED = 5
SHOOT_DELAY = 50  # Delay between shots in milliseconds (300ms = 0.3 seconds)
BOMB_DELAY = 5000  # Bomb cooldown in milliseconds (5 seconds)
BOMB_EFFECT_TIME = 1000  # Bomb effect time in milliseconds (1 second)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Load player image (or use a rectangle for simplicity)
player_image = pygame.Surface((25, 25))
player_image.fill(GREEN)

# Fonts
font = pygame.font.Font(None, 36)

# Bullet class
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

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), random.randint(-100, -40)))
        self.speed = ENEMY_SPEED

    def update(self):
        # Move the enemy downward
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH)
            self.rect.y = random.randint(-100, -40)
        
        # Enemy shooting bullets at the player
        if random.randint(0, 60) == 0:  # Random chance to shoot
            angle = math.atan2(HEIGHT - self.rect.centery, WIDTH // 2 - self.rect.centerx)
            enemy_bullet = Bullet(self.rect.centerx, self.rect.centery, angle, ENEMY_BULLET_SPEED)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.speed = PLAYER_SPEED
        self.last_shot_time = 0  # Timestamp of last shot
        self.last_bomb_time = 0  # Timestamp of last bomb use
        self.bomb_active = False  # Flag to track bomb effect

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= (self.speed - 2)
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += (self.speed - 2)
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= (self.speed - 2)
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += (self.speed - 2)
        else:
            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
                self.rect.y += self.speed

    def can_shoot(self):
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_shot_time >= SHOOT_DELAY:  # Check if enough time has passed since last shot
            return True
        return False

    def shoot(self,angle=270):
        bullet = Bullet(self.rect.centerx, self.rect.centery, math.radians(angle), BULLET_SPEED)
        all_sprites.add(bullet)
        bullets.add(bullet)
        self.last_shot_time = pygame.time.get_ticks()  # Update last shot time

    def can_use_bomb(self):
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if current_time - self.last_bomb_time >= BOMB_DELAY:  # Check if enough time has passed since last bomb use
            return True
        return False

    def use_bomb(self):
        # Clear all enemies and enemy bullets
        enemies.empty()
        enemy_bullets.empty()

        self.last_bomb_time = pygame.time.get_ticks()  # Update last bomb time
        self.bomb_active = True  # Activate bomb effect

# Setup sprites and groups
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create some enemies
for _ in range(5):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

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

    # Continuous shooting when left ctrl is held with delay between shots
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL] and player.can_shoot():  # Check if left ctrl is held and player can shoot
        if keys[pygame.K_LSHIFT]:
            player.shoot()
        else:
            player.shoot()
            player.shoot(angle=240)
            player.shoot(angle=300)
            player.shoot(angle=240)
            player.shoot(angle=300)# Call shoot method to fire a bullet

    # Use bomb when "Z" is pressed and bomb cooldown has passed
    if keys[pygame.K_z] and player.can_use_bomb():  # Check if "Z" is pressed and bomb cooldown is ready
        player.use_bomb()  # Activate bomb

    # If the bomb is active, we can display a message or perform additional effects
    if player.bomb_active:
        # You can display a temporary bomb effect here (e.g., a short screen flash or message)
        if pygame.time.get_ticks() - player.last_bomb_time <= BOMB_EFFECT_TIME:
            # Bomb effect is active (you can add a visual effect here if desired)
            pass
        else:
            player.bomb_active = False  # End bomb effect after BOMB_EFFECT_TIME

    # Check for collisions between player bullets and enemies
    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        for enemy in hit_enemies:
            bullet.kill()  # Remove bullet on collision
            # Create new enemy when an enemy is hit
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Check for collisions between enemy bullets and player
    if pygame.sprite.spritecollide(player, enemy_bullets, True) or pygame.sprite.spritecollide(player, enemies, False):
        running = False  # End game if player is hit

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Refresh the display
    pygame.display.flip()

    # Maintain framerate
    clock.tick(FPS)

# Quit pygame
pygame.quit()