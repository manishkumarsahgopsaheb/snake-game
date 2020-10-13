import pygame
import random
import os

pygame.mixer.init()
# initialization of pygame
pygame.init()

# colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
welcome_color = (236, 179, 255)
red_last = (204, 0, 0)
# creating window of our pygame
screen_width = 900
screen_height = 600
game_window = pygame.display.set_mode((screen_width, screen_height))  # it accept the argument as tuple

# Background image
bgimg = pygame.image.load("backimage.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# welcome image
bgimg_start = pygame.image.load("snakeback.jpg")
bgimg_start = pygame.transform.scale(bgimg_start, (screen_width, screen_height)).convert_alpha()

manish = pygame.image.load("manish.jpg")
manish = pygame.transform.scale(manish, (200, 200)).convert_alpha()
pygame.display.set_caption("Snake Game By Manish Kumar Sah")
pygame.display.update()

# lets make a clock so that our snake can move with some velocity i.e velocity = distance/time
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


def game_instructions():
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    exit_game = False

    while not exit_game:
        game_window.fill(white)
        game_window.blit(bgimg, (0, 0))
        game_window.blit(manish, (350, 25))
        text_screen("Game Instructions!:", white, 50, 240)
        text_screen("(Press Space Bar To Continue...)", white, 500, 240)
        text_screen("1. Use Arrow Keys For X And Y Move", white, 100, 280)
        text_screen("2. If Snake Is Moving In +X dir Then, Do Not Press Left Arrow Key", white, 100, 320)
        text_screen("3. If Snake Is Moving In -X dir Then, Do Not Press Right Arrow Key", white, 100, 360)
        text_screen("4. If Snake Is Moving In +Y dir Then, Do Not Press Down Arrow Key", white, 100, 400)
        text_screen("5. If Snake Is Moving In -Y dir Then, Do Not Press Up Arrow Key", white, 100, 440)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    welcome()

        pygame.display.update()
        clock.tick(30)


def welcome():
    pygame.mixer.music.load('welcome.mp3')
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        game_window.fill(welcome_color)
        # game_window.blit(manish, (0, 0))
        game_window.blit(bgimg_start, (0, 0))

        text_screen("Welcome To Manish's Snake Game!", black, 200, 200)
        text_screen("Press Space Bar To Play", black, 275, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('background.mp3')
                    pygame.mixer.music.play()
                    game_loop()
        pygame.display.update()
        clock.tick(30)


# creating a game loop
def game_loop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45  # initial position of snake(snake_x, snake_y)
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5

    food_x = random.randint(20, screen_width / 1.5)
    food_y = random.randint(20, screen_height / 1.5)
    score = 0
    snake_size = 15
    fps = 30

    snake_list = []
    snake_length = 1
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
            game_window.fill(white)
            game_window.blit(bgimg_start, (0, 0))

            text_screen("Saanp Mar Gya! Enter Dabao Phir Se Khelna Hai To...", red_last, 80, 200)
            text_screen("Your Score : " + str(score), black, 80, 125)
            text_screen("High Score : " + str(high_score), black, 600, 125)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                # why i have been used event.type before this(event.key) if condition, reason
                # is event.key does not exist without event.type
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score = score + 10
                food_x = random.randint(20, screen_width / 1.5)
                food_y = random.randint(20, screen_height / 1.5)

                snake_length = snake_length + 5

                if score > int(high_score):
                    high_score = score

            game_window.fill(white)
            game_window.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score), red, 5, 5)
            text_screen("High Score: " + str(high_score), red, 650, 5)
            pygame.draw.rect(game_window, green, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('burst.mp3')
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('burst.mp3')
                pygame.mixer.music.play()

            plot_snake(game_window, green, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


game_instructions()
