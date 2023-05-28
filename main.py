import pygame
import random
import math
import json

# pygame setup
pygame.init()
display_width = 1280
display_height = 720

screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
dt = 0
speed = 300
running = True
game_over = False

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_angle = 0

def player(x, y, angle=0):
    rotated_image = pygame.transform.rotate(playerImg, angle)
    new_rect = rotated_image.get_rect(center=playerImg.get_rect(center=(x, y)).center)
    screen.blit(rotated_image, new_rect.topleft)

def burgers():
    x_burger = random.randrange(50, display_width - 50)
    y_burger = random.randrange(50, display_height - 50)
    return pygame.Rect(x_burger, y_burger, burger.get_width(), burger.get_height())

def shuriken(x, y, angle):
    rotated_image = pygame.transform.rotate(shurikenImg, angle)
    screen.blit(rotated_image, (x, y))

def generate_random_coordinates():
    x = random.randint(30, display_width - 30)
    y = random.randint(30, display_height - 30)
    while abs(x - display_width / 2) < 250 and abs(y - display_height / 2) < 250:
        x = random.randint(30, display_width - 30)
        y = random.randint(30, display_height - 30)
    return pygame.Vector2(x, y)


def is_collision(rect1, x2, y2, width2, height2):
    rect2 = pygame.Rect(x2, y2, width2, height2)
    return rect1.colliderect(rect2)

class Shuriken:
    def __init__(self):
        self.position = generate_random_coordinates()
        self.target = generate_random_coordinates()
        self.angle = 0
        self.speed = 300  # Adjust the speed of shurikens

    def update(self):
        angle_to_target = math.atan2(self.target.y - self.position.y, self.target.x - self.position.x)
        self.angle += 360 * dt  # Rotate shuriken by 360 deg/s

        distance_to_target = self.target.distance_to(self.position)
        if distance_to_target > 1:
            movement_vector = pygame.Vector2(math.cos(angle_to_target), math.sin(angle_to_target)) * self.speed * dt
            if movement_vector.length() < distance_to_target:
                self.position += movement_vector
            else:
                self.position = self.target
        else:
            self.target = generate_random_coordinates()


# assets
playerImg = pygame.image.load('assets/car.png').convert_alpha()
burger = pygame.image.load('assets/burger.png').convert_alpha()
shurikenImg = pygame.image.load('assets/skuriken.png').convert_alpha()

