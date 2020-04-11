import pygame as pg

from Food import Food
from Creature import Creature
from Cursor import Cursor

from random import randint as rand
from lib_func import *
from settings import *

count_crt = COUNT_CRT
alive     = count_crt
days      = 1
brd_info  = ""
iterator  = 0

pg.init()

window = pg.display.set_mode((Win_W, Win_H))
screen = window.subsurface((Set_W, 0, SCR_W, SCR_H))
set_pan = window.subsurface((0, 0, Set_W, SCR_H))

run = 1

fd_gr    = pg.sprite.Group()
crtb_gr  = pg.sprite.Group()
crts_gr  = pg.sprite.Group()
deadb_gr = pg.sprite.Group()
deads_gr = pg.sprite.Group()
curs_gr  = pg.sprite.Group()

vis_gr   = []
crt_mas  = [Creature(WCR, HCR, SENS) for i in range(count_crt)]
fd_mas   = [Food() for i in range(COUNT_FD)]
curs_mas = [Cursor(10, 160 + 80 * i, [COUNT_FD / 2000, 0.9, 0][i]) for i in range(3)]

for i in range(count_crt):
    crtb_gr.add(crt_mas[i].body)
    crts_gr.add(crt_mas[i].sens_circ)

for i in range(COUNT_FD):
    fd_gr.add(fd_mas[i])

for i in range(3):
    curs_gr.add(curs_mas[i])

f = pg.font.Font(None, 36)
index = [fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr) for i in range(count_crt)]

