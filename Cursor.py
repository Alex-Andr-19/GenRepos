import pygame as pg
from lib_func import clamp
from settings import Set_W

class Cursor(pg.sprite.Sprite):
    def __init__(self, x, y, st=0):
        super().__init__()
        self.x = x
        self.y = y
        self.percent = st
        self.focus = 0
        self.image = pg.Surface([Set_W - 20, 25])
        self.image.fill((210, 210, 210))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        pg.draw.line(self.image, (0, 0, 130), (0, 13), (Set_W - 20, 13))
        pg.draw.rect(self.image, (0, 0, 0), (int(st * (Set_W - 20)), 0, 15, 25))
        pg.draw.circle(self.image,
                       (255, 255, 255),
                       (clamp(int(st * (Set_W - 20)), Set_W - 27) + 7, 13),
                       3)

    def redraw(self, cords):
        self.percent = clamp(cords[0] / (Set_W - 20), 1)
        self.image = pg.Surface([Set_W - 20, 25])
        self.image.fill((210, 210, 210))
        pg.draw.line(self.image, (0, 0, 130), (0, 13), (Set_W - 20, 13))
        pg.draw.rect(self.image, (0, 0, 0), (clamp(cords[0] - 17, Set_W - 37), 0, 15, 25))
        if self.focus:
            pg.draw.circle(self.image,
                           (255, 255, 255),
                           (clamp(int(self.percent * (Set_W - 20)) - 7, Set_W - 27) - 2, 13),
                           3)

    def type(self):
        return "Cursor"
