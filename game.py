import sys
import sqlite3

import time

import pygame
from gun import Gun
from pygame.sprite import Group

# from scores import Scores
from ino import Ino
from bullet import Bullet

clock = pygame.time.Clock()


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


def update(bg_color, screen, gun, inos, bullets):
    """обновление экрана"""
    # sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    inos.draw(screen)


def update_bullets(screen, inos, bullets, f):
    """обновление позиции пуль"""
    global level_game
    global win
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
        win = True
        level_game = False


def gun_kill(screen, gun, inos, bullets):
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


def update_inos(screen, gun, inos, bullets):
    """обновляет позицию пришельцев"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(screen, gun, inos, bullets)
    inos_check(screen, gun, inos, bullets)


def inos_check(screen, gun, inos, bullets):
    """проверка, добралась ли армия до края экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(screen, gun, inos, bullets)
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
# def check_high_score( sc):
#     """проверка новых рекордов"""
#     if stats.score > stats.high_score:
#         stats.high_score = stats.score
#         sc.image_high_score()
#         with open('highscore.txt', 'w') as f:
#             f.write(str(stats.high_score))


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Space Defenders")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()

    # sc = Scores(screen, stats)
    start_window = True
    menu = level_game = finish_window = rating = rules = animation = win = False
    k = 0
    user_name = ''
    color = 'green'
    input_rect = pygame.Rect(130, 350, 440, 32)
    while True:
        if start_window:
            screen.fill(bg_color)

            screen.blit(pygame.image.load('заставка.png'), (0, 0))
            pygame.draw.rect(screen, 'Black', (150, 200, 400, 400))
            pygame.draw.rect(screen, ('black'), (100, 150, 500, 450))
            font = pygame.font.Font(None, 70)
            text = font.render("WELCOME", True, (164, 255, 161))
            text_x = (700 - text.get_width()) // 2
            text_y = (800 - text.get_height()) // 2 - 160
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 30)
            text = font.render("User name:", True, (164, 255, 161))
            text_x = 130
            text_y = (800 - text.get_height()) // 2 - 70
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 23)
            text = font.render("(use letters and numbers, no more than 11, no less than 0)", True, (164, 255, 161))
            text_x = 130
            text_y = (800 - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 35)
            text = font.render("Done!", True, (164, 255, 161))
            text_x = text.get_width() + 250
            text_y = text.get_height() + 440
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (164, 255, 161), (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20), 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 381 and 451 <= y <= 493 and 11 > len(user_name) > 0:
                        start_window = False
                        menu = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(user_name) > 0:
                            user_name = user_name[:-1]
                            if len(user_name) > 10:
                                color = 'red'
                            else:
                                color = 'green'

                    else:
                        if len(user_name) > 10:
                            color = 'red'
                        else:
                            color = 'green'
                        user_name += event.unicode

            pygame.draw.rect(screen, color, input_rect, 2)
            text_surface = font.render(user_name, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(300, text_surface.get_width() + 10)
            pygame.display.flip()
            clock.tick(60)

            f = 1




        elif menu:
            if f == 1:
                # данные считываются из бд и впоследствии используются в функциях: create_army, table_results
                con = sqlite3.connect("rating.db")
                cur = con.cursor()
                result = cur.execute(f"""SELECT level FROM main
                                    WHERE name == '{user_name}'""").fetchall()
                if result:
                    level = result[0][0]
                else:
                    con = sqlite3.connect("rating.db")

                    # Создание курсора
                    cur = con.cursor()

                    # Выполнение запроса и получение всех результатов
                    result = cur.execute(f"""INSERT INTO main(name, level) VALUES ('{user_name}', 1)""").fetchall()
                    con.commit()
                    level = 1

                if level < 5:
                    image = 'ino(2).png'
                elif level < 10:
                    image = 'ino.png'
                else:
                    image = 'pr.png'

                create_army(screen, inos, level, image)
                f = 0
            screen.fill(bg_color)
            font = pygame.font.SysFont('inkfree', 90)
            text = font.render("Space Defenders", True, (204, 100, 255))
            text_x = (700 - text.get_width()) // 2
            text_y = text.get_height() + 120
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 50)
            text = font.render("LEVEL " + str(level), True, (255, 153, 102))
            text_x = (700 - text.get_width()) // 2
            text_y = (800 - text.get_height()) // 2 + 50
            screen.blit(text, (text_x, text_y))
            text = font.render("PLAY", True, (0, 230, 80))
            t_x = (700 - text.get_width()) // 2
            t_y = (800 - text.get_height()) // 2 + 150
            screen.blit(text, (t_x, t_y))
            t_w = text.get_width()
            t_h = text.get_height()
            pygame.draw.rect(screen, (0, 230, 80), (t_x - 10, t_y - 10, t_w + 20, t_h + 20), 1)

            text = font.render("RATING", True, (135, 250, 255))
            text_x = 530
            text_y = 40
            screen.blit(text, (text_x, text_y))
            w = text.get_width()
            h = text.get_height()
            pygame.draw.rect(screen, (135, 250, 255), (text_x - 10, text_y - 10, w + 20, h + 20), 1)

            text = font.render("RULES", True, (190, 0, 121))
            text_x = 30
            text_y = 40
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (183, 110, 121), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if t_x - 10 <= x <= t_x + t_w + 10 and t_y - 10 <= y <= t_y + t_h + 10:
                        menu = False
                        animation = True
                        k = 1
                        f = 1
                    elif 30 <= x <= 30 + text.get_width() and 40 <= y <= 40 + text.get_width():
                        menu = False
                        rules = True
                        k = 1
                        f = 1
                    elif 500 <= x <= 520 + w and 30 <= y <= 50 + h:
                        menu = False
                        rating = True
                        k = 1
                        f = 1
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

        elif rating:
            screen.fill(bg_color)
            font = pygame.font.Font(None, 55)
            text = font.render("Player's Rating", True, (135, 250, 255))
            text_x = 100 + (500 - text.get_width()) // 2
            text_y = 100
            screen.blit(text, (text_x, text_y))
            font = pygame.font.Font(None, 35)
            text = font.render(f"username", True, 'white')
            text_x = (700 - text.get_width()) // 2 - 120
            text_y = (800 - text.get_height()) // 2 - 175
            screen.blit(text, (text_x, text_y))
            text = font.render(f"level", True, 'white')
            text_x = (700 - text.get_width()) // 2 + 120
            text_y = (800 - text.get_height()) // 2 - 175
            screen.blit(text, (text_x, text_y))
            con = sqlite3.connect("rating.db")
            cur = con.cursor()
            result = cur.execute(f"""SELECT * FROM main""").fetchall()
            sorted_results = sorted(result, key=lambda x: x[1], reverse=True)
            k = 0

            for i in sorted_results:
                k += 1
                colorr = (148 + (k - 1) * 16, 250 - (k - 1) * 20, 0)
                text = font.render(f"{i[0]}", True, colorr)
                text_x = (700 - text.get_width()) // 2 - 120
                text_y = (800 - text.get_height()) // 2 + k * 35 - 160
                screen.blit(text, (text_x, text_y))

                text = font.render(f"{i[1]}", True, colorr)
                text_x = (700 - text.get_width()) // 2 + 120
                text_y = (800 - text.get_height()) // 2 + k * 35 - 160
                screen.blit(text, (text_x, text_y))
                if k == 5:
                    break

            text = font.render(f"{user_name}", True, 'white')
            text_x = (700 - text.get_width()) // 2 - 120
            text_y = (800 - text.get_height()) // 2 + 7.5 * 36 - 160
            screen.blit(text, (text_x, text_y))
            text = font.render(f"{level}", True, 'white')
            text_x = (700 - text.get_width()) // 2 + 120
            text_y = (800 - text.get_height()) // 2 + 7.5 * 36 - 160
            screen.blit(text, (text_x, text_y))

            font = pygame.font.Font(None, 44)
            text = font.render("Colse", True, (135, 250, 255))
            text_x = (700 - text.get_width()) // 2 + 5
            text_y = (800 - text.get_height()) // 2 + 250
            screen.blit(text, (text_x, text_y))
            text_w = text.get_width()
            text_h = text.get_height()
            pygame.draw.rect(screen, (135, 206, 235), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if text_x - 10 <= x <= text.get_width() + text_x + 10 and text_y - 10 <= y <= text.get_height() + text_y + 10:
                        rating = False
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
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                if kol > 700:
                    running = False

            animation = False
            level_game = True

        elif level_game:
            f = 1
            screen.fill(bg_color)
            if k == 1:
                gun.zero_update_gun(screen)
                k = 0
            events(screen, gun, bullets)

            gun.update_gun()
            update(bg_color, screen, gun, inos, bullets)
            update_bullets(screen, inos, bullets, f)
            update_inos(screen, gun, inos, bullets)

            gun.output()
        elif win:
            screen.fill(bg_color)
            font = pygame.font.Font(None, 40)
            text = font.render('Level successfully completed!)', True, 'green')
            text_x = (700 - text.get_width()) // 2
            text_y = (800 - text.get_height()) // 2
            screen.blit(text, (text_x, text_y))
            con = sqlite3.connect("rating.db")

            # Создание курсора
            cur = con.cursor()

            # Выполнение запроса и получение всех результатов
            result = cur.execute(f"""UPDATE main SET level={level + 1} 
                        WHERE name == '{user_name}'""").fetchall()
            con.commit()
            con.close()
            pygame.display.flip()
            time.sleep(2.4)
            menu = True
            win = False
            f = 1

        elif finish_window:

            screen.fill(bg_color)

            font = pygame.font.Font(None, 40)
            text = font.render('Level failed(', True, 'red')
            text_x = (700 - text.get_width()) // 2
            text_y = (800 - text.get_height()) // 2 - 20
            screen.blit(text, (text_x, text_y))
            text = font.render('Try again', True, 'red')
            text_x = (700 - text.get_width()) // 2
            text_y = (800 - text.get_height()) // 2 + 20
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            time.sleep(2.4)
            menu = True
            finish_window = False
            f = 1





        elif results:
            screen.fill(bg_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 400 and 350 <= y <= 450:
                        menu = True
                        results = False
                        f = 1

        pygame.display.flip()
