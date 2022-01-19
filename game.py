import sys
import sqlite3

import time

import pygame
from gun import Gun
from pygame.sprite import Group
from stats import Stats
# from scores import Scores
from ino import Ino
from bullet import Bullet


#
# # Подключение к БД
# con = sqlite3.connect("films_db.sqlite")
#
# # Создание курсора
# cur = con.cursor()
#
# # Выполнение запроса и получение всех результатов
# result = cur.execute("""SELECT * FROM films
#             WHERE year = 2010""").fetchall()
#
# # Вывод результатов на экран
# for elem in result:
#     print(elem)
#
# con.close()


def events(screen, gun, bullets):
    """обработка нажатий клавиш"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                gun.mright = True
            elif event.key == pygame.K_LEFT:
                gun.mleft = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gun.mright = False
            elif event.key == pygame.K_LEFT:
                gun.mleft = False


def update(bg_color, screen, stats, gun, inos, bullets):
    """обновление экрана"""
    # sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    inos.draw(screen)


def update_bullets(screen, stats, inos, bullets):
    """обновление позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    # if collisions:
    # for inos in collisions.values():
    # stats.score += 10 * len(inos)
    # sc.image_score()
    # check_high_score(stats)
    # sc.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos, level, image)


def gun_kill(stats, screen, gun, inos, bullets):
    global finish_window
    global level_game
    inos.empty()
    bullets.empty()
    finish_window = True
    level_game = False
    # """столкновение пушки и армии"""
    # if stats.guns_left > 0:
    #     stats.guns_left -= 1
    #     sc.image_guns()
    #     inos.empty()
    #     bullets.empty()
    #     create_army(screen, inos, level)
    #     gun.create_gun()
    #     time.sleep(1)
    # else:
    #     stats.run_game = False
    #     sys.exit()


def update_inos(stats, screen, gun, inos, bullets):
    """обновляет позицию пришельцев"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, gun, inos, bullets)
    inos_check(stats, screen, gun, inos, bullets)


def inos_check(stats, screen, gun, inos, bullets):
    """проверка, добралась ли армия до края экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, gun, inos, bullets)
            break


def create_army(screen, inos, level, image):
    """создание армии пришельцев"""
    if level < 5:
        w = 7
        number_ino_x = (level * 2 - 1)
        number_ino_y = (level + 2)
    elif level < 10:
        w = 12
        number_ino_x = (level - 3) * 2
        number_ino_y = level + 2
    else:
        w = 19
        if level <= 17:
            number_ino_x = 2 * (level - 8)
            number_ino_y = level + 1
        else:
            number_ino_x = 19
            number_ino_y = 18
    ino = Ino(screen, image)
    ino_width = ino.rect.width
    ino_height = ino.rect.height
    # number_ino_x = int((700 - x * ino_width) / ino_width)
    # number_ino_y = int((800 - 100 - y * ino_height) / ino_height)

    for row_number in range(number_ino_y):
        for ino_number in range(number_ino_x):
            ino = Ino(screen, image)
            ino.x = ino_width * (w - number_ino_x + 2) // 2 + (ino_width * ino_number)
            ino.y = ino_height + (ino_height * row_number)
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)
            inos.add(ino)


#
# def check_high_score(stats, sc):
#     """проверка новых рекордов"""
#     if stats.score > stats.high_score:
#         stats.high_score = stats.score
#         sc.image_high_score()
#         with open('highscore.txt', 'w') as f:
#             f.write(str(stats.high_score))