# Rescale images
burger = pygame.transform.scale(burger, (burger.get_width() // 30, burger.get_height() // 30))
playerImg = pygame.transform.scale(playerImg, (playerImg.get_width() // 1.5, playerImg.get_height() // 1.5))
shurikenImg = pygame.transform.scale(shurikenImg, (shurikenImg.get_width() // 8, shurikenImg.get_height() // 8))

# Hamburgers
hamburgers = []

# Shurikens
shurikens = []
for _ in range(3):
    new_shuriken = Shuriken()
    shurikens.append(new_shuriken)

# Initialize player rectangle
player_rect = pygame.Rect(player_pos.x - 15, player_pos.y - 15, 50, 50)

# Game over text
font = pygame.font.Font(None, 70)
new_record_font = pygame.font.Font(None, 80)
game_over_text = font.render("Game Over", True, (255, 0, 0))

# Restart button
restart_button = pygame.Rect(display_width // 2 - 100, display_height // 2 + 50, 200, 50)
restart_text = font.render("Restart", True, (255, 255, 255))

# Score
score = 1
score_text = font.render("Score: " + str(score), True, (255, 255, 255))

def save_high_score(score):
    try:
        with open("high_score.json", "r") as file:
            high_score_data = json.load(file)
            high_score = high_score_data.get("high_score", 0)
            if score > high_score:
                high_score_data["high_score"] = score
                with open("high_score.json", "w") as file:
                    json.dump(high_score_data, file)
    except FileNotFoundError:
        high_score_data = {"high_score": score}
        with open("high_score.json", "w") as file:
            json.dump(high_score_data, file)

# Load the high score from the JSON file
try:
    with open("high_score.json", "r") as file:
        high_score_data = json.load(file)
        high_score = high_score_data.get("high_score", 0)
except FileNotFoundError:
    high_score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and restart_button.collidepoint(pygame.mouse.get_pos()):
                # Restart the game
                game_over = False
                player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                player_rect.x = player_pos.x - 15
                player_rect.y = player_pos.y - 15
                hamburgers = []
                shurikens = []
                for _ in range(3):
                    new_shuriken = Shuriken()
                    shurikens.append(new_shuriken)
                score = 0

    if not game_over:
        screen.fill("purple")
        

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_pos.y - 27 > 0:
            player_pos.y -= speed * dt
            player_angle = 0
        if (keys[pygame.K_s]or keys[pygame.K_DOWN]) and player_pos.y + 27 < display_height:
            player_pos.y += speed * dt
            player_angle = 180
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_pos.x - 27 > 0:
            player_pos.x -= speed * dt
            player_angle = 90
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_pos.x + 27 < display_width:
            player_pos.x += speed * dt
            player_angle = 270

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            player_angle = 45
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            player_angle = 135
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            player_angle = 225
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            player_angle = 315

        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            speed = 600
        else:
            speed = 300

        # Update player rectangle for collision detection
        player_rect.x = player_pos.x - 25
        player_rect.y = player_pos.y - 25

        # Update shurikens' positions and rotation
        for shuriken_obj in shurikens:
            shuriken_obj.update()
            shuriken(shuriken_obj.position.x, shuriken_obj.position.y, shuriken_obj.angle % 360)  # Rotate shurikens

            # Expand shuriken hitbox
            shuriken_hitbox = pygame.Rect(shuriken_obj.position.x, shuriken_obj.position.y, 50, 50)

            # Check for collision with player
            if player_rect.colliderect(shuriken_hitbox):
                game_over = True

        # Spawn hamburgers
        while len(hamburgers) < 10:
            new_burger = burgers()
            hamburgers.append(new_burger)

        # Check for collision between player and hamburgers
        for hamburger in hamburgers:
            screen.blit(burger, hamburger)
            if is_collision(player_rect, hamburger.x, hamburger.y, 40, 40):
                hamburgers.remove(hamburger)
                score += 1

       
        player(player_pos.x, player_pos.y, player_angle)
        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        if not game_over:
            screen.blit(score_text, (10, 10))
    

    elif game_over:
        game_over_text_width = game_over_text.get_width()
        game_over_text_height = game_over_text.get_height()
        game_over_text_position = (display_width // 2 - game_over_text_width // 2, display_height // 2 - game_over_text_height // 2 - 25)
        screen.blit(game_over_text, game_over_text_position)
         # Restart button
        restart_button = pygame.Rect(display_width // 2 - 100, display_height // 2 + 50, 200, 50)
        restart_text = font.render("Restart", True, (255, 255, 255))
        restart_text_width = restart_text.get_width()
        restart_text_height = restart_text.get_height()
        restart_text_x = restart_button.x + (restart_button.width - restart_text_width) // 2
        restart_text_y = restart_button.y + (restart_button.height - restart_text_height) // 2
        pygame.draw.rect(screen, (0, 0, 0), restart_button)
        screen.blit(restart_text, (restart_text_x, restart_text_y))
        if score > high_score:
             new_record_text = new_record_font.render("NEW RECORD: " + str(score), True, (255, 255, 0))
             new_record_text_width = new_record_text.get_width()
             new_record_text_x = display_width // 2 - new_record_text_width // 2
             screen.blit(new_record_text, (new_record_text_x, display_height // 2))
             save_high_score(score)
        else:
            score_width = score_width = score_text.get_width()
            screen.blit(score_text, (display_width // 2 - score_width // 2, display_height // 2))
            
    dt = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()
