import pygame
import random

# Initialize Pygame
pygame.init()

# Screen Setup
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cricket Shot Game with Lives")

# Colors
green = (50, 205, 50)
white = (255, 255, 255)
red = (255, 50, 50)
yellow = (255, 255, 0)
black = (0, 0, 0)
blue = (30, 144, 255)
sky_blue = (135, 206, 250)
orange = (255, 165, 0)
purple = (186, 85, 211)
gold = (255, 215, 0)

# Fonts
font = pygame.font.SysFont("comicsansms", 30)
big_font = pygame.font.SysFont("comicsansms", 50)

# Game Variables
ball_y = 0
ball_speed = 4
ball_radius = 20
ball_x = width // 2
score = 0
last_runs = 0
game_active = True
lives = 3

hit_zone = (420, 460)
run_display_timer = 0
animation_text = ""
hit_effect_timer = 0
hit_flash_color = orange

clock = pygame.time.Clock()

def draw_background():
    # Sky
    screen.fill(sky_blue)

    # Grass
    pygame.draw.rect(screen, green, (0, 300, width, 200))

    # Pitch
    pygame.draw.rect(screen, (222, 184, 135), (150, 100, 200, 300))

    # Decorative circles
    for i in range(3):
        pygame.draw.circle(screen, yellow, (50 + i * 30, 70), 10)
        pygame.draw.circle(screen, purple, (width - 50 - i * 30, 70), 10)

def draw_game():
    draw_background()

    # Stumps
    for i in range(3):
        pygame.draw.rect(screen, white, (ball_x - 15 + i * 10, 450, 4, 30))

    # Bat
    pygame.draw.rect(screen, yellow, (ball_x - 40, 470, 80, 10))

    # Ball
    if hit_effect_timer > 0:
        pygame.draw.circle(screen, white, (ball_x, int(ball_y)), ball_radius + 5)
    pygame.draw.circle(screen, red, (ball_x, int(ball_y)), ball_radius)

    # Score & Lives
    screen.blit(font.render(f"Score: {score}", True, black), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, red), (10, 45))

    # Hit text (like SIX / FOUR)
    if run_display_timer > 0:
        color = gold if animation_text == "SIX!" else blue
        screen.blit(big_font.render(animation_text, True, color), (200, 200))

def show_game_over():
    screen.blit(big_font.render("Game Over!", True, red), (130, 200))
    screen.blit(font.render("Press R to Restart", True, white), (130, 260))

# Game loop
running = True
while running:
    screen.fill(green)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_active:
        ball_y += ball_speed
        draw_game()

        if run_display_timer > 0:
            run_display_timer -= 1

        if hit_effect_timer > 0:
            hit_effect_timer -= 1

        if keys[pygame.K_SPACE]:
            if hit_zone[0] <= ball_y <= hit_zone[1]:
                if abs(ball_y - (hit_zone[0] + hit_zone[1]) // 2) < 10:
                    last_runs = 6
                    animation_text = "SIX!"
                    hit_flash_color = gold
                elif hit_zone[0] <= ball_y <= hit_zone[1]:
                    last_runs = 4
                    animation_text = "FOUR!"
                    hit_flash_color = blue
                else:
                    last_runs = random.choice([1, 2])
                    animation_text = f"{last_runs} RUNS"
                    hit_flash_color = black

                score += last_runs
                ball_y = 0
                run_display_timer = 30
                hit_effect_timer = 10

        if ball_y > height:
            lives -= 1
            ball_y = 0
            if lives <= 0:
                game_active = False

    else:
        show_game_over()
        if keys[pygame.K_r]:
            score = 0
            last_runs = 0
            ball_y = 0
            lives = 3
            run_display_timer = 0
            hit_effect_timer = 0
            game_active = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
