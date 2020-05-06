import matplotlib.pyplot as plt

from Statistics import Statistic
from Food import Food
from Creature import Creature
from Cursor import Cursor
from DNA import DNA
from Button import Button
from SubWindow import subwindow

from random import randint as rand
from lib_func import *
from settings import *

count_crt = COUNT_CRT
alive     = count_crt
days      = 1
brd_info  = ""
iterator  = 0
focus = -1
redraw_dna = 0

pg.init()

window = pg.display.set_mode((Win_W, Win_H))
screen = window.subsurface((Set_W, 0, SCR_W, SCR_H))
set_pan = window.subsurface((0, 0, Set_W, SCR_H))
btn_mas = [Button(186, 2, "img/pause.png"), Button(218, 2, "img/reset.png"), Button(2, 5, " Statistic", 93, 22)]

stat_w = subwindow(95, 27, 900, 510)
stat = Statistic()
visible = 0

run = 1

fd_gr = pg.sprite.Group()
crtb_gr = pg.sprite.Group()
crts_gr = pg.sprite.Group()
deadb_gr = pg.sprite.Group()
deads_gr = pg.sprite.Group()
curs_gr = pg.sprite.Group()
btn_gr = pg.sprite.Group()

vis_gr   = []
crt_mas  = [Creature(WCR, HCR, SENS) for i in range(count_crt)]
fd_mas   = [Food() for i in range(COUNT_FD)]
curs_mas = [Cursor(10, 160 + 80 * i, [COUNT_FD / 2000, SPEED, SP_GEN_FD][i]) for i in range(3)]

for i in range(count_crt):
    crtb_gr.add(crt_mas[i].body)
    crts_gr.add(crt_mas[i].sens_circ)

for i in range(COUNT_FD):
    fd_gr.add(fd_mas[i])

for i in range(3):
    curs_gr.add(curs_mas[i])

for i in range(len(btn_mas)):
    btn_gr.add(btn_mas[i])

index = [fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr) for i in range(count_crt)]

dna = DNA(15, 70, 430)
time_of_press = pg.time.get_ticks()

