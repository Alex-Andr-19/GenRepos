import pygame as pg
from random import randint as rand
from lib_func import clamp
from settings import *

class Food(pg.sprite.Sprite):
    def __init__(self, color=(0, 255, 0)):
        super().__init__()
        self.image = pg.Surface([WF, HF])
        self.rect = self.image.get_rect()
        self.rect.x = rand(0, SCR_W - WCR)
        self.rect.y = rand(0, SCR_H - HCR)

        self.image.fill(color)
        self.color = color

    def type(self):
        return "Food"

    # функция угасания
    def fading(self):
        self.image.fill((clamp(self.color[0] - STEP_FAD), clamp(self.color[1] + STEP_FAD), 0))
        self.color = (clamp(self.color[0] - STEP_FAD), clamp(self.color[1] + STEP_FAD), 0)
