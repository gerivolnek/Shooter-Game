from pygame import *
import pygame.time
from random import randint

rocket = "rocket.png"
genya = 1

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 90:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
            self.rect.y += self.speed
            global lost
            if self.rect.y > win_height:
                self.rect.x = randint(80, win_width - 80)
                self.rect.y = 0
                lost = lost + 1
                self.speed = randint(1,5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#zene
mixer.init()
mixer.music.load('space.ogg')
#mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


#ablak
win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#karakterek
player = Player(rocket, 5, win_height - 100, 80, 100, 10)

ufok = sprite.Group()
for i in range(genya):
    ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    ufok.add(ufo)

bullets = sprite.Group()

font.init()
font1 = font.Font(None, 36)

game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                player.fire()


    if not finish:
        window.blit(background,(0, 0))
        text_score = font1.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))
        text_lost = font1.render("Lost: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))

        player.update()
        player.reset()
        ufok.update()
        ufok.draw(window)
        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(ufok, bullets, True, True)
        for c in collides:
            score += 1
            ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            ufok.add(ufo)

        if genya == 3: 
            win = font1.render("YOU WIN!", True, (200, 0, 0))
            window.blit(win, (300, 250))
            finish = True      
            time.delay(2000)
            game = False

        if score >= 10 and genya < 3:
            finish = True
            levelup = font1.render("LEVEL UP!", True, (255, 255, 255))
            window.blit(levelup, (300, 250))
            genya += 1

        if lost > 3 or sprite.spritecollide(player, ufok, False):
            finish = True
            lose = font1.render("YOU LOST!", True, (200, 0, 0))
            window.blit(lose, (300, 250))

        display.update()

    else:
        finish = False
        score, lost = 0, 0
        for b in bullets:
            b.kill()
        for ufo in ufok:
            ufo.kill()
        time.delay(1000)
        for i in range(genya):
            ufo = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            ufok.add(ufo)

    time.delay(15)

display.update()
