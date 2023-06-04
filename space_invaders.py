import pygame
import random
import subprocess

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

background_image = pygame.image.load("images/space.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
player_image = pygame.image.load("images/spaceship.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (64, 64))
bullet_image = pygame.image.load("images/bullet.png").convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (32, 32))
enemy_image = pygame.image.load("images/invader.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (64, 64))
circle_image = pygame.image.load("images/circle.png").convert_alpha()
circle_image = pygame.transform.scale(circle_image, (32, 32))

w = 5

global score
score = 0

def game(wave):
    global score
    global bullet_state
    player_width = 64
    player_height = 64
    player_x = (screen_width - player_width) // 2
    player_y = screen_height - player_height - 10
    player_speed = 5

    bullet_width = 32
    bullet_height = 32
    bullet_x = 0
    bullet_y = screen_height - player_height - 10
    bullet_speed = 10
    bullet_state = "ready"

    enemy_width = 64
    enemy_height = 64
    enemy_speed = 2

    enemies = []
    enemy_rows = 5
    enemy_cols = 8
    enemy_start_x = 100
    enemy_start_y = 50
    enemy_x_gap = 80
    enemy_y_gap = 70

    for row in range(enemy_rows):
        for col in range(enemy_cols):
            enemy_x = enemy_start_x + enemy_x_gap * col
            enemy_y = enemy_start_y + enemy_y_gap * row
            enemies.append({"x": enemy_x, "y": enemy_y, "speed": enemy_speed, "bullet_state": "ready"})

    circles = []
    circle_speed = 3

    score_font = pygame.font.Font(None, 36)

    running = True
    clock = pygame.time.Clock()

    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bullet_image, (x, y))

    def draw_score():
        score_text = score_font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    right = False
    left = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                subprocess.Popen("python end_screen.py")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_x > 0:
                    left = True
                if event.key == pygame.K_RIGHT and player_x < screen_width - player_width:
                    right = True
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    fire_bullet(bullet_x, bullet_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:
                    right = False

        if right and player_x < screen_width - player_width:
            player_x += player_speed
        if left and player_x > 0:
            player_x -= player_speed

        screen.blit(background_image, (0, 0))

        if bullet_state == "fire":
            bullet_y -= bullet_speed
            if bullet_y < 0:
                bullet_state = "ready"

        for enemy in enemies:
            enemy_x = enemy["x"]
            enemy_y = enemy["y"]

            enemy_x += enemy["speed"]
            if enemy_x <= 0 or enemy_x >= screen_width - enemy_width:
                for e in enemies:
                    e["speed"] *= -1
                    e["y"] += wave
                enemy_y += wave

            enemy["x"] = enemy_x
            enemy["y"] = enemy_y

            if (
                bullet_x < enemy_x + enemy_width
                and bullet_x + bullet_width > enemy_x
                and bullet_y < enemy_y + enemy_height
                and bullet_y + bullet_height > enemy_y
            ):
                bullet_state = "ready"
                enemies.remove(enemy)
                score += 1

            if (
                player_x < enemy_x + enemy_width
                and player_x + player_width > enemy_x
                and player_y < enemy_y + enemy_height
                and player_y + player_height > enemy_y
            ):
                subprocess.Popen("python end_screen.py")
                pygame.quit()

            screen.blit(enemy_image, (enemy_x, enemy_y))

        if bullet_state == "fire":
            screen.blit(bullet_image, (bullet_x, bullet_y))
            bullet_y -= bullet_speed

        for circle in circles:
            circle_x = circle["x"]
            circle_y = circle["y"]

            circle_y += circle_speed

            if (
                player_x < circle_x + bullet_width
                and player_x + player_width > circle_x
                and player_y < circle_y + bullet_height
                and player_y + player_height > circle_y
            ):
                subprocess.Popen("python end_screen.py")
                pygame.quit()

            if circle_y > screen_height:
                circles.remove(circle)

            screen.blit(circle_image, (circle_x, circle_y))

        if random.randint(0, 500) < wave:
            r=random.randint(0,len(enemies)-1)

            circle_x = (enemies[r])["x"]
            circle_y = (enemies[r])["cy"]
            circles.append({"x": circle_x, "y": circle_y})

        for circle in circles:
            circle["y"]+=1

        screen.blit(player_image, (player_x, player_y))
        draw_score()

        if len(enemies) == 0:
            break

        pygame.display.update()
        clock.tick(60)


while True:
    game(w)
    w += 1
