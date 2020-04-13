import pygame as pg
from random import randint as rand
from math import fabs, cos, sin, pi, ceil
from lib_func import clamp
from settings import *


class Creature:
    def __init__(self, w, h, sens=70, start_cords=(0, 0), breed=1, color1=(0, 0, 255), color2=(87, 87, 87),
                 fon_c=(0, 0, 0)):
        # внешние характеристики
        self.w = w
        self.h = h
        self.color1 = color1
        self.color2 = color2
        self.fon_c = fon_c
        self.breed = breed
        self.days = 1
        self.focus = 0

        # внутренние характеристики
        self.energy = 2.5
        self.speed = 1
        self.sens = sens
        self.birth_enr = 5
        self.weight = self.w * self.h
        self.name = rand(1, 1000001)
        self.parent_name = 0
        self.child_name = 0

        # отрисовка особи
        self.terretory = pg.sprite.Group()

        self.body = pg.sprite.Sprite()
        self.body.image = pg.Surface([w, h])
        self.body.rect = self.body.image.get_rect()
        if start_cords[0] or start_cords[1]:
            self.body.rect.x = start_cords[0]
            self.body.rect.y = start_cords[1]
        else:
            self.body.rect.x = rand(0, SCR_W - w)
            self.body.rect.y = rand(0, SCR_H - h)
        self.body.image.fill(color1)

        self.sens_circ = pg.sprite.Sprite()
        self.sens_circ.image = pg.Surface([sens * 2, sens * 2])
        self.sens_circ.rect = self.sens_circ.image.get_rect()
        self.sens_circ.rect.x = self.body.rect.x - sens + int(w / 2) - 1
        self.sens_circ.rect.y = self.body.rect.y - sens + int(h / 2) - 1
        self.sens_circ.image.fill(fon_c)
        self.sens_circ.image.set_colorkey(fon_c)

        self.terretory.add(self.sens_circ)
        self.terretory.add(self.body)

        pg.draw.ellipse(self.sens_circ.image,
                        self.color2,
                        self.sens_circ.image.get_rect())

        self.f = pg.font.Font(None, 15)
        self.brd_info = self.f.render(str(self.breed), 0, (255, 255, 255))
        self.sens_circ.image.blit(self.brd_info, (18, 12))

        # дополнительная информация
        self.enrg_info = self.f.render(str(self.energy), 0, (255, 255, 255))
        # self.days_info = self.f.render(str(self.breed), 0, (255, 255, 255))
        # self.speed_info = self.f.render(str(self.speed), 0, (255, 255, 255))
        # self.birth_info = self.f.render(str(self.birth_enr), 0, (255, 255, 255))

    def type(self):
        return "Creature"

    # функция возвращает 1, если особь не потратила всю энергию
    #                    0, иначе
    def go_to_target(self, targ):
        x_t = targ.rect.x
        y_t = targ.rect.y

        # высчитывание новых координат
        for i in range(self.speed):
            if fabs(self.body.rect.x - x_t) > fabs(self.body.rect.y - y_t):
                if self.body.rect.x > x_t:
                    self.body.rect.x -= 1
                    self.sens_circ.rect.x -= 1
                else:
                    self.body.rect.x += 1
                    self.sens_circ.rect.x += 1
            else:
                if self.body.rect.y > y_t:
                    self.body.rect.y -= 1
                    self.sens_circ.rect.y -= 1
                else:
                    self.body.rect.y += 1
                    self.sens_circ.rect.y += 1

            # затрата на передвижение
            self.energy = clamp(self.energy - 0.006 * self.weight / 64)

        # расчёт цвета в зависимости от количества энергии
        r = clamp(int(self.color1[0] * self.energy))
        if self.energy > 5.5:
            r = clamp(int((self.energy - 5.5) * 255))
        g = clamp(int(self.color1[1] * self.energy))
        if self.energy > 8.5:
            g = clamp(int((self.energy - 8.5) * 255))
        b = clamp(int(self.color1[2] * self.energy / 5.5))

        # обновление размеров поверхности при мутации у особи гена размера тела
        if self.body.rect.w != self.w:
            self.body.image = pg.Surface([self.w, self.h])
            self.body.rect.w = self.w
            self.body.rect.x += (self.w - self.body.rect.w) // 2
            self.weight = self.w * self.h
        if self.body.rect.h != self.h:
            self.body.image = pg.Surface([self.w, self.h])
            self.body.rect.h = self.h
            self.body.rect.y -= (self.h - self.body.rect.h) // 2
            self.weight = self.w * self.h

        # отрисовка особи с обновлёнными координатами
        self.sens_circ.image = pg.Surface([self.sens * 2 + self.w - 5, self.sens * 2 + self.h - 5])
        self.sens_circ.image.fill((0, 0, 0))
        self.sens_circ.image.set_colorkey((0, 0, 0))
        pg.draw.ellipse(self.sens_circ.image,
                        self.color2,
                        self.sens_circ.image.get_rect())
        if self.focus:
            pg.draw.rect(self.sens_circ.image,
                         (255, 215, 0),
                         (self.sens - self.body.rect.w // 2,
                          self.sens - self.body.rect.h // 2,
                          self.body.rect.w + 2,
                          self.body.rect.h + 2))
        self.body.image.fill((r, g, b))

        self.sens_circ.image.blit(self.brd_info, (18, 12 + 3 * HCR))

        # дополнительная информация
        self.enrg_info = self.f.render(str(self.energy)[:5], 1, (255, 255, 255))
        # self.days_info = self.f.render(str(self.days), 1, (255, 255, 255))
        # self.speed_info = self.f.render(str(self.speed), 1, (255, 255, 255))
        # self.birth_info = self.f.render(str(self.birth_enr), 1, (255, 255, 255))
        self.sens_circ.image.blit(self.enrg_info, (18, 12))
        # self.sens_circ.image.blit(self.days_info, (36, 12 + 3 * HCR))
        # self.sens_circ.image.blit(self.speed_info, (11, 25))
        # self.sens_circ.image.blit(self.birth_info, (11 + 4*WCR, 25))

        if not self.energy:
            self.dead()
            return 0
        return 1

    # своеобразныйконструктор копирования,
    # предназначенный для копирования должным образом всех своих характеристик потомку
    # + обновление своих внутренних характеристик
    def copy_to(self, tmp):
        tmp.color2 = self.color2
        tmp.w = self.w
        tmp.h = self.h
        tmp.body.rect.w = self.w
        tmp.body.rect.h = self.h
        tmp.body.image = pg.Surface((self.w, self.h))
        tmp.energy = self.birth_enr / 1.5
        tmp.birth_enr = self.birth_enr
        tmp.speed = self.speed
        tmp.weight = self.weight
        tmp.parent_name = self.name
        self.child_name = tmp.name

    def dead(self):
        self.color2 = (150, 150, 150)
        pg.draw.ellipse(self.sens_circ.image,
                        self.color2,
                        self.sens_circ.image.get_rect())
        self.sens_circ.image.blit(self.brd_info, (18, 12 + 3 * HCR))

    def expantion(self, sens):
        self.sens = sens
        self.sens_circ.rect.x = self.body.rect.x - sens + ceil(self.w / 2) - 1
        self.sens_circ.rect.y = self.body.rect.y - sens + ceil(self.h / 2) - 1

    def type(self):
        return "Creature"

    '''def just_walk(self, start_w):
        for i in range(self.speed):
            self.angle += pi / 90
            self.body.rect.x = self.center[0] + self.sens * cos(self.angle)
            self.body.rect.y = self.center[1] - self.sens * sin(self.angle)
            self.sens_circ.rect.x = self.body.rect.x - self.sens + self.w // 2
            self.sens_circ.rect.y = self.body.rect.y - self.sens + self.h // 2'''

