import sys

import time

import pygame
from gun import Gun
from pygame.sprite import Group
from stats import Stats
from scores import Scores
from ino import Ino
from bullet import Bullet


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


def update(bg_color, screen, stats, sc, gun, inos, bullets):
    """обновление экрана"""
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    inos.draw(screen)


def update_bullets(screen, stats, sc, inos, bullets):
    """обновление позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, inos, True, True)
    if collisions:
        for inos in collisions.values():
            stats.score += 10 * len(inos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(inos) == 0:
        bullets.empty()
        create_army(screen, inos)


def gun_kill(stats, screen, sc, gun, inos, bullets):
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
    #     create_army(screen, inos)
    #     gun.create_gun()
    #     time.sleep(1)
    # else:
    #     stats.run_game = False
    #     sys.exit()


def update_inos(stats, screen, sc, gun, inos, bullets):
    """обновляет позицию пришельцев"""
    inos.update()
    if pygame.sprite.spritecollideany(gun, inos):
        gun_kill(stats, screen, sc, gun, inos, bullets)
    inos_check(stats, screen, sc, gun, inos, bullets)


def inos_check(stats, screen, sc, gun, inos, bullets):
    """проверка, добралась ли армия до края экрана"""
    screen_rect = screen.get_rect()
    for ino in inos.sprites():
        if ino.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, inos, bullets)
            break


def create_army(screen, inos):
    """создание армии пришельцев"""
    ino = Ino(screen)
    ino_width = ino.rect.width
    ino_height = ino.rect.height
    number_ino_x = int((700 - 2 * ino_width) / ino_width)
    number_ino_y = int((800 - 100 - 2 * ino_height) / ino_height)

    for row_number in range(number_ino_y - 1):
        for ino_number in range(number_ino_x):
            ino = Ino(screen)
            ino.x = ino_width + (ino_width * ino_number)
            ino.y = ino_height + (ino_height * row_number)
            ino.rect.x = ino.x
            ino.rect.y = ino.rect.height + (ino.rect.height * row_number)
            inos.add(ino)


def check_high_score(stats, sc):
    """проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('highscore.txt', 'w') as f:
            f.write(str(stats.high_score))


def table_results():
    pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 800))
    pygame.display.set_caption("Космические защитники")
    bg_color = (0, 0, 0)
    gun = Gun(screen)
    bullets = Group()
    inos = Group()
    create_army(screen, inos)
    stats = Stats()
    sc = Scores(screen, stats)
    start_window = True
    menu = level_game = finish_window = results = rules = False
    # shop =False
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
            pygame.draw.rect(screen, ('white'), (100, 150, 500, 450))
            font = pygame.font.Font(None, 50)
            text = font.render("WELCOME", True, 'PURPLE')
            text_x = text.get_width() + 70
            text_y = text.get_height() + 300
            screen.blit(text, (text_x, text_y))
            level = 1
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
                        level_game = True
                        k = 1
                    if 107 <= x <= 244 and 163 <= y <= 217:
                        menu = False
                        rules = True
                        k = 1
        elif rules:
            screen.fill(bg_color)
            pygame.draw.rect(screen, ('white'), (100, 150, 500, 450))
            font = pygame.font.Font(None, 50)
            text = font.render("Тут должны быть правила", True, 'black')
            text_x = text.get_width() - 330
            text_y = text.get_height() + 300
            screen.blit(text, (text_x, text_y))
            text = font.render("CLOSE RULES", True, 'RED')
            text_x = text.get_width() - 130
            text_y = text.get_height() + 140
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
                    if 104 <= x <= 365 and 164 <= y <= 217:
                        rules = False
                        menu = True
                        k = 1






        elif level_game:
            screen.fill(bg_color)
            if k == 1:
                gun.zero_update_gun(screen)
                k = 0
            events(screen, gun, bullets)
            if stats.run_game:
                gun.update_gun()
                update(bg_color, screen, stats, sc, gun, inos, bullets)
                update_bullets(screen, stats, sc, inos, bullets)
                update_inos(stats, screen, sc, gun, inos, bullets)

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
            table_results()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 400 and 350 <= y <= 450:
                        menu = True
                        results = False

        pygame.display.flip()
