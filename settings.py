import pygame as pg

SCR_W = 1300
SCR_H = 700

WCR = HCR = 8
SENS = 30

WF = HF = 4

COUNT_CRT = 20
print(int(SCR_W * SCR_H * 0.00121))
COUNT_FD = int(SCR_W * SCR_H * 0.00121)

FD_EN = 0.25

START_TIME = pg.time.get_ticks()