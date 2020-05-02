from math import sqrt
from settings import Set_W
import pygame as pg

# необходимые математические функции
def distance_s(a, b):
    return sqrt((a.rect.x - b.rect.x)**2 + (a.rect.y - b.rect.y)**2)
def distance_c(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
'''
# функция вычисления угла от спрайта до точки
def angle_to(body, cords):
    gip = distance_c(body.rect.x, body.rect.y, cords[0], cords[1])
    kat = fabs(body.rect.y - cords[1])
    sin_a = kat / gip
    a = asin(sin_a)
    if body.rect.x <= cords[0]:
        a = pi - a
    if body.rect.y >= cords[1]:
        a = -a
    return a
'''

def clamp(a, max=255, min=0):
    if a >= max:
        return max
    if a < min:
        return min
    return a

def cycle(a, max, min):
    res = a
    if a > max:
        res = min
    elif a < min:
        res = max
    return res

def exist_in(pos, rect):
    if rect.x <= pos[0] <= rect.x + rect.w and rect.y <= pos[1] <= rect.y + rect.h:
        return True
    return False

def create_sprite(x, y, w, h, color=(0, 0, 0)):
    sprite = pg.sprite.Sprite()
    sprite.image = pg.Surface((w, h))
    sprite.image.fill(color)
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = x
    sprite.rect.y = y

    return sprite

# функция нахождения ближайшей и важнейшей цели
# Приоритеты:
#               1. Живая особь
#               2. Мёртвая особь
#               3. Еда
def fn_nrst_trg(crt, crt_mas, fd_mas, crt_gr, dead_gr, fd_gr, without=[]):
    index = 0
    min_dis = 10000

    if len(crt_gr) - len(dead_gr) > len(fd_gr):
        for i in range(len(fd_mas)):
            if min_dis > distance_s(crt.body, fd_mas[i]) and fd_mas[i] in fd_gr:
                min_dis = distance_s(crt.body, fd_mas[i])
                index = i
    else:
        for i in range(len(fd_mas)):
            if min_dis > distance_s(crt.body, fd_mas[i]) and fd_mas[i] in fd_gr and i not in without:
                min_dis = distance_s(crt.body, fd_mas[i])
                index = i

    for i in range(len(crt_mas)):
        fam = crt.child_name == crt_mas[i].name or crt.parent_name == crt_mas[i].name
        if min_dis > distance_s(crt.body, crt_mas[i].body) and crt_mas[i].body in dead_gr:
            min_dis = distance_s(crt.body, crt_mas[i].body)
            index = i + len(fd_mas)
        if min_dis > distance_s(crt.body, crt_mas[i].body) and \
                crt_mas[i].weight + 10 < crt.weight and \
                crt_mas[i].energy and not fam:
            min_dis = distance_s(crt.body, crt_mas[i].body)
            index = i + len(fd_mas)
    return index

def redraw_cursors(focus, count_crt, curs_mas):
    if focus == count_crt:
        curs_mas[0].focus = 1
        curs_mas[1].focus = 0
        curs_mas[2].focus = 0
        #
        curs_mas[1].redraw((curs_mas[1].percent * (Set_W - 20), 0))
        curs_mas[2].redraw((curs_mas[2].percent * (Set_W - 20), 0))

    elif focus == count_crt + 1:
        curs_mas[0].focus = 0
        curs_mas[1].focus = 1
        curs_mas[2].focus = 0
        curs_mas[0].redraw((curs_mas[0].percent * (Set_W - 20), 0))
        #
        curs_mas[2].redraw((curs_mas[2].percent * (Set_W - 20), 0))

    elif focus == count_crt + 2:
        curs_mas[0].focus = 0
        curs_mas[1].focus = 0
        curs_mas[2].focus = 1
        curs_mas[0].redraw((curs_mas[0].percent * (Set_W - 20), 0))
        curs_mas[1].redraw((curs_mas[1].percent * (Set_W - 20), 0))
        #

    else:
        curs_mas[0].focus = 0
        curs_mas[1].focus = 0
        curs_mas[2].focus = 0
        curs_mas[0].redraw((curs_mas[0].percent * (Set_W - 20), 0))
        curs_mas[1].redraw((curs_mas[1].percent * (Set_W - 20), 0))
        curs_mas[2].redraw((curs_mas[2].percent * (Set_W - 20), 0))

'''
# функция вращения по окружности по часовой стрелке на целый круг со стартового угла
def circ_on(crt, start_w=0, clock=1):
    if clock:
        angle_tmp = crt.angle + pi / 90 + start_w
    else:
        angle_tmp = pi - (crt.angle + pi / 90) + start_w

    crt.body.rect.x = crt.center[0] + crt.radius * cos(angle_tmp)
    crt.body.rect.y = crt.center[1] - crt.radius * sin(angle_tmp)
    crt.sens_circ.rect.x = crt.body.rect.x - crt.sens + crt.w//2
    crt.sens_circ.rect.y = crt.body.rect.y - crt.sens + crt.h//2
    crt.angle += pi / 90

    if crt.angle >= 2 * pi:
        crt.angle = 0
'''
