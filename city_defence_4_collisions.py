import pygame as pg
import random
from os import path

image_dir = path.join(path.dirname(__file__), 'image')

WIDTH, HEIGHT = 450, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("CITY DEFENCE")
clock = pg.time.Clock()

background = pg.image.load(path.join(image_dir, "urban_long.png")).convert()
player_img = pg.image.load(path.join(image_dir, "plane_white.png")).convert()
laser_img = pg.image.load(path.join(image_dir, "laser.png")).convert()

enemy_images = []
enemy_list = ['virus_red.png', 'virus_blue.png', 'virus_violet.png']

for image in enemy_list:
    enemy_images.append(pg.image.load(path.join(image_dir, image)).convert())


def add_enemy():
    x = Enemy()
    all_sprites.add(x)
    enemies.add(x)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (100, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.shoot_delay = 300
        self.last_shot = pg.time.get_ticks()
        self.hidden = False

    def update(self):
        self.speedx = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -7
        if keystate[pg.K_RIGHT]:
            self.speedx = 7
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not self.hidden:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now

                laser = Laser(self.rect.centerx, self.rect.top)
                all_sprites.add(laser)
                lasers.add(laser)

    def hide(self):
        self.hidden = True
        self.rect.center = (WIDTH / 2, HEIGHT + 1000)


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(enemy_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -10)
            self.speedy = random.randrange(2, 10)


class Laser(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pg.sprite.Group()
player = Player()
all_sprites.add(player)
enemies = pg.sprite.Group()
for i in range(5):
    add_enemy()
lasers = pg.sprite.Group()

running = True

while running:

    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    all_sprites.update()

    hits = pg.sprite.groupcollide(enemies, lasers, True, True)
    for hit in hits:
        add_enemy()

    hits = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
    for hit in hits:
        add_enemy()
        player.hide()

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    pg.display.update()

pg.quit()
