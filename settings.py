import pygame as pg

# настройки экрана
SCR_W = 1300
SCR_H = 700

# общие настройки
COUNT_CRT = 5
COUNT_FD = int(SCR_W * SCR_H * 0.00075)
START_TIME = pg.time.get_ticks()

# настройки особи
WCR = HCR = 8
SENS = 30

# настройки еды
WF = HF = 4
FD_EN = 0.25
STEP_FAD = 17