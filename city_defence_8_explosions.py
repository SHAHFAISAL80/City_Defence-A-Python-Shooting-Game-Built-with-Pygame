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

font_name = pg.font.match_font('arial bold')

background_start = pg.image.load(path.join(image_dir, "urban_long_grey.png")).convert()
background = pg.image.load(path.join(image_dir, "urban_long.png")).convert()
player_img = pg.image.load(path.join(image_dir, "plane_white.png")).convert()
laser_img = pg.image.load(path.join(image_dir, "laser.png")).convert()
heart_img = pg.image.load(path.join(image_dir, "heart.png")).convert()
heart_mini_img = pg.transform.scale(heart_img, (25, 19))
heart_mini_img.set_colorkey(BLACK)

enemy_images = []
enemy_list = ['virus_red.png', 'virus_blue.png', 'virus_violet.png']

for image in enemy_list:
    enemy_images.append(pg.image.load(path.join(image_dir, image)).convert())


def draw_text(surface, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(image, img_rect)


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
        self.lives = 3
        self.hide_timer = pg.time.get_ticks()

    def update(self):
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

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
        self.hide_timer = pg.time.get_ticks()
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


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        pg.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 20

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def show_go_screen():
    screen.blit(background_start, (0, 0))
    draw_text(screen, "CITY DEFENCE!", 64, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Press any key to begin", 32, WIDTH / 2, HEIGHT / 7 * 3)
    draw_text(screen, "(Arrow keys to move, Space to fire)", 18, WIDTH / 2, HEIGHT / 8 * 4 - 20)

    pg.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


explosion_anim = {}
explosion_anim['large'] = []
explosion_anim['small'] = []

for i in range(7):
    filename = 'explosion_0{}.png'.format(i)
    img = pg.image.load(path.join(image_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_large = pg.transform.scale(img, (75, 75))
    explosion_anim['large'].append(img_large)
    img_small = pg.transform.scale(img, (32, 32))
    explosion_anim['small'].append(img_small)

game_over = True
running = True

while running:

    clock.tick(FPS)

    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        enemies = pg.sprite.Group()
        for i in range(5):
            add_enemy()
        lasers = pg.sprite.Group()

        score = 0

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    all_sprites.update()

    hits = pg.sprite.groupcollide(enemies, lasers, True, True)
    for hit in hits:
        score += int(hit.radius)
        expl = Explosion(hit.rect.center, 'large')
        all_sprites.add(expl)
        add_enemy()

    hits = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        add_enemy()
        death_explosion = Explosion(player.rect.center, 'large')
        all_sprites.add(death_explosion)
        player.hide()
        player.lives -= 1

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    draw_lives(screen, WIDTH - 100, 5, player.lives, heart_mini_img)
    draw_text(screen, str(score), 36, WIDTH / 2, 5)

    pg.display.update()

pg.quit()
