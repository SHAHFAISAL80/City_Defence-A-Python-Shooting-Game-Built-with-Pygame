import pygame as pg
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

background = pg.image.load(path.join(image_dir, r"C:\Users\Al Shahbaz\Videos\new projects\City_Defence-main\image\urban_long.png")).convert()

running = True

while running:

    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        screen.blit(background, (0, 0))

        pg.display.update()

pg.quit()
