import pygame as pg
from lib_func import clamp
from settings import Set_W

class Cursor(pg.sprite.Sprite):
    def __init__(self, x, y, st=0):
        super().__init__()
        self.x = x
        self.y = y
        self.percent = st
        self.image = pg.Surface([Set_W - 20, 25])
        self.image.fill((210, 210, 210))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pg.draw.line(self.image, (0, 0, 130), (0, 13), (Set_W - 20, 13))
        pg.draw.rect(self.image, (0, 0, 0), (int(st * (Set_W - 20)), 0, 15, 25))

    def redraw(self, cords):
        self.percent = cords[0] / (Set_W - 20)
        self.image = pg.Surface([Set_W - 20, 25])
        self.image.fill((210, 210, 210))
        pg.draw.line(self.image, (0, 0, 130), (0, 13), (Set_W - 20, 13))
        pg.draw.rect(self.image, (0, 0, 0), (clamp(cords[0] - 10, Set_W - 35), 0, 15, 25))