# начало программы
while run:

    # вывод информации о ситуации
    l1 = F1.render("Alive      - " + str(alive), 1, (0, 0, 0))
    l2 = F1.render("Food      - " + str(int(len(fd_gr) / COUNT_FD * 100)) + "%", 1, (0, 0, 0))
    l3 = F1.render("Days      - " + str(days), 1, (0, 0, 0))
    l4 = F1.render("Food - " + str(COUNT_FD), 1, (0, 0, 0))
    l5 = F1.render("Speed - " + str(int(curs_mas[1].percent * 100)) + "%", 1, (0, 0, 0))
    l6 = F2.render("Speed gener. food - " + str(int(curs_mas[2].percent * 100)) + "%", 1, (0, 0, 0))

    screen.fill((0, 0, 0))
    set_pan.fill((210, 210, 210))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = 0
        if event.type == pg.KEYUP and 0 <= focus < count_crt:
            index[focus] = fn_nrst_trg(crt_mas[focus], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr)

    # перемещение курсора с помощью клавиши TAB
    keys = pg.key.get_pressed()
    if keys[pg.K_TAB] and pg.time.get_ticks() - time_of_press > 300:
        # чтобы курсор не проскакивал
        time_of_press = pg.time.get_ticks()
        dna.normal()
        if 0 <= focus < count_crt:
            crt_mas[focus].focus = 0
        focus = cycle(focus + 1, count_crt + 2, 0)
        while focus < count_crt and not crt_mas[focus].energy:
            focus = cycle(focus + 1, count_crt + 2, 0)
        if 0 <= focus < count_crt:
            crt_mas[focus].focus = 1
            dna.redraw(crt_mas[focus])
        elif focus > 0:
            redraw_cursors(focus, count_crt, curs_mas)
            x = curs_mas[focus - count_crt].percent * (Set_W - 20)
            curs_mas[focus - count_crt].redraw((x, 0))
    # Пауза
    if keys[pg.K_SPACE] and pg.time.get_ticks() - time_of_press > 300:
        # чтобы курсор не проскакивал
        time_of_press = pg.time.get_ticks()
        PAUSE = not PAUSE
        if PAUSE:
            btn_mas[0].redraw("img/play.png")
        else:
            btn_mas[0].redraw("img/pause.png")
    # Закрытие окна статистики
    if keys[pg.K_ESCAPE] and visible:
        visible = 0
        btn_mas[2].unfocus()
        PAUSE = 0

        btn_mas[0].redraw("img/pause.png")

    # отрисовка всех объектов
    crts_gr.draw(screen)
    fd_gr.draw(screen)
    crtb_gr.draw(screen)
    btn_gr.draw(set_pan)

    # "обнуление" фокуса
    if pg.mouse.get_pressed()[0] and not focus >= count_crt:
        focus = -1

    # снятие фокуса с особей
    if not 0 <= focus < count_crt:
        if redraw_dna:
            dna.normal()
            redraw_dna = 0
        for j in range(count_crt):
            crt_mas[j].focus = 0

    # затухание еды
    temp_time = pg.time.get_ticks()
    if (temp_time - START_TIME) % 10 == 0:
        for i in range(len(fd_mas)):
            if fd_mas[i].color[0]:
                fd_mas[i].fading()

    # появление новой еды
    if (temp_time - START_TIME) % (int(200 * (1 - SP_GEN_FD)) + 1) == 0 and not PAUSE:
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

        # передвижение выбранной особи
        keys = pg.key.get_pressed()
        control = 0
        if keys[pg.K_RIGHT] and 0 <= focus < count_crt:
            control = 1
            crt_mas[focus].body.rect.x += 1
            crt_mas[focus].sens_circ.rect.x += 1
        elif keys[pg.K_UP] and 0 <= focus < count_crt:
            control = 1
            crt_mas[focus].body.rect.y -= 1
            crt_mas[focus].sens_circ.rect.y -= 1
        elif keys[pg.K_LEFT] and 0 <= focus < count_crt:
            control = 1
            crt_mas[focus].body.rect.x -= 1
            crt_mas[focus].sens_circ.rect.x -= 1
        elif keys[pg.K_DOWN] and 0 <= focus < count_crt:
            control = 1
            crt_mas[focus].body.rect.y += 1
            crt_mas[focus].sens_circ.rect.y += 1
        elif keys[pg.K_ESCAPE]:
            focus = -1
        # Убийство особи
        elif keys[pg.K_DELETE] and 0 <= focus < count_crt and crt_mas[focus].energy:
            stat.dead_at_day += 1
            crt_mas[focus].energy = 0
            if 0 <= index[focus] < COUNT_FD:
                tmp = crt_mas[focus].go_to_target(fd_mas[index[focus]])
            elif 0 <= index[focus]:
                tmp = crt_mas[focus].go_to_target(crt_mas[clamp(index[focus] - len(fd_mas), len(crt_mas) - 1)].body)
            stat.dead_at_day += 1

            index[focus] = -1
            deadb_gr.add(crt_mas[focus].body)
            deads_gr.add(crt_mas[focus].sens_circ)
            crt_mas[focus].color2 = (60, 60, 60)
            focus = -1


