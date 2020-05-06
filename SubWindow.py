import pygame as pg
from lib_func import create_sprite
from settings import F1, F2
from Button import Button, Radio_Button
from Statistics import Statistic

class subwindow(pg.sprite.Group):
    def __init__(self, x, y, w, h, stat=Statistic()):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.bg = create_sprite(x, y, w, h, (220, 220, 220))
        self.hr_g = create_sprite(x + 10, y + h // 2 - 10, w - 20, 2, (150, 150, 150))
        self.hr_v = create_sprite(x + w // 2, y + 10, 2, h // 2 - 30, (150, 150, 150))
        self.r_hr1 = create_sprite(x + 145, y + 40, 180, 2, (255, 0, 0))
        self.r_hr2 = create_sprite(x + w // 2 + 132, y + 40, 180, 2, (255, 0, 0))
        self.r_hr3 = create_sprite(x + w // 2 - 125, y + h // 2 + 40, 275, 2, (255, 0, 0))

        per_day_str = F1.render("Per Day", 1, (0, 0, 0))
        digits_str = F1.render("Digits", 1, (0, 0, 0))
        adv_set = F1.render("Advanced Settings", 1, (0, 0, 0))

        oldest_alive_breed_str = F2.render("The Oldest Alive Breed - " + str(stat.oldest_alive_breed), 1, (0, 0, 0))
        youngest_alive_breed_str = F2.render("The Youngest Alive Breed - " + str(stat.youngest_alive_breed), 1, (0, 0, 0))
        average_day_str = F2.render("Averange Day - " + str(stat.avarage_day), 1, (0, 0, 0))
        oldest_creature_str = F2.render("The Oldest Creature - " + str(stat.oldest_creature), 1, (0, 0, 0))
        mut_str = F2.render("Mutation", 1, (0, 0, 0))

        self.add(self.bg)
        self.add(self.hr_g)
        self.add(self.hr_v)
        self.add(self.r_hr1)
        self.add(self.r_hr2)
        self.add(self.r_hr3)

        self.bg.image.blit(per_day_str, (190, 10))
        self.bg.image.blit(digits_str, (190 + w // 2, 10))
        self.bg.image.blit(adv_set, (w // 2 - 100, h // 2 + 10))

        # Статистичесие данные
        self.buttons = []
        self.buttons.append(Button(x + 10, y + 50, " Count of Birth", 143, 25))
        self.buttons.append(Button(x + 10, y + 80, " Count of Alive", 143, 25))
        self.buttons.append(Button(x + 10, y + 110, " Count of Dead", 143, 25))
        self.buttons.append(Button(x + 10, y + 140, " Count of Mutation", 178, 25))

        # Кнопки настроек
        self.buttons.append(Radio_Button(x + 40, y + h // 2 + 75, " Speed", 157, 25))
        self.buttons.append(Radio_Button(x + 40, y + h // 2 + 100, " Reproduction", 157, 25))
        self.buttons.append(Radio_Button(x + 40, y + h // 2 + 125, " Width", 157, 25))
        self.buttons.append(Radio_Button(x + 40, y + h // 2 + 150, " Height", 157, 25))
        self.buttons.append(Radio_Button(x + 40, y + h // 2 + 175, " Sense", 157, 25))

        self.add(self.buttons)

        # Численные данные
        self.bg.image.blit(oldest_alive_breed_str, (10 + w // 2, 50))
        self.bg.image.blit(youngest_alive_breed_str, (10 + w // 2, 75))
        self.bg.image.blit(average_day_str, (10 + w // 2, 100))
        self.bg.image.blit(oldest_creature_str, (10 + w // 2, 125))

        # Расг=ширенные настройки
        self.bg.image.blit(mut_str, (w // 16 + 22, y + h // 2 + 25))

    def redraw(self, oab, yab, avd, oc):
        self.bg.image = pg.Surface([self.w, self.h])
        self.bg.image.fill((220, 220, 220))

        per_day_str = F1.render("Per Day", 1, (0, 0, 0))
        digits_str = F1.render("Digits", 1, (0, 0, 0))
        adv_set = F1.render("Advanced Settings", 1, (0, 0, 0))
        mut_str = F2.render("Mutation", 1, (0, 0, 0))

        self.bg.image.blit(per_day_str, (190, 10))
        self.bg.image.blit(digits_str, (190 + self.w // 2, 10))
        self.bg.image.blit(adv_set, (self.w // 2 - 100, self.h // 2 + 10))

        oldest_alive_breed_str = F2.render("The Oldest Alive Breed - " + str(oab), 1, (0, 0, 0))
        youngest_alive_breed_str = F2.render("The Youngest Alive Breed - " + str(yab), 1, (0, 0, 0))
        average_day_str = F2.render("Averange Day - " + str(avd), 1, (0, 0, 0))
        oldest_creature_str = F2.render("The Oldest Creature - " + str(oc), 1, (0, 0, 0))

        # Численные данные
        self.bg.image.blit(oldest_alive_breed_str, (10 + self.w // 2, 50))
        self.bg.image.blit(youngest_alive_breed_str, (10 + self.w // 2, 75))
        self.bg.image.blit(average_day_str, (10 + self.w // 2, 100))
        self.bg.image.blit(oldest_creature_str, (10 + self.w // 2, 125))

        # Расширенные настройки
        self.bg.image.blit(mut_str, (self.w // 16 + 22, self.y + self.h // 2 + 25))

