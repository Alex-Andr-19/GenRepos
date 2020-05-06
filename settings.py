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
pg.init()
F1 = pg.font.Font(None, 36)
F2 = pg.font.Font(None, 29)
COUNT_CRT = 5
Coef = 0.0008
COUNT_FD = int(SCR_W * SCR_H * Coef)
START_TIME = pg.time.get_ticks()
PAUSE = 0
SPEED = 0.8
SP_GEN_FD = 0.615

# расширенные настройки
Sp_MUT = 1
R_MUT = 1
W_MUT = 1
H_MUT = 1
Se_MUT = 1

# настройки особи
WCR = HCR = 8
SENS = 30

# настройки еды
WF = HF = 4
FD_EN = 0.25
STEP_FAD = 17