def table_results(name, level):
    pass


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Космические защитники")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    # данные считываются из бд и впоследствии используются в функциях: create_army, table_results
    name = 0
    level = 5
    if level < 5:
        image = 'ino(2).png'
    elif level < 10:
        image = 'ino.png'
    else:
        image = 'pr.png'

    create_army(screen, inos, level, image)
    stats = Stats()
    # sc = Scores(screen, stats)
    start_window = True
    menu = level_game = finish_window = results = rules = animation = False
    k = 0
    while True:
        if start_window:
            screen.fill(bg_color)
            pygame.draw.rect(screen, (0, 255, 0), (300, 350, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 400 and 350 <= y <= 450:
                        start_window = False
                        menu = True


        elif menu:
            screen.fill(bg_color)
            # pygame.draw.rect(screen, ('black'), (100, 150, 500, 450))
            font = pygame.font.Font(None, 50)
            text = font.render("WELCOME", True, 'PURPLE')
            text_x = text.get_width() + 70
            text_y = text.get_height() + 300
            screen.blit(text, (text_x, text_y))
            text = font.render("LEVEL " + str(level), True, 'BLUE')
            text_x = text.get_width() + 128
            text_y = text.get_height() + 370
            screen.blit(text, (text_x, text_y))
            text = font.render("RULES", True, 'RED')
            text_x = text.get_width()
            text_y = text.get_height() + 140
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, 'RED', (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)
            text = font.render("PLAY", True, 'GREEN')
            text_x = text.get_width() + 200
            text_y = text.get_height() + 440
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 278 <= x <= 385 and 464 <= y <= 518:
                        menu = False
                        animation = True
                        k = 1
                    if 107 <= x <= 244 and 163 <= y <= 217:
                        menu = False
                        rules = True
                        k = 1
        elif rules:
            screen.fill(bg_color)
            pygame.draw.rect(screen, ('white'), (100, 150, 500, 450))
            font = pygame.font.Font(None, 40)
            text = font.render("RULS", True, 'red')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 160
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 30)
            text = font.render('Press the "PLAY" button to start the game', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 220
            screen.blit(text, (text_x, text_y))
            text = font.render('Goal of the game: exterminate all alien', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 250
            screen.blit(text, (text_x, text_y))
            text = font.render('Use spacebar to shoot', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 280
            screen.blit(text, (text_x, text_y))
            text = font.render('Using the arrows you can move the cannon', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 310
            screen.blit(text, (text_x, text_y))
            text = font.render('to defend against the aliens', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 330
            screen.blit(text, (text_x, text_y))
            text = font.render('If you fail to pass the level, you can try again', True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 360
            screen.blit(text, (text_x, text_y))
            # you can keep trying until the level is completed
            text = font.render("You have an infinite number of attempts per level", True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 390
            screen.blit(text, (text_x, text_y))
            text = font.render("Upon successful completion, it won't be possible", True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 420
            screen.blit(text, (text_x, text_y))
            text = font.render("to return to the previous level", True, 'black')
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = text.get_height() + 440
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 40)
            text = font.render("Got it!", True, 'RED')
            text_x = (700 - text.get_width()) // 2 + 5
            text_y = (800 - text.get_height()) // 2 + 140
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, 'RED', (text_x - 10, text_y - 10,
                                             text_w + 20, text_h + 20), 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if text_x - 10 <= x <= text.get_width() + text_x + 10 and text_y - 10 <= y <= text.get_height() + text_y + 10:
                        rules = False
                        menu = True
                        k = 1

        elif animation:
            screen.fill('black')
            illustration = [pygame.image.load('кадр 1.png'), pygame.image.load('кадр 2.png'),
                            pygame.image.load('кадр 3.png'), pygame.image.load('кадр 4.png'),
                            pygame.image.load('кадр 5.png'), pygame.image.load('кадр 6.png'),
                            pygame.image.load('кадр 7.png'), pygame.image.load('кадр 8.png'),
                            pygame.image.load('кадр 9.png'), pygame.image.load('кадр 10.png'),
                            pygame.image.load('кадр 11.png'), pygame.image.load('кадр 12.png')
                            ]

            width = 254
            height = 254
            count = 0
            running = True
            kol = 0

            while running:
                kol += 10

                screen.blit(illustration[count], (kol, 300))
                pygame.display.update()

                if count == 11:

                    count = 0
                else:
                    count += 1

                clock.tick(20)
                screen.fill(bg_color)
                pygame.display.update()
                if kol > 700:
                    print(44)
                    running = False

            animation = False
            level_game = True


        elif level_game:
            screen.fill(bg_color)
            if k == 1:
                gun.zero_update_gun(screen)
                k = 0
            events(screen, gun, bullets)
            if stats.run_game:
                gun.update_gun()
                update(bg_color, screen, stats, gun, inos, bullets)
                update_bullets(screen, stats, inos, bullets)
                update_inos(stats, screen, gun, inos, bullets)

            gun.output()

        elif finish_window:
            screen.fill(bg_color)
            pygame.draw.rect(screen, (255, 0, 0), (300, 350, 100, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 400 and 350 <= y <= 450:
                        menu = True
                        finish_window = False

        elif results:
            screen.fill(bg_color)
            table_results(name, level)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 400 and 350 <= y <= 450:
                        menu = True
                        results = False

        pygame.display.flip()
