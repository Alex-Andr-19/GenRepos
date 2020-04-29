import pygame as pg

class subwindow(pg.sprite.Group):
    def __init__(self, x, y, w, h):
        super().__init__()
        bg = pg.sprite.Sprite()
        bg.image = pg.Surface((w, h))
        bg.image.fill((220, 220, 220))
        bg.rect = bg.image.get_rect()
        bg.rect.x = x
        bg.rect.y = y
        self.bg = bg

        self.add(self.bg)