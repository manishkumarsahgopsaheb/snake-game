import pygame
import random
import os

# initialization of pygame
pygame.init()

# colors

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
welcome_color = (236, 179, 255)
# creating window of our pygame
screen_width = 900
screen_height = 600
game_window = pygame.display.set_mode((screen_width, screen_height))  # it accept the argument as tuple
pygame.display.set_caption("Snake Game By Manish Kumar Sah")
pygame.display.update()

# lets make a clock so that our snake can move with some velocity i.e velocity = distance/time
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 45)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


def plot_snake(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(game_window, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        game_window.fill(welcome_color)
        text_screen("Welcome To Manish's Snake Game!", black, 200, 200)
        text_screen("Press Space To Play", black, 275, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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
            text_screen("Saanp Mar Gya! Enter Dabao Phir Se Khelna Hai To...", red, 80, 250)
            text_screen("Your Score is: " + str(score) + " and High Score is: " + str(high_score), red, 125, 125)
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
            text_screen("Score: " + str(score), red, 5, 5)
            text_screen("High Score: " + str(high_score), red, 650, 5)
            pygame.draw.rect(game_window, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(game_window, black, snake_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
