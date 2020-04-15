import pygame as pg

# настройки окна
Win_W = 1350
Win_H = 700

# настройки экрана настроек
Set_W = 250
Set_H = 700

# настройки экрана жизни
SCR_W = Win_W - Set_W
SCR_H = Win_H

# общие настройки
COUNT_CRT = 0
Coef = 0.0008
COUNT_FD = int(SCR_W * SCR_H * Coef)
START_TIME = pg.time.get_ticks()
PAUSE = 0
SPEED = 0.8
SP_GEN_FD = 0.615

# настройки особи
WCR = HCR = 8
SENS = 30

# настройки еды
WF = HF = 4
FD_EN = 0.25
STEP_FAD = 17