# ниже функция clamp используется в качестве костыля, потому что без неё почему-то происходит 'index out of range'

        if 0 <= index[i] < COUNT_FD and not PAUSE and (focus != i or not control):
            # к еде
            if (crt_mas[i].body.rect.x != fd_mas[index[i]].rect.x or
                crt_mas[i].body.rect.y != fd_mas[index[i]].rect.y) and \
                index[i] != -1:

                tmp = crt_mas[i].go_to_target(fd_mas[index[i]])
        elif 0 <= index[i] and not PAUSE and (focus != i or not control):
            # к особи
            if (crt_mas[i].body.rect.x != crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].body.rect.x or
                crt_mas[i].body.rect.y != crt_mas[clamp(index[i] - COUNT_FD, count_crt - 1)].body.rect.y) and \
                index[i] != -1:

                tmp = crt_mas[i].go_to_target(crt_mas[clamp(index[i] - len(fd_mas), len(crt_mas) - 1)].body)

        # регестрация гибели
        if tmp == 0:
            # Statistics
            stat.dead_at_day += 1

            index[i] = -1
            deadb_gr.add(crt_mas[i].body)
            deads_gr.add(crt_mas[i].sens_circ)
            crt_mas[i].color2 = (60, 60, 60)
            if focus == i:
                focus = -1

    # обработка энергии
    for i in range(count_crt):
        # фокус на особь
        if crt_mas[i].sens_circ.rect.x <= pg.mouse.get_pos()[0] - Set_W <= crt_mas[i].sens_circ.rect.x + crt_mas[i].sens_circ.rect.w and \
                crt_mas[i].sens_circ.rect.y <= pg.mouse.get_pos()[1] <= crt_mas[i].sens_circ.rect.y + crt_mas[
            i].sens_circ.rect.h and pg.mouse.get_pressed()[0] and crt_mas[i].energy:
            if focus < count_crt:
                crt_mas[focus].focus = 0
            focus = i
            crt_mas[i].focus = 1
            dna.normal()
            dna.redraw(crt_mas[i])
            redraw_dna = 1
            break

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
                # Statistics
                stat.dead_at_day += 1

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
            if focus >= count_crt:
                focus += 1
            for j in range(int(9.8 // crt_mas[i].birth_enr)):
                # Statistics
                stat.birth_at_day += 1

                # вычисление координат дочерней особи
                cords = (crt_mas[i].body.rect.x + WCR, crt_mas[i].body.rect.y + HCR)

                # факт рождения
                crt_mas.append(Creature(WCR, HCR, SENS, cords, crt_mas[i].breed+1))
                crt_mas[i].copy_to(crt_mas[-1])

                # мутация
                # скорость
                chance = rand(0, 100)
                if 90 <= chance < 95 and crt_mas[-1].speed != clamp(crt_mas[-1].speed - 1, 5, 1):
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] - 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed - 1, 5, 1)
                elif chance >= 95 and crt_mas[-1].speed != clamp(crt_mas[-1].speed + 1, 5, 1):
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].color2 = (clamp(crt_mas[-1].color2[0] + 13),
                                          crt_mas[-1].color2[1],
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].speed = clamp(crt_mas[-1].speed + 1, 5, 1)

                # размножение
                chance = rand(0, 100)
                if 90 <= chance < 95 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr + 1, 5, 1):
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] - 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr + 1, 5, 2)
                elif chance >= 95 and crt_mas[-1].birth_enr != clamp(crt_mas[-1].birth_enr - 1, 5, 1):
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].color2 = (crt_mas[-1].color2[0],
                                          clamp(crt_mas[-1].color2[1] + 13),
                                          crt_mas[-1].color2[2])
                    crt_mas[-1].birth_enr = clamp(crt_mas[-1].birth_enr - 1, 5, 2)

                # размер: ширина
                chance = rand(0, 100)
                if 0: # 90 <= chance < 95:
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].w += 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 0: # 95 <= chance:
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].w -= 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                # размер: высота
                chance = rand(0, 100)
                if 0: # 90 <= chance < 95:
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].h += 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h
                elif 0:# 95 <= chance:
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].h -= 2
                    crt_mas[-1].weight = crt_mas[-1].w * crt_mas[-1].h

                # размер видимого поля
                chance = rand(0, 100)
                if 90 <= chance < 95:
                    # Statistics
                    stat.mut_at_day += 1

                    crt_mas[-1].expantion(clamp(crt_mas[-1].sens + 2, 45))
                elif 95 <= chance:
                    # Statistics
                    stat.mut_at_day += 1

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

        # случай, при котором уда, за которой шла особь, удалилась из-за уменьшения её общего количества
        else:
            index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr,
                                   [index[j] for j in range(count_crt) if j != i])

    # "Текучая" статистика
    stat.avarage_day = 0
    stat.oldest_alive_breed = 0
    stat.oldest_creature = 0
    stat.youngest_alive_breed = 1000000
    for i in range(count_crt):
        if crt_mas[i].energy:
            if crt_mas[i].breed > stat.oldest_alive_breed:
                stat.oldest_alive_breed = crt_mas[i].breed
            if crt_mas[i].breed < stat.youngest_alive_breed:
                stat.youngest_alive_breed = crt_mas[i].breed
            if crt_mas[i].days > stat.oldest_creature:
                stat.oldest_creature = crt_mas[i].days

        stat.avarage_day += 1
    stat.avarage_day //= count_crt
    stat.avarage_day = clamp(stat.avarage_day, 1000000, 1)
    if (pg.time.get_ticks() - START_TIME) % 150 == 0:
        stat_w.redraw(stat.oldest_alive_breed,
                      stat.youngest_alive_breed,
                      stat.avarage_day,
                      stat.oldest_creature)

    # генерация нового дня
    if len(fd_gr) < COUNT_FD // 100 * 6:
        stat.new_day(alive)
        # stat.get()
        # генерация нового поля еды
        for i in range(COUNT_FD):
            if fd_mas[i] not in fd_gr:
                fd_mas[i].rect.x = rand(WCR, SCR_W - WCR)
                fd_mas[i].rect.y = rand(HCR, SCR_H - HCR)
                fd_mas[i].image.fill((0, 255, 0))
                fd_mas[i].color = (0, 255, 0)
                fd_gr.add(fd_mas[i])

        # навый подсчет целей-еды для каждой живой особи (чтобы не бежали все в одну сторону)
        for i in range(count_crt):
            if index[i] >= 0:
                index[i] = fn_nrst_trg(crt_mas[i], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr)
            crt_mas[i].days += 1

        # очистка "памяти" от съеденных особей
        index = [index[i] for i in range(count_crt) if crt_mas[i].body in crtb_gr]
        tmp = []
        for i in range(count_crt):
            if crt_mas[i].body in crtb_gr:
                tmp.append(crt_mas[i])
            # коррекция фокуса
            elif i < focus or focus > len(crtb_gr):
                focus -= 1

        crt_mas = tmp
        count_crt = len(crt_mas)

        # обновление дня
        days += 1

    # обновление информации
    brd_info = ""
    vis_gr   = []
    alive = count_crt - index.count(-1)

    # обработка кнопок
    for i in range(len(btn_mas)):
        # Наведён ли курсор на кнопку
        if exist_in(pg.mouse.get_pos(), btn_mas[i].rect):
            # Нажата ли кнопка
            if pg.mouse.get_pressed()[0] and pg.time.get_ticks() - time_of_press > 200:
                time_of_press = pg.time.get_ticks()
                if i == 0 and btn_mas[i].active:
                    btn_mas[i].up()
                else:
                    btn_mas[i].down()

                # Пвуза
                if i == 0:
                    if btn_mas[i].active:
                        btn_mas[i].redraw("img/play.png")
                        PAUSE = 1
                    else:
                        btn_mas[i].redraw("img/pause.png")
                        PAUSE = 0

                # Ресет
                if i == 1:
                    stat.reset()
                    count_crt = COUNT_CRT

                    fd_gr = pg.sprite.Group()
                    crtb_gr = pg.sprite.Group()
                    crts_gr = pg.sprite.Group()
                    deadb_gr = pg.sprite.Group()
                    deads_gr = pg.sprite.Group()

                    vis_gr = []
                    crt_mas = [Creature(WCR, HCR, SENS) for j in range(count_crt)]
                    fd_mas = [Food() for j in range(COUNT_FD)]

                    for j in range(count_crt):
                        crtb_gr.add(crt_mas[j].body)
                        crts_gr.add(crt_mas[j].sens_circ)
                    for j in range(COUNT_FD):
                        fd_gr.add(fd_mas[j])

                    index = [fn_nrst_trg(crt_mas[j], crt_mas, fd_mas, crtb_gr, deadb_gr, fd_gr) for j in
                             range(count_crt)]
                    days = 1

                # Статистика
                if i == 2:
                    if visible:
                        visible = 0
                        btn_mas[0].redraw("img/pause.png")
                        btn_mas[i].active = 0
                        PAUSE = 0
                    else:
                        visible = 1
                        btn_mas[0].redraw("img/play.png")
                        btn_mas[i].active = 1
                        PAUSE = 1

            btn_mas[i].focus()
        elif i != 2 or not btn_mas[i].active:
            btn_mas[i].unfocus()

    # изменение настроек
    for i in range(3):
        if exist_in(pg.mouse.get_pos(), curs_mas[i].rect) and pg.mouse.get_pressed()[0]:
            curs_mas[i].redraw(pg.mouse.get_pos())

            # количество еды
            if i == 0:
                focus = count_crt
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

            # скорость
            if i == 1:
                focus = count_crt + 1
                SPEED = curs_mas[i].percent

            # скорость генерации новой еды
            if i == 2:
                focus = count_crt + 2
                SP_GEN_FD = curs_mas[i].percent

        # фокус на курсор
        redraw_cursors(focus, count_crt, curs_mas)

    # передвижение выбранного курсора
    if focus >= count_crt:
        keys = pg.key.get_pressed()
        # отрисовка
        x = 0
        if keys[pg.K_RIGHT]:
            x = clamp(curs_mas[focus - count_crt].percent * (Set_W - 20) + (Set_W - 20) // 200, SCR_W, 20)
        elif keys[pg.K_LEFT]:
            x = clamp(curs_mas[focus - count_crt].percent * (Set_W - 20) - (Set_W - 20) // 200, SCR_W, 20)
        elif keys[pg.K_UP] and pg.time.get_ticks() - time_of_press > 300:
            # чтобы курсор не проскакивал
            time_of_press = pg.time.get_ticks()
            focus = cycle(focus - 1, count_crt + 2, count_crt)
            x = curs_mas[focus - count_crt].percent * (Set_W - 20)
        elif keys[pg.K_DOWN] and pg.time.get_ticks() - time_of_press > 300:
            # -//-
            time_of_press = pg.time.get_ticks()
            focus = cycle(focus + 1, count_crt + 2, count_crt)
            x = curs_mas[focus - count_crt].percent * (Set_W - 20)
        elif keys[pg.K_ESCAPE]:
            focus = -1

        redraw_cursors(focus, count_crt, curs_mas)

        if x:
            curs_mas[focus - count_crt].redraw((x, 0))

        # изменение настроек
        if focus == count_crt:
            COUNT_FD = int(2000 * curs_mas[0].percent)
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
        elif focus == count_crt + 1:
            SPEED = curs_mas[1].percent
        elif focus == count_crt + 2:
            SP_GEN_FD = curs_mas[2].percent

    # оформление
    pg.draw.line(set_pan, (130, 130, 130), (0, 34), (Set_W, 34))
    pg.draw.line(set_pan, (130, 130, 130), (10, 120), (Set_W - 10, 120))
    curs_gr.draw(set_pan)
    pg.draw.line(set_pan, (130, 130, 130), (10, 380), (Set_W - 10, 380))
    pg.draw.rect(set_pan, (0, 0, 0), (25, 405, 190, 265))
    # ДНК
    for i in range(2):
        dna.turning()
        dna.draw(set_pan)
    set_pan.blit(l1, (Set_W * (1 - 170/Set_W) / 2, 42))
    set_pan.blit(l2, (Set_W * (1 - 170/Set_W) / 2 + 1, 65))
    set_pan.blit(l3, (Set_W * (1 - 170/Set_W) / 2 + 4, 92))
    set_pan.blit(l4, (Set_W * (1 - 140/Set_W) / 2, 135))
    set_pan.blit(l5, (Set_W * (1 - 150/Set_W) / 2, 215))
    set_pan.blit(l6, (10, 295))

    # Отрисовка окна статистики
    if visible:
        stat_w.draw(window)
        for i in range(len(stat_w.buttons)):
            if exist_in(pg.mouse.get_pos(), stat_w.buttons[i].rect):
                stat_w.buttons[i].focus()
            else:
                stat_w.buttons[i].unfocus()
    for i in range(len(stat_w.buttons)):
        if exist_in(pg.mouse.get_pos(), stat_w.buttons[i].rect)\
                and pg.mouse.get_pressed()[0]\
                and pg.time.get_ticks() - time_of_press > 200:
            time_of_press = pg.time.get_ticks()
            if i == 0:
                plt.bar([i + 1 for i in range(days - 1)], stat.BIRTH_PER_DAY)
                plt.show()
            if i == 1:
                plt.bar([i + 1 for i in range(days)], stat.ALIVE_PER_DAY)
                plt.show()
            if i == 2:
                plt.bar([i + 1 for i in range(days - 1)], stat.DEAD_PER_DAY)
                plt.show()
            if i == 3:
                plt.bar([i + 1 for i in range(days - 1)], stat.MUT_PER_DAY)
                plt.show()

    pg.time.delay(int(50 * (1 - SPEED)))

    pg.display.update()
