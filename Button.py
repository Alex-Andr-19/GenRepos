import pygame as pg
pg.init()
f = pg.font.Font(None, 29)

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, text, w=30, h=30):
        super().__init__()
        self.color = (210, 210, 210)
        self.img = pg.Surface
        self.text = ""

        self.image = pg.Surface((w, h))
        self.image.fill(self.color)

        if "img" in text:
            img = pg.image.load(text)
            self.img = pg.transform.scale(img, (w, h))
            self.image.blit(self.img, (0, 0))
        else:
            self.text = f.render(text, 1, (0, 0, 0))
            self.image.blit(self.text, (100, 500))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.active = 0

    def focus(self):
        self.image.fill((255, 0, 0))
        pg.draw.rect(self.image, self.color,
                     (2, 2, self.rect.w - 4, self.rect.h - 4))
        if self.text == "":
            self.image.blit(self.img, (0, 0))
        else:
            self.image.blit(self.text, (2, 2))

    def unfocus(self):
        self.image.fill(self.color)
        if self.text == "":
            self.image.blit(self.img, (0, 0))
        else:
            self.image.blit(self.text, (2, 2))

    def redraw(self, photo):
        img = pg.image.load(photo)
        self.img = pg.transform.scale(img, (self.rect.w, self.rect.h))
        self.image.blit(self.img, (0, 0))

    def down(self):
        self.active = 1

    def up(self):
        self.active = 0

class Radio_Button(Button):
    def __init__(self, x, y, text, w=30, h=30):
        super().__init__(x, y, text, w, h)

        self.w = w
        self.h = h

        self.active = 1
        pg.draw.circle(self.image, (0, 180, 0), (w - 10, h // 2 + 1), 6)

    def focus(self):
        self.image.fill((255, 0, 0))
        pg.draw.rect(self.image, self.color,
                     (2, 2, self.rect.w - 4, self.rect.h - 4))
        if self.active:
            pg.draw.circle(self.image, (0, 180, 0), (self.w - 10, self.h // 2 + 1), 6)
        else:
            pg.draw.circle(self.image, (0, 0, 180), (self.w - 10, self.h // 2 + 1), 6)
        if self.text == "":
            self.image.blit(self.img, (0, 0))
        else:
            self.image.blit(self.text, (2, 2))

    def unfocus(self):
        self.image.fill(self.color)
        if self.active:
            pg.draw.circle(self.image, (0, 180, 0), (self.w - 10, self.h // 2 + 1), 6)
        else:
            pg.draw.circle(self.image, (0, 0, 180), (self.w - 10, self.h // 2 + 1), 6)
        if self.text == "":
            self.image.blit(self.img, (0, 0))
        else:
            self.image.blit(self.text, (2, 2))
