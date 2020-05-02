import pygame as pg
from math import cos, sin, acos, pi, fabs, ceil
from random import randint as rand
from lib_func import clamp, create_sprite

class Gen(pg.sprite.Group):
    def __init__(self, x, y, length, diam=50, side=1):
        super().__init__()

        self.x = x
        self.y = y
        self.side = side
        self.length = length
        self.diam = diam
        self.angle = acos(clamp(length / diam * side, 1, -1))

        self.color1 = (192 + 63 * sin(self.angle), 0, 0)
        self.color2 = (length / diam * 200, length / diam * 200, length / diam * 200)
        self.color3 = (0, 192 - 63 * sin(self.angle), 0)

        self.gen1 = create_sprite(0, y, 10, 10, self.color1)
        self.link = create_sprite(x + 10, y + 3, length, 4, self.color2)
        self.gen2 = create_sprite(0, y, 10, 10, self.color3)

        if side == 1:
            self.gen1.rect.x = x
            self.gen2.rect.x = x + 10 + length
        else:
            self.gen1.rect.x = x + 10 + length
            self.gen2.rect.x = x
        self.link.rect.x = x + 10
        self.link.rect.y = y + 3

        self.add([self.link, self.gen1, self.gen2])
        self.mem = [self.gen1, self.link, self.gen2]

    def turning(self):
        self.angle += pi / 180
        if -pi / 2 <= self.angle < pi / 2:
            self.side = 1
        elif pi / 2 < self.angle <= 3 * pi / 2:
            self.side = -1
        else:
            self.angle = -pi / 2

        self.x += (self.length - fabs(self.diam * cos(self.angle))) / 2
        self.length = fabs(self.diam * cos(self.angle))
        self.color1 = (192 + 63 * sin(self.angle), 0, self.color1[2])
        c = self.length / self.diam * 200
        self.color2 = (c, c, c)
        self.color3 = (0, 192 - 63 * sin(self.angle), self.color3[2])

        '''self.gen1 = create_sprite(0, self.y, 10, 10, self.color1)
        self.gen2 = create_sprite(0, self.y, 10, 10, self.color3)
        self.link = create_sprite(self.x + 10, self.y + 3, self.length, 4, self.color2)'''

        self.gen1.image = pg.Surface([10, 10])
        self.link.image = pg.Surface([self.length, 4])
        self.gen2.image = pg.Surface([10, 10])

        self.gen1.image.fill(self.color1)
        self.link.image.fill(self.color2)
        self.gen2.image.fill(self.color3)

        self.gen1.rect = self.gen1.image.get_rect()
        self.link.rect = self.link.image.get_rect()
        self.gen2.rect = self.gen1.image.get_rect()

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

    def redraw(self):
        gen = rand(0, 2)
        success = 0
        if gen and not self.color1[2]:
            self.color1 = (192 + int(63 * sin(self.angle)), self.color1[1], rand(180, 255))
            success = 1
        elif not self.color3[2]:
            self.color3 = (self.color3[0], 192 - int(63 * sin(self.angle)), rand(180, 255))
            success = 1
        return success

    def normal(self):
        self.color1 = (192 + 63 * sin(self.angle), 0, 0)
        self.color3 = (0, 192 - 63 * sin(self.angle), 0)

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

    def redraw(self, crt):
        # скорость
        if crt.speed > 1:
            success = self.gens[rand(0, 2)].redraw()
            while not success:
                success = self.gens[rand(0, 2)].redraw()

        # рождение
        if crt.birth_enr < 5:
            success = self.gens[rand(3, 5)].redraw()
            while not success:
                success = self.gens[rand(3, 5)].redraw()

        # ширина
        if crt.w != 8:
            success = self.gens[rand(6, 8)].redraw()
            while not success:
                success = self.gens[rand(6, 8)].redraw()

        # высота
        if crt.h != 8:
            success = self.gens[rand(9, 11)].redraw()
            while not success:
                success = self.gens[rand(9, 11)].redraw()

        # область вилимости
        if crt.sens != 30:
            success = self.gens[rand(12, 14)].redraw()
            while not success:
                success = self.gens[rand(12, 14)].redraw()

    def normal(self):
        for i in range(len(self.gens)):
            self.gens[i].normal()