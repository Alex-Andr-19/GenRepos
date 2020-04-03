import pygame as pg
from random import randint as rand
from lib_func import clamp
from settings import *

class Food(pg.sprite.Sprite):
    def __init__(self, color=(0, 255, 0)):
        super().__init__()
        # self.food = pg.sprite.Sprite()
        self.image = pg.Surface([WF, HF])
        self.rect = self.image.get_rect()
        self.rect.x = rand(0, SCR_W - WCR)
        self.rect.y = rand(0, SCR_H - HCR)

        self.image.fill(color)
        self.color = color

    def type(self):
        return "Food"

    def fading(self):
        self.image.fill((clamp(self.color[0] - 17), clamp(self.color[1] + 17), 0))
        self.color = (clamp(self.color[0] - 17), clamp(self.color[1] + 17), 0)
