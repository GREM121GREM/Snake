import pygame
import random
from os import path

pygame.init()

WIDTH = 1000
HEIGHT = 700
BG = (108, 108, 115)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 25

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

snake_block = 30
snake_speed = 5

images = path.join(path.dirname(__file__), "img")
music = path.join(path.dirname(__file__), "music")


def create_message(msg, color, x, y, font_name, size):
    font_style = pygame.font.SysFont(font_name, size)
    message = font_style.render(msg, True, color)
    screen.blit(message, (x, y))


def eat_check(xcoord, ycoord, foodx, foody):
    if foodx - snake_block <= xcoord <= foodx + snake_block:
        if foody - snake_block <= ycoord <= foody + snake_block:
            return True
    else:
        return False


head = [
    pygame.image.load(path.join(images, "HeadW.png")),
    pygame.image.load(path.join(images, "HeadA.png")),
    pygame.image.load(path.join(images, "HeadS.png")),
    pygame.image.load(path.join(images, "HeadD.png"))
]


def draw_head(i, snake_body):
    head_img = head[i]
    snake_head = pygame.transform.scale(head_img, (snake_block, snake_block)).convert()
    snake_head.set_colorkey(BLACK)
    snake_head_rect = snake_head.get_rect(x=snake_body[-1][0], y=snake_body[-1][1])
    screen.blit(snake_head, snake_head_rect)


def game_loop():
    score = 0
    snake_body = []
    x_coord = WIDTH / 2 - 15
    y_coord = HEIGHT / 2 - 15
    x_change = 0
    y_change = 0
    snake_len = 2
    i = 0

    pygame.mixer.music.load(path.join(music, "Intense.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

    eat = pygame.mixer.Sound(path.join(music, "apple_bite.ogg"))
    eat.set_volume(0.35)

    hit = pygame.mixer.Sound(path.join(music, "hit_wall.mp3"))
    hit.set_volume(0.3)

    food_x = random.randint(0, WIDTH-snake_block)
    food_y = random.randint(0, HEIGHT-snake_block)

    bg = pygame.image.load(path.join(images, "Fon_grass4.jpg"))
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_rect = bg.get_rect()
    food_img = [
        pygame.image.load(path.join(images, "f_1.png")),
        pygame.image.load(path.join(images, "f_2.png")),
        pygame.image.load(path.join(images, "f_3.png")),
        pygame.image.load(path.join(images, "f_4.png")),
        pygame.image.load(path.join(images, "f_5.png")),
        pygame.image.load(path.join(images, "f_6.png")),
        pygame.image.load(path.join(images, "f_7.png"))

    ]
    food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
    food_rect = food.get_rect(x=food_x, y=food_y)

    game_run = True
    game_close = False

    while game_run:
        clock.tick(FPS)
        screen.fill(BG)
        screen.blit(bg, bg_rect)
        screen.blit(food, food_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -snake_speed
                    x_change = 0
                    i = 0
                elif event.key == pygame.K_LEFT:
                    x_change = -snake_speed
                    y_change = 0
                    i = 1
                elif event.key == pygame.K_DOWN:
                    y_change = +snake_speed
                    x_change = 0
                    i = 2
                elif event.key == pygame.K_RIGHT:
                    x_change = +snake_speed
                    y_change = 0
                    i = 3

        y_coord += y_change
        x_coord += x_change

        if x_coord <= 0 or x_coord >= WIDTH - 20 or y_coord <= 0 or y_coord >= HEIGHT - 20:
            game_run = False
            game_close = True
            hit.play()
            pygame.mixer.music.load(path.join(music, "lose_game.mp3"))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        snake_item = [x_coord, y_coord]
        snake_body.append(snake_item)

        if len(snake_body) > snake_len:
            del snake_body[0]

        for snake in snake_body[1:]:
            # pygame.draw.rect(screen, BLACK, (snake[0], snake[1], snake_block, snake_block))
            body = pygame.image.load(path.join(images, "body3.png"))
            body = pygame.transform.scale(body, (snake_block, snake_block))
            body.set_colorkey(WHITE)
            screen.blit(body, (snake[0], snake[1]))

        for snake in snake_body[1:-1]:
            if snake == snake_item:
                game_run = False
                game_close = True
                pygame.mixer.music.load(path.join(music, "lose_game.mp3"))
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
        draw_head(i, snake_body)

        # pygame.draw.rect(screen, RED, (food_x, food_y, snake_block, snake_block))
        if eat_check(x_coord, y_coord, food_x, food_y):
            food_x = random.randint(0, WIDTH - snake_block)
            food_y = random.randint(0, HEIGHT - snake_block)
            food_img = [
                pygame.image.load(path.join(images, "f_1.png")),
                pygame.image.load(path.join(images, "f_2.png")),
                pygame.image.load(path.join(images, "f_3.png")),
                pygame.image.load(path.join(images, "f_4.png")),
                pygame.image.load(path.join(images, "f_5.png")),
                pygame.image.load(path.join(images, "f_6.png")),
                pygame.image.load(path.join(images, "f_7.png"))

            ]
            food = pygame.transform.scale(random.choice(food_img), (snake_block, snake_block))
            food_rect = food.get_rect(x=food_x, y=food_y)
            eat.play()
            snake_len += 2
            score += 1

        create_message(f"{score}", WHITE, 930, 10, "comicsans", 50)

        while game_close:
            screen.fill(BLACK)
            create_message("Вы проиграли!", RED, 150, 200, "comicsans", 50)
            create_message("Ваш счет  "f"{score}", WHITE, 150, 100, "comicsans", 50)
            create_message("Для закрытия нажмите Q", RED, 150, 300, "comicsans", 50)
            create_message("Чтобы начать заново нажмите R", RED, 150, 400, "comicsans", 50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit()
                    elif event.key == pygame.K_r:
                        game_run = False
                        game_close = False
                        game_loop()

            pygame.display.update()

        pygame.display.update()
        pygame.display.flip()


game_loop()
pygame.quit()
