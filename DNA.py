import pygame as pg
from math import cos, sin, acos, pi, fabs, ceil
from lib_func import clamp

class Gen(pg.sprite.Group):
    def __init__(self, x, y, length, diam=50, side=1):
        super().__init__()

        self.x = x
        self.y = y
        self.side = side
        self.length = length
        self.diam = diam
        self.angle = acos(clamp(length / diam * side, 1 ,-1))

        self.gen1 = pg.sprite.Sprite()
        self.gen2 = pg.sprite.Sprite()
        self.link = pg.sprite.Sprite()

        self.gen1.image = pg.Surface([10, 10])
        self.gen2.image = pg.Surface([10, 10])
        self.link.image = pg.Surface([length, 4])

        self.gen1.image.fill((192 + 63 * sin(self.angle), 0, 0))
        self.gen2.image.fill((0, 192 - 63 * sin(self.angle), 0))
        self.link.image.fill((length / diam * 200, length / diam * 200, length / diam * 200))

        self.gen1.rect = self.gen1.image.get_rect()
        self.gen2.rect = self.gen1.image.get_rect()
        self.link.rect = self.link.image.get_rect()

        if side == 1:
            self.gen1.rect.x = x
            self.gen2.rect.x = x + 10 + length
        else:
            self.gen1.rect.x = x + 10 + length
            self.gen2.rect.x = x
        self.gen1.rect.y = y
        self.gen2.rect.y = y
        self.link.rect.x = x + 10
        self.link.rect.y = y + 3

        self.add([self.link, self.gen1, self.gen2])
        self.mem = [self.gen1, self.link, self.gen2]



    def turning(self, right=1):
        self.angle += pi / 180
        if -pi / 2 <= self.angle < pi / 2:
            self.side = 1
        elif pi / 2 < self.angle <= 3 * pi / 2:
            self.side = -1
        else:
            self.angle = -pi / 2

        self.x += (self.length - fabs(self.diam * cos(self.angle))) / 2
        self.length = fabs(self.diam * cos(self.angle))

        self.gen1.image = pg.Surface([10, 10])
        self.gen2.image = pg.Surface([10, 10])
        self.link.image = pg.Surface([self.length, 4])

        self.gen1.image.fill((192 + 63 * sin(self.angle), 0, 0))
        self.gen2.image.fill((0, 192 - 63 * sin(self.angle), 0))
        self.link.image.fill((self.length / self.diam * 200, self.length / self.diam * 200, self.length / self.diam * 200))

        self.gen1.rect = self.gen1.image.get_rect()
        self.gen2.rect = self.gen1.image.get_rect()
        self.link.rect = self.link.image.get_rect()

        if self.side == 1:
            self.gen1.rect.x = self.x
            self.gen2.rect.x = self.x + 10 + self.length
        else:
            self.gen1.rect.x = self.x + 10 + self.length
            self.gen2.rect.x = self.x
        self.gen1.rect.y = self.y
        self.gen2.rect.y = self.y
        self.link.rect.x = self.x + 10
        self.link.rect.y = self.y + 3

class DNA(pg.sprite.Group):
    def __init__(self, count, x, y):
        super().__init__()
        diam = ceil(count / 11 * 50)
        self.gens = []
        for i in range(count):
            if i < ceil(count / 2):
                self.gens.append(Gen(x + i * 5, y + i * 15, fabs(diam - i * 10), diam))
            else:
                self.gens.append(Gen(x + (count - i - 1) * 5, y + i * 15, fabs(diam - i * 10), diam, -1))

    def turning(self):
        for i in range(len(self.gens)):
            self.gens[i].turning()
            self.add(self.gens[i])