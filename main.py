import pygame as pg

from Food import Food
from Creature import Creature

from random import randint as rand
from lib_func import *
from settings import *

count_crt = COUNT_CRT
alive     = count_crt
days      = 1
brd_info  = ""
iterator  = 0

pg.init()

window = pg.display.set_mode((SCR_W, SCR_H))
run = 1

all_s    = pg.sprite.Group()
fd_gr    = pg.sprite.Group()
crtb_gr  = pg.sprite.Group()
crts_gr  = pg.sprite.Group()
deadb_gr = pg.sprite.Group()
deads_gr = pg.sprite.Group()

vis_gr   = []
crt_mas  = [Creature(WCR, HCR, SENS) for i in range(count_crt)]
fd_mas   = [Food() for i in range(COUNT_FD)]

breed_mas = [count_crt]

for i in range(count_crt):
    crtb_gr.add(crt_mas[i].body)
    crts_gr.add(crt_mas[i].sens_circ)
    all_s.add(crt_mas[i].terretory)

for i in range(COUNT_FD):
    all_s.add(fd_mas[i])
    fd_gr.add(fd_mas[i])

f = pg.font.Font(None, 36)
index = [fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr) for i in range(count_crt)]

while run:
    l1 = f.render("Creatures - " + str(len(crtb_gr)), 1, (255, 255, 255))
    l2 = f.render("Alive      - " + str(alive), 1, (255, 255, 255))
    l3 = f.render("Food      - " + str(len(fd_gr)), 1, (255, 255, 255))
    l4 = f.render("Days      - " + str(days), 1, (255, 255, 255))
    while iterator != len(breed_mas) and not breed_mas[iterator]:
        brd_info = str(iterator + 1) + "^0: "
        iterator += 1

    for i in range(iterator, len(breed_mas)):
        brd_info += str(breed_mas[i])
        if i != len(breed_mas) - 1:
            brd_info += ", "
    iterator = 0
    l6 = f.render("Breeds      - " + brd_info, 1, (255, 255, 255))

    window.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0

    crts_gr.draw(window)
    fd_gr.draw(window)
    crtb_gr.draw(window)

    temp_time = pg.time.get_ticks()
    if (temp_time - START_TIME) % 10 == 0:
        for i in range(len(fd_mas)):
            if fd_mas[i].color[0]:
                fd_mas[i].fading()

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

    for i in range(len(vis_gr)):
        vis_gr[i].color = (255, 0, 0)

    if not PAUSE:
    # видит ли особь другую особь меньше себя
        for i in range(count_crt):
            vis_gr = pg.sprite.spritecollide(crt_mas[i].sens_circ, crtb_gr, False) # массив всех коллизий особи с группой тел всех особей
            if len(vis_gr) > 1:
                if index[i] <= COUNT_FD:
                    for j in range(len(vis_gr)): # проход по всем спрайтам внутри заданного массива
                        if crt_mas[i].weight - 17 > vis_gr[j].rect.w*vis_gr[j].rect.h: # поиск первого вхождения особи с весом меньше
                            while crt_mas[iterator].body.rect != vis_gr[j].rect:  # нахождение индекса найденного спрайта в массиве всех особей
                                iterator += 1
                            if crt_mas[i].parent_name == crt_mas[iterator].name or \
                                crt_mas[i].child_name == crt_mas[iterator].name:
                                iterator = 0
                                continue
                            index[i] = iterator + COUNT_FD # переопределение цели на найденную особь
                            print(crt_mas[i].body.rect, crt_mas[iterator].body.rect, vis_gr[j].rect)
                            iterator = 0
                            break
            elif index[i] > COUNT_FD:
                index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr)

    # передвижение каждой особи
        for i in range(count_crt):
            # Костыль; без него нормально не работает. ХЗ
            if crt_mas[i].body in crtb_gr and crt_mas[i].sens_circ not in crts_gr:
                crts_gr.add(crt_mas[i].sens_circ)
            if crt_mas[i].body not in crtb_gr and crt_mas[i].sens_circ in crts_gr:
                crt_mas[i].sens_circ.kill()

            tmp = 1
            if index[i] < len(fd_mas):
                if (crt_mas[i].body.rect.x != fd_mas[index[i]].rect.x or \
                    crt_mas[i].body.rect.y != fd_mas[index[i]].rect.y) and \
                    index[i] != -1:

                    tmp = crt_mas[i].go_to_targer(fd_mas[index[i]])
            else:
                if (crt_mas[i].body.rect.x != crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body.rect.x or \
                    crt_mas[i].body.rect.y != crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body.rect.y) and \
                    index[i] != -1:

                    tmp = crt_mas[i].go_to_targer(crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)])

            # регестрация гибели
            if tmp == 0:
                alive   -= 1
                index[i] = -1
                deadb_gr.add(crt_mas[i].body)
                deads_gr.add(crt_mas[i].sens_circ)
                breed_mas[crt_mas[i].breed - 1] -= 1

    # обработка энергии
    for i in range(count_crt):
        hit_gr = pg.sprite.spritecollide(crt_mas[i].body, fd_gr, True)
        # съела ли особь еду
        if len(hit_gr):
            for j in range(len(hit_gr)):
                crt_mas[i].energy += FD_EN

        # съела ли особь другую особь
        elif index[i] >= COUNT_FD:
            # мёртвую
            hit_gr = pg.sprite.spritecollide(crt_mas[i].body, deadb_gr, True)
            if len(hit_gr):
                while crt_mas[iterator].body not in hit_gr and iterator < count_crt:
                    iterator += 1
                if iterator < count_crt:
                    crt_mas[i].energy += 0.5 * crt_mas[iterator].weight / 64
                    hit_gr_dead  = pg.sprite.spritecollide(crt_mas[i].body, deads_gr, True)
                    hit_gr_dead += pg.sprite.spritecollide(crt_mas[i].body, deadb_gr, True)
                iterator = 0

            # живую
            hit_gr = pg.sprite.spritecollide(crt_mas[i].body, crtb_gr, False) # массив коллизий тела особи с группой тел всех особей
            if len(hit_gr) > 1:
                tmpb_gr = pg.sprite.Group([crt_mas[j].body for j in range(count_crt) if j != i])      # группа тел всех особей кроме итой
                tmps_gr = pg.sprite.Group([crt_mas[j].sens_circ for j in range(count_crt) if j != i]) # -//-
                hit_gr_dead = pg.sprite.spritecollide(crt_mas[i].body, tmpb_gr, True)  # удаление тела цели
                hit_gr_dead += pg.sprite.spritecollide(crt_mas[i].body, tmps_gr, True) # -//-

                crt_mas[i].energy += crt_mas[index[i] - COUNT_FD].energy / 5
                crt_mas[index[i] - COUNT_FD].energy = 0
                index[index[i] - COUNT_FD] = -1
                breed_mas[crt_mas[index[i] - COUNT_FD].breed - 1] -= 1
                alive -= 1

        # рождение
        if crt_mas[i].energy > 9.8:
            for j in range(int(crt_mas[i].energy // crt_mas[i].birth_enr)):
                # вычисление координат дочерней особи
                cords = (crt_mas[i].body.rect.x + WCR, crt_mas[i].body.rect.y + HCR)

                # факт рождения
                crt_mas.append(Creature(WCR, HCR, SENS, cords, crt_mas[i].breed+1))
                index.append(fn_nrst_trg(crt_mas[-1], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr, [index[j] for j in range(count_crt) if j != i]))

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
                    crt_mas[-1].w = clamp(crt_mas[-1].w + 2, 20, 2)
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 95 <= chance:
                    crt_mas[-1].w = clamp(crt_mas[-1].w - 2, 20, 2)
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                # размер: высота
                chance = rand(0, 100)
                if 90 <= chance < 95:
                    crt_mas[-1].h = clamp(crt_mas[-1].h + 2, 20, 2)
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 95 <= chance:
                    crt_mas[-1].h = clamp(crt_mas[-1].h - 2, 20, 2)
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                print(crt_mas[-1].weight)

                # статистика
                if len(breed_mas) < crt_mas[-1].breed:
                    breed_mas.append(1)
                else:
                    breed_mas[crt_mas[-1].breed - 1] += 1
                alive += 1

                crtb_gr.add(crt_mas[-1].body)
                crts_gr.add(crt_mas[-1].sens_circ)
                all_s.add(crt_mas[-1].terretory)
                count_crt += 1

                # затраты на рождение
                # tmp -= crt_mas[i].birth_enr
            crt_mas[i].energy = 2.5

    # пересчёт следущей цели-еды
    for i in range(count_crt):
        if index[i] < len(fd_mas):
            if fd_mas[index[i]] not in fd_gr and index[i] != -1:
               index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr,
                                      [index[j] for j in range(count_crt) if j != i])
        elif crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body not in crtb_gr:
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
                all_s.add(fd_mas[i])

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

    keys = pg.key.get_pressed()
    if keys[pg.K_SPACE]:
        PAUSE = (PAUSE + 1) % 2
    '''if keys[pg.K_RIGHT] and crt_mas[0].body.rect.x + 20 < 495:
        crt_mas[0].body.rect.x += 2
        crt_mas[0].senc_circ.rect.x += 2
    if keys[pg.K_UP] and crt_mas[0].body.rect.y > 5:
        crt_mas[0].body.rect.y -= 2
        crt_mas[0].senc_circ.rect.y -= 2
    if keys[pg.K_LEFT] and crt_mas[0].body.rect.x > 5:
        crt_mas[0].body.rect.x -= 2
        crt_mas[0].senc_circ.rect.x -= 2
    if keys[pg.K_DOWN] and crt_mas[0].body.rect.y + 20 < 495:
        crt_mas[0].body.rect.y += 2
        crt_mas[0].senc_circ.rect.y += 2'''

    brd_info = ""
    vis_gr   = []
    window.blit(l1, (20, 15))
    window.blit(l2, (40, 40))
    window.blit(l3, (41, 65))
    window.blit(l4, (44, 86))
    window.blit(l6, (20, 110))
    pg.time.delay(10)
    pg.display.update()
