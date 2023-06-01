import pygame
import random
import math
import json

# Constants
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

# Colors
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
clock = pygame.time.Clock()
dt = 0

# Initialize shurikens and hamburgers
hamburgers = []
shurikens = []

# Classes
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(playerImg, (playerImg.get_width() // 1.5, playerImg.get_height() // 1.5))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.position = pygame.Vector2(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
        self.rect.center = self.position
        self.speed = 300

    def reset_position(self):
        self.rect.center = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= player.speed * dt
            self.angle = 0
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += player.speed * dt
            self.angle = 180
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= player.speed * dt
            self.angle = 90
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += player.speed * dt
            self.angle = 270

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.angle = 45
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.angle = 135
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            self.angle = 225
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.angle = 315

        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            self.speed = 600
        else:
            self.speed = 300

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > DISPLAY_WIDTH:
            self.rect.right = DISPLAY_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > DISPLAY_HEIGHT:
            self.rect.bottom = DISPLAY_HEIGHT

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)


class Hamburger:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(burger, (burger.get_width() // 30, burger.get_height() // 30))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self):
        screen.blit(self.image, self.rect)


class Shuriken:
    num = 3
    def __init__(self, x, y, target_x, target_y):
        self.image = pygame.transform.scale(shurikenImg, (shurikenImg.get_width() // 7, shurikenImg.get_height() // 7))
        self.rect = self.image.get_rect(center=(x, y))
        self.position = pygame.Vector2(x, y)
        self.target = pygame.Vector2(target_x, target_y)
        self.speed = 200
        self.angle = 0

    def update(self):
        direction = self.target - self.position
        distance = direction.length()
        self.angle = (self.angle + 360 * dt) % 360  # Update angle to rotate 360 degrees per second

        if random.random() < 0.0003:
            Shuriken.num += 1

        if distance > 5:
            direction.normalize_ip()
            move_amount = direction * self.speed * dt

            if move_amount.length_squared() > distance ** 2:
                self.position = self.target
            else:
                self.position += move_amount

        else:
            # Pick new random coordinates for the target
            self.target = pygame.Vector2(random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT))

        self.rect.center = self.position

    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

class GameOverScreen:
    def __init__(self, score, high_score):
        self.score = score
        self.high_score = high_score
        self.restart_button_rect = pygame.Rect(
            DISPLAY_WIDTH // 2 - 100,
            DISPLAY_HEIGHT // 2 + 50,
            200,
            50,
        )

    def draw(self):
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_text_width = game_over_text.get_width()
        game_over_text_height = game_over_text.get_height()
        game_over_text_position = (
            DISPLAY_WIDTH // 2 - game_over_text_width // 2,
            DISPLAY_HEIGHT // 2 - game_over_text_height // 2 - 25,
        )
        screen.blit(game_over_text, game_over_text_position)

        pygame.draw.rect(screen, (0, 0, 0), self.restart_button_rect)
        restart_text = font.render("Restart", True, (255, 255, 255))
        restart_text_width = restart_text.get_width()
        restart_text_height = restart_text.get_height()
        restart_text_x = self.restart_button_rect.x + (self.restart_button_rect.width - restart_text_width) // 2
        restart_text_y = self.restart_button_rect.y + (self.restart_button_rect.height - restart_text_height) // 2
        screen.blit(restart_text, (restart_text_x, restart_text_y))

    def handle_click(self):
        global game_over, score, high_score, player, hamburgers, shurikens
        if self.restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            score = 0
            high_score = max(score, self.high_score)
            player.reset_position()
            hamburgers = []
            shurikens = []
            Shuriken.num = 3
            game_over = False

# Load images
playerImg = pygame.image.load("assets/car.png").convert_alpha()
burger = pygame.image.load("assets/burger.png").convert_alpha()
shurikenImg = pygame.image.load("assets/skuriken.png").convert_alpha()

# Load fonts
font = pygame.font.Font(None, 36)

# Game variables
player = Player(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2)
score = 0
high_score = 0
running = True
game_over = False

# Load high score from file
try:
    with open("high_score.json", "r") as file:
        high_score = json.load(file)
        high_score = int(high_score)  # Convert high_score to an integer
except (FileNotFoundError, json.JSONDecodeError):
    pass

game_over_screen = GameOverScreen(score, high_score)

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            game_over_screen.handle_click()

    player.update()

    
    if not game_over:

        # Update hamburgers
        hamburgers = [hamburger for hamburger in hamburgers if hamburger.rect.colliderect(screen.get_rect())]

        # Check collision between player and hamburgers
        for hamburger in hamburgers:
            if hamburger.rect.colliderect(player.rect):
                hamburgers.remove(hamburger)
                score += 1
                if score > high_score:
                    high_score = score

        # Spawn hamburgers
        if random.random() < 0.03 and len(hamburgers) < 25:
            x = random.randint(0, DISPLAY_WIDTH)
            y = random.randint(0, DISPLAY_HEIGHT)
            hamburgers.append(Hamburger(x, y))

        # Update shurikens
        for shuriken in shurikens:
            shuriken.update()
            if shuriken.rect.colliderect(player.rect):
                # Game over condition
                game_over = True

        # Spawn shurikens
        if len(shurikens) < Shuriken.num:
            x = random.randint(0, DISPLAY_WIDTH)
            y = random.randint(0, DISPLAY_HEIGHT)
            if math.hypot(x - player.rect.centerx, y - player.rect.centery) > 250:
                shurikens.append(Shuriken(x, y, random.randint(0, DISPLAY_WIDTH), random.randint(0, DISPLAY_HEIGHT)))

        # Draw background
        screen.fill(PURPLE)

        # Draw player, hamburgers, and shurikens
        player.draw()
        for hamburger in hamburgers:
            hamburger.draw()
        for shuriken in shurikens:
            shuriken.draw()

        #  Draw score
        score_text = "Score: " + str(score)
        score_surface = pygame.font.Font(None, 36).render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(topleft=(20, 20))
        screen.blit(score_surface, score_rect)

    elif game_over:
        game_over_screen.draw()

    pygame.display.flip()

# Save high score to file
with open("high_score.json", "w") as file:
    json.dump(high_score, file)