# начало программы
while run:

    # вывод информации о ситуации
    l1 = f.render("Alive      - " + str(alive), 1, (0, 0, 0))
    l2 = f.render("Food      - " + str(int(len(fd_gr) / COUNT_FD * 100)) + "%", 1, (0, 0, 0))
    l3 = f.render("Days      - " + str(days), 1, (0, 0, 0))
    l4 = f.render("Food - " + str(COUNT_FD), 1, (0, 0, 0))
    l5 = f.render("Speed - " + str(int(curs_mas[1].percent * 100)) + "%", 1, (0, 0, 0))

    screen.fill((0, 0, 0))
    set_pan.fill((210, 210, 210))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0

    # отрисовка всех объектов
    crts_gr.draw(screen)
    fd_gr.draw(screen)
    crtb_gr.draw(screen)

    # затухание еды
    temp_time = pg.time.get_ticks()
    if (temp_time - START_TIME) % 10 == 0:
        for i in range(len(fd_mas)):
            if fd_mas[i].color[0]:
                fd_mas[i].fading()

    # появление новой еды
    if (temp_time - START_TIME) % (COUNT_FD // 5) == 0:
        for i in range(COUNT_FD):
            if fd_mas[i] not in fd_gr:
                fd_mas[i].rect.x = rand(WCR, SCR_W - WCR)
                fd_mas[i].rect.y = rand(HCR, SCR_H - HCR)
                fd_mas[i].image.fill((0, 255, 0))
                fd_mas[i].color  = (0, 255, 0)
                fd_gr.add(fd_mas[i])
                break

    # видит ли особь еду
    prev_len = 0
    for i in range(count_crt):
        vis_gr += pg.sprite.spritecollide(crt_mas[i].sens_circ, fd_gr, False)
        if index[i] == -1:
            while len(vis_gr) != prev_len:
                del vis_gr[-1]
        if len(vis_gr) - prev_len:
            for j in range(len(vis_gr) - prev_len):
                vis_gr[j + prev_len].image.fill((255, 0, 0))
            prev_len = len(vis_gr)

    # окраска еды которую видит особь
    for i in range(len(vis_gr)):
        vis_gr[i].color = (255, 0, 0)

    # передвижение каждой особи
    for i in range(count_crt):
        tmp = 1

# ниже функция clamp используется в качестве костыля, потому что без неё почему-то происходит 'index out of range'

        if 0 <= index[i] < COUNT_FD:
            # к еде
            if (crt_mas[i].body.rect.x != fd_mas[index[i]].rect.x or
                crt_mas[i].body.rect.y != fd_mas[index[i]].rect.y) and \
                index[i] != -1:

                tmp = crt_mas[i].go_to_target(fd_mas[index[i]])
        elif 0 <= index[i]:
            # к особи
            if (crt_mas[i].body.rect.x != crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].body.rect.x or
                crt_mas[i].body.rect.y != crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].body.rect.y) and \
                index[i] != -1:

                tmp = crt_mas[i].go_to_target(crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body)

        # регестрация гибели
        if tmp == 0:
            index[i] = -1
            deadb_gr.add(crt_mas[i].body)
            deads_gr.add(crt_mas[i].sens_circ)
            crt_mas[i].color2 = (60, 60, 60)

    # обработка энергии
    for i in range(count_crt):
        if crt_mas[i].sens_circ.rect.x <= pg.mouse.get_pos()[0] - Set_W <= crt_mas[i].sens_circ.rect.x + crt_mas[i].sens_circ.rect.w and \
                crt_mas[i].sens_circ.rect.y <= pg.mouse.get_pos()[1] <= crt_mas[i].sens_circ.rect.y + crt_mas[
            i].sens_circ.rect.h and pg.mouse.get_pressed()[0]:
            print(i)

        hit_gr = pg.sprite.spritecollide(crt_mas[i].body, fd_gr, True)
        # съела ли особь еду
        if len(hit_gr):
            for j in range(len(hit_gr)):
                crt_mas[i].energy += FD_EN
        # съела ли особь другую особь
        elif index[i] >= 0:

            # живую
            hit_gr = pg.sprite.spritecollide(crt_mas[i].body, crtb_gr, False)
            if len(hit_gr) > 1 and \
                    index[i] >= COUNT_FD and \
                    crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].energy and \
                    crt_mas[i].weight - 10 > crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].weight:
                crt_mas[index[i] - COUNT_FD].body.kill()
                crt_mas[index[i] - COUNT_FD].sens_circ.kill()
                crt_mas[i].energy += 0.5 * crt_mas[index[i] - COUNT_FD].weight / 64
                crt_mas[index[i] - COUNT_FD].energy = 0
                index[index[i] - COUNT_FD] = -1

            # мёртвую
            hit_gr = pg.sprite.spritecollide(crt_mas[i].body, deadb_gr, True)
            if len(hit_gr):
                while crt_mas[iterator].body not in hit_gr:
                    iterator += 1
                crt_mas[i].energy += 0.5 * crt_mas[iterator].weight / 64
                crt_mas[iterator].body.kill()
                crt_mas[iterator].sens_circ.kill()
                iterator     = 0

        # рождение
        if crt_mas[i].energy > 9.8:
            for j in range(int(9.8 // crt_mas[i].birth_enr)):
                # вычисление координат дочерней особи
                cords = (crt_mas[i].body.rect.x + WCR, crt_mas[i].body.rect.y + HCR)

                # факт рождения
                crt_mas.append(Creature(WCR, HCR, SENS, cords, crt_mas[i].breed+1))
                crt_mas[i].copy_to(crt_mas[-1])

                # мутация
                # скорость
                chance = rand(0, 100)
                if 90 <= chance < 95 and crt_mas[-1].speed != clamp(crt_mas[-1].speed - 1, 5, 1):
                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] - 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed - 1, 5, 1)
                elif chance >= 95 and crt_mas[-1].speed != clamp(crt_mas[-1].speed + 1, 5, 1):
                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] + 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed + 1, 5, 1)

                # размножение
                chance = rand(0, 100)
                if 90 <= chance < 95 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr + 1, 5, 1):
                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] - 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr + 1, 5, 2)
                elif chance >= 95 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr - 1, 5, 1):
                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] + 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr - 1, 5, 2)

                # размер: ширина
                chance = rand(0, 100)
                if 90 <= chance < 95:
                    crt_mas[-1].w += 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 95 <= chance:
                    crt_mas[-1].w -= 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                # размер: высота
                chance = rand(0, 100)
                if 90 <= chance < 95:
                    crt_mas[-1].h += 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 95 <= chance:
                    crt_mas[-1].h -= 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                # размер видимого поля
                chance = rand(0, 100)
                if 90 <= chance < 95:
                    crt_mas[-1].expantion(clamp(crt_mas[-1].sens + 2, 45))
                elif 95 <= chance:
                    crt_mas[-1].expantion(clamp(crt_mas[-1].sens - 2, 45, 15))

                # высчитывание цели для дочерней особи
                index.append(fn_nrst_trg(crt_mas[-1], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr, [index[j] for j in range(count_crt) if j != i]))

                # отрисовка дочерней особи
                crtb_gr.add(crt_mas[-1].body)
                crts_gr.add(crt_mas[-1].sens_circ)
                count_crt += 1

            # затраты на рождение
            crt_mas[i].energy = 2.5

    # пересчёт следущей цели-еды
    for i in range(count_crt):
        if index[i] < len(fd_mas):
            if fd_mas[index[i]] not in fd_gr and index[i] != -1:
               index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr,
                                      [index[j] for j in range(count_crt) if j != i])
        elif crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].body not in crtb_gr:
            index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr,
                                   [index[j] for j in range(count_crt) if j != i])
        else:
            # if fd_mas[index[i]] not in fd_gr and index[i] != -1:
            index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr,
                                   [index[j] for j in range(count_crt) if j != i])

    # генерация нового дня
    if len(fd_gr) < COUNT_FD // 100 * 5:
        # генерация нового поля еды
        for i in range(COUNT_FD):
            if fd_mas[i] not in fd_gr:
                fd_mas[i].rect.x = rand(WCR, SCR_W - WCR)
                fd_mas[i].rect.y = rand(HCR, SCR_H - HCR)
                fd_mas[i].image.fill((0, 255, 0))
                fd_mas[i].color  = (0, 255, 0)
                fd_gr.add(fd_mas[i])

        # навый подсчет целей-еды для каждой живой особи (чтобы не бежали все в одну сторону)
        for i in range(count_crt):
            if index[i] >= 0:
                index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr)
            crt_mas[i].days += 1

        # очистка "памяти" от съеденных особей
        index     = [index[i] for i in range(count_crt) if crt_mas[i].body in crtb_gr]
        crt_mas   = [crt_mas[i] for i in range(count_crt) if crt_mas[i].body in crtb_gr]
        count_crt = len(crt_mas)

        # обновление дня
        days += 1
    # обновление информации
    brd_info = ""
    vis_gr   = []
    alive = count_crt - index.count(-1)

    # изменение настроек
    for i in range(3):
        if curs_mas[i].rect.x <= pg.mouse.get_pos()[0] <= curs_mas[i].rect.x + curs_mas[i].rect.w and \
                curs_mas[i].rect.y <= pg.mouse.get_pos()[1] <= curs_mas[i].rect.y + curs_mas[i].rect.h and \
                    pg.mouse.get_pressed()[0]:
            curs_mas[i].redraw(pg.mouse.get_pos())
            # количество еды
            if i == 0:
                COUNT_FD = int(2000 * curs_mas[i].percent)
                while COUNT_FD > len(fd_mas):
                    fd_mas.append(Food())
                    fd_mas[-1].rect.x = rand(WCR, SCR_W - WCR)
                    fd_mas[-1].rect.y = rand(HCR, SCR_H - HCR)
                    fd_mas[-1].image.fill((0, 255, 0))
                    fd_mas[-1].color = (0, 255, 0)
                    fd_gr.add(fd_mas[-1])
                while COUNT_FD < len(fd_mas):
                    fd_mas[-1].kill()
                    fd_mas = fd_mas[:-1]
            if i == 1:
                SPEED = curs_mas[i].percent

    # оформление
    pg.draw.line(set_pan, (130, 130, 130), (10, 120), (Set_W - 10, 120))
    curs_gr.draw(set_pan)
    pg.draw.line(set_pan, (130, 130, 130), (10, 380), (Set_W - 10, 380))

    set_pan.blit(l1, (Set_W * (1 - 170/Set_W) / 2, 15))
    set_pan.blit(l2, (Set_W * (1 - 170/Set_W) / 2 + 1, 40))
    set_pan.blit(l3, (Set_W * (1 - 170/Set_W) / 2 + 4, 65))
    set_pan.blit(l4, (Set_W * (1 - 140/Set_W) / 2, 135))
    set_pan.blit(l5, (Set_W * (1 - 150/Set_W) / 2, 215))

    pg.time.delay(int(100 * (1 - SPEED)))

    pg.display.update()
