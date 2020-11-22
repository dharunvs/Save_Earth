import sys
import random
import math

import pygame
from setting import *


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Save Earth")
        self.icon = pygame.image.load("sources/icon/icon.png")
        pygame.display.set_icon(self.icon)

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.font = "Arial"

        self.distance = 0

        self.start_time = 0
        self.end_time = 0
        self.elapsed_time = 0

        self.start_screen = pygame.image.load("sources/screens/start.png")
        self.background = pygame.image.load("sources/background/background2.png")
        self.settings_background = pygame.image.load("sources/screens/settings.png")
        self.tick = pygame.image.load("sources/screens/tick.png")

        self.background_choice = 0
        self.planet_choice = 0

        self.life1 = pygame.image.load("sources/lives/1.png")
        self.life2 = pygame.image.load("sources/lives/2.png")
        self.life3 = pygame.image.load("sources/lives/3.png")
        self.lives = 3

        self.player_speed = PLAYER_SPEED
        self.enemy_speed = ENEMY_SPEED

        self.player_img = pygame.image.load("sources/planet/earth1.png")
        self.playerX = WIDTH/2.2
        self.playerY = HEIGHT/2.2
        self.playerX_change = 0
        self.playerY_change = 0

        self.enemy_img = pygame.image.load("sources/virus/virus.png")
        self.enemyX = random.randint(WIDTH/2 + 60, WIDTH)
        self.enemyY = random.randint(HEIGHT-HEIGHT, HEIGHT)
        self.enemyX_change = ENEMY_SPEED
        self.enemyY_change = ENEMY_SPEED

        self.score = 0
        self.high_score = 0
        self.last_score = 0

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'settings':
                self.settings_events()
                self.settings_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

# ------------------------------------------ HELPING FUNCTIONS ---------------------------------------------------------
    def draw_text(self, words, pos, font_size, font_name, color):
        pygame.font.init()
        font = pygame.font.SysFont(font_name, font_size)
        text = font.render(words, False, color)
        self.screen.blit(text, pos)

    def player(self):
        self.screen.blit(self.player_img, (self.playerX, self.playerY))

    def enemy(self):
        self.screen.blit(self.enemy_img, (self.enemyX, self.enemyY))

    def collision(self):
        self.distance = math.sqrt(math.pow(self.playerX - self.enemyX, 2) +
                                  math.pow(self.playerY - self.enemyY, 2))

        if self.distance < 60:
            return True

    def lives_bar(self):
        if self.lives == 3:
            self.screen.blit(self.life3, (4, 400))
        elif self.lives == 2:
            self.screen.blit(self.life2, (4, 400))
        elif self.lives == 1:
            self.screen.blit(self.life1, (4, 400))

# ------------------------------------------ START FUNCTIONS ---------------------------------------------------------

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.state = 'settings'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.start_screen, (0, 0))

        self.draw_text(f"{self.high_score}", (173, 396), 28,
                       self.font, (255, 255, 255))
        self.draw_text(f"{self.last_score}", (527, 396), 28,
                       self.font, (255, 255, 255))
        pygame.display.update()

# ------------------------------------------ PLAYING FUNCTIONS ---------------------------------------------------------

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # player movements

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.playerY_change -= self.player_speed

                if event.key == pygame.K_DOWN:
                    self.playerY_change += self.player_speed

                if event.key == pygame.K_RIGHT:
                    self.playerX_change += self.player_speed

                if event.key == pygame.K_LEFT:
                    self.playerX_change -= self.player_speed

            if event.type == pygame.KEYUP:
                if \
                        event.key == pygame.K_UP or \
                        event.key == pygame.K_DOWN or \
                        event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_LEFT:

                    self.playerX_change = 0
                    self.playerY_change = 0

        self.playerX += self.playerX_change
        self.playerY += self.playerY_change

        if self.playerX <= 1:
            self.playerX = 1

        if self.playerX >= 529:
            self.playerX = 529

        if self.playerY <= 1:
            self.playerY = 1

        if self.playerY >= 379:
            self.playerY = 379

    # enemy movements
        self.enemyX += self.enemyX_change
        self.enemyY += self.enemyY_change
        self.score += 1

    # enemy level (increased speed)
        if self.score == 500:
            self.enemy_speed += 3

        elif self.score == 1000:
            self.enemy_speed += 2

        elif self.score == 2000:
            self.enemy_speed += 2

    ##

        if self.enemyX <= 1:
            self.enemyX_change = self.enemy_speed

        if self.enemyX >= 549:
            self.enemyX_change = -self.enemy_speed

        if self.enemyY <= 1:
            self.enemyY_change = self.enemy_speed

        if self.enemyY >= 399:
            self.enemyY_change = -self.enemy_speed

    def playing_update(self):
        if self.collision():
            self.enemyX_change = 0
            self.enemyY_change = 0
            self.playerX_change = 0
            self.playerY_change = 0
            self.lives -= 1
            self.enemyX = random.randint(WIDTH / 2 + 60, WIDTH)
            self.enemyY = random.randint(HEIGHT-HEIGHT, HEIGHT)
            self.enemyX_change = ENEMY_SPEED
            self.enemyY_change = ENEMY_SPEED

        if self.high_score < self.score:
            self.high_score = self.score
        self.last_score = self.score

        if self.lives == 0:
            self.state = "start"
            self.score = 0
            self.playerX = WIDTH / 2.2
            self.playerY = HEIGHT / 2.2
            self.playerX_change = 0
            self.playerY_change = 0
            self.enemyX = random.randint(WIDTH / 2 + 60, WIDTH)
            self.enemyY = random.randint(HEIGHT-HEIGHT, HEIGHT)
            self.enemyX_change = ENEMY_SPEED
            self.enemyY_change = ENEMY_SPEED
            self.lives = 3
            self.enemy_speed = ENEMY_SPEED

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))

        self.draw_text(f"Score: {self.score}", (5, 5), 25, self.font, (255, 255, 255))

        self.lives_bar()
        self.enemy()
        self.player()

        pygame.display.update()

# ------------------------------------------ SETTINGS FUNCTIONS --------------------------------------------------------

    def settings_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.state = 'start'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.background = pygame.image.load("sources/background/background1.png")
                    self.background_choice = 1

                if event.key == pygame.K_2:
                    self.background = pygame.image.load("sources/background/background2.png")
                    self.background_choice = 2

                if event.key == pygame.K_3:
                    self.background = pygame.image.load("sources/background/background3.png")
                    self.background_choice = 3

                if event.key == pygame.K_q:
                    self.player_img = pygame.image.load("sources/planet/earth1.png")
                    self.planet_choice = 1

                if event.key == pygame.K_w:
                    self.player_img = pygame.image.load("sources/planet/earth2.png")
                    self.planet_choice = 2

    def settings_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.settings_background, (0, 0))

        if self.background_choice == 0:
            self.screen.blit(self.tick, (355, 100))

        elif self.background_choice == 1:
            self.screen.blit(self.tick, (165, 100))

        elif self.background_choice == 2:
            self.screen.blit(self.tick, (355, 100))

        elif self.background_choice == 3:
            self.screen.blit(self.tick, (545, 100))

        if self.planet_choice == 0:
            self.screen.blit(self.tick, (175 + 50, 350))

        elif self.planet_choice == 1:
            self.screen.blit(self.tick, (175 + 50, 350))

        elif self.planet_choice == 2:
            self.screen.blit(self.tick, (445 + 50, 350))

        pygame.display.update()
        

if __name__ == '__main__':
    app = App()
    app.run()
