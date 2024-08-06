import pygame as pg
import random
from os import path

image_dir = path.join(path.dirname(__file__), 'image')

HS_FILE = "highscore.txt"

WIDTH, HEIGHT = 450, 600
FPS = 60

POWERUP_TIME = 6000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

pg.init()

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("CITY DEFENCE")
clock = pg.time.Clock()

font_name = pg.font.match_font('arial bold')

global score
score = 0

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


def draw_shield_bar(surface, x, y, percent):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    if percent < 0:
        percent = 0
    fill = (percent / 100) * BAR_LENGTH
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pg.draw.rect(surface, GREEN, fill_rect)
    pg.draw.rect(surface, WHITE, outline_rect, 2)


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
        self.shield = 100
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.powerup_time = pg.time.get_ticks()
        self.radius = int(self.rect.width * .8 / 2)

    def update(self):
        if self.power >= 2 and pg.time.get_ticks() - self.powerup_time > POWERUP_TIME:
            self.power -= 1
            self.powerup_time = pg.time.get_ticks()

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

    def powerup(self):
        self.power += 1
        self.powerup_time = pg.time.get_ticks()

    def shoot(self):
        if not self.hidden:
            now = pg.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                if self.power == 1:
                    laser = Laser(self.rect.centerx, self.rect.top)
                    all_sprites.add(laser)
                    lasers.add(laser)
                if self.power >= 2:
                    laser1 = Laser(self.rect.left, self.rect.centery)
                    laser2 = Laser(self.rect.right, self.rect.centery)
                    all_sprites.add(laser1)
                    all_sprites.add(laser2)
                    lasers.add(laser1)
                    lasers.add(laser2)

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


class Powerup(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'bolt'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 7

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


def load_data():
    dir = path.dirname(__file__)
    try:
        with open(path.join(dir, HS_FILE), 'r') as f:
            highscore = int(f.read())
    except:
        with open(path.join(dir, HS_FILE), 'w') as f:
            highscore = 0
    return highscore


def show_go_screen(svalue, hvalue):
    score = svalue
    highscore = hvalue
    dir = path.dirname(__file__)
    screen.blit(background_start, (0, 0))
    draw_text(screen, "CITY DEFENCE!", 64, WIDTH / 2, HEIGHT / 3)
    draw_text(screen, "Press any key to begin", 32, WIDTH / 2, HEIGHT / 7 * 3)
    draw_text(screen, "(Arrow keys to move, Space to fire)", 18, WIDTH / 2, HEIGHT / 8 * 4 - 20)
    if score > highscore:
        highscore = score
        with open(path.join(dir, HS_FILE), 'r+') as f:
            f.write(str(score))
    draw_text(screen, "High Score: " + str(highscore), 24, WIDTH / 2, 15)

    pg.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                waiting = False


powerup_images = {}
powerup_images['shield'] = pg.image.load(path.join(image_dir, 'shield_gold.png')).convert()
powerup_images['bolt'] = pg.image.load(path.join(image_dir, 'bolt_gold.png')).convert()

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

ground_scroll = -(background.get_height() / 2)
scroll_speed = 2

game_over = True
running = True

while running:

    clock.tick(FPS)

    if game_over:
        highscore = load_data()
        show_go_screen(score, highscore)
        game_over = False
        all_sprites = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        enemies = pg.sprite.Group()
        for i in range(5):
            add_enemy()
        lasers = pg.sprite.Group()
        powerups = pg.sprite.Group()

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
        if random.random() > 0.95:
            pow = Powerup(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        add_enemy()

    hits = pg.sprite.spritecollide(player, enemies, True, pg.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'small')
        all_sprites.add(expl)
        add_enemy()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'large')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pg.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += 10
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'bolt':
            player.powerup()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.blit(background, (0, ground_scroll))
    ground_scroll += scroll_speed
    if ground_scroll > 0:
        ground_scroll = -(background.get_height() / 2)
    all_sprites.draw(screen)

    draw_lives(screen, WIDTH - 100, 5, player.lives, heart_mini_img)
    draw_text(screen, str(score), 36, WIDTH / 2, 5)
    draw_shield_bar(screen, 5, 10, player.shield)

    pg.display.update()

pg.quit()
