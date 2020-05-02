import pygame as pg
from lib_func import create_sprite
from settings import F1, F2
from Button import Button

class subwindow(pg.sprite.Group):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.bg = create_sprite(x, y, w, h, (220, 220, 220))
        self.hr_g = create_sprite(x + 10, y + h // 2 - 10, w - 20, 2, (150, 150, 150))
        self.hr_v = create_sprite(x + w // 2, y + 10, 2, h // 2 - 30, (150, 150, 150))
        self.r_hr1 = create_sprite(x + 145, y + 40, 180, 2, (255, 0, 0))
        self.r_hr2 = create_sprite(x + w // 2 + 132, y + 40, 180, 2, (255, 0, 0))
        self.r_hr3 = create_sprite(x + w // 2 - 125, y + h // 2 + 40, 275, 2, (255, 0, 0))

        per_day_str = F1.render("Per Day", 1, (0, 0, 0))
        digits_str = F1.render("Digits", 1, (0, 0, 0))
        adv_set = F1.render("Advanced Settings", 1, (0, 0, 0))

        oldest_alive_breed = F2.render("The Oldest Alive Breed - 10", 1, (0, 0, 0))
        youngest_alive_breed = F2.render("The Youngest Alive Breed - 10", 1, (0, 0, 0))
        average_day = F2.render("Averange Day - 10", 1, (0, 0, 0))
        oldest_creature = F2.render("The Oldest Creature - 10", 1, (0, 0, 0))
        domin_kind = F2.render("Dominant Kind:", 1, (0, 0, 0))

        v = F2.render("V - 10", 1, (0, 0, 0))
        birth = F2.render("Birth - 10", 1, (0, 0, 0))
        sens = F2.render("Sense - 10", 1, (0, 0, 0))
        w_ = F2.render("W - 10", 1, (0, 0, 0))
        h_ = F2.render("H - 10", 1, (0, 0, 0))

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
        self.buttons.append(Button(x + 10, y + 170, " Dom_Kind / Other", 178, 25))

        self.add(self.buttons)

        # Численные данные
        self.bg.image.blit(oldest_alive_breed, (10 + w // 2, 50))
        self.bg.image.blit(youngest_alive_breed, (10 + w // 2, 75))
        self.bg.image.blit(average_day, (10 + w // 2, 100))
        self.bg.image.blit(oldest_creature, (10 + w // 2, 125))

        self.bg.image.blit(domin_kind, (13 + w // 2 + w // 8, 175))
        self.bg.image.blit(v, (10 + w // 2, 200))
        self.bg.image.blit(birth, (70 + w // 2, 200))
        self.bg.image.blit(sens, (160 + w // 2, 200))
        self.bg.image.blit(w_, (270 + w // 2, 200))
        self.bg.image.blit(h_, (330 + w // 2, 200))


