import pygame as pg
import sys
from random import randint
from functools import *


class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 5

    def move(self, key):
        global cells

        if key == 'w':
            if cells[self.y - 1][self.x].type in [1, 2, 3]:
                self.y -= 1
        elif key == 's':
            if cells[self.y + 1][self.x].type in [1, 2, 3]:
                self.y += 1
        elif key == 'a':
            if cells[self.y][self.x - 1].type in [1, 2, 3]:
                self.x -= 1
        elif key == 'd':
            if cells[self.y][self.x + 1].type in [1, 2, 3]:
                self.x += 1

    def draw(self):
        global cells
        pg.draw.rect(win, (255, 0, 0), (cells[self.y][self.x].x + 5, cells[self.y][self.x].y + 5, 65, 65))


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cx = self.x // 75
        self.cy = self.y // 75
        self.type = 1
        self.center = (x + 75 / 2, y + 75 / 2)

    def draw(self):
        color = (255, 255, 255)
        cell_img = None
        if self.type == 0:
            cell_img = pg.image.load('Вода_75х75(3).png')
        elif self.type == 1:
            cell_img = pg.image.load('Песок_75х75.png')
        elif self.type == 2:
            cell_img = pg.image.load('Ресурс 30.png')
        elif self.type == 3:
            cell_img = pg.image.load('Ресунок 32.png')
        cell_rect = cell_img.get_rect(center=self.center)
        win.blit(cell_img, cell_rect)


class Kuvshinka:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = randint(2, 3)
        if self.type == 2:
            self.timer = randint(120, 150)
        elif self.type == 3:
            self.timer = randint(180, 210)


win = pg.display.set_mode((750, 790))

# ---------- Текст ------------ #

score = 0
string_score = 'Счёт: ' + str(score)
pg.font.init()
textF = pg.font.Font('carbonara(FONT BY LYAJKA)', 45)
text = textF.render(string_score, False, 'black')

# ---------- Изображения ------- #

# list_image = [pg.image.load('image/Песок_75х75.png'), pg.image.load('image/Вода_75х75(3).png'), pg.image.load('image/Кувшинка_большая.png'), pg.image.load('image/Кувшинка_маленькая.png')]

# sirs = get_rect(center=(24+i*50, 30))

# screen.blit(имя, центр)

# ---------- Создание ячеек ---------- #

cells = []
for y in range(0, 750, 75):
    cells_x = []
    for x in range(0, 750, 75):
        cells_x.append(Cell(x, y))
    cells.append(cells_x)

for y in range(0, 10):
    for x in range(1, 9):
        cells[y][x].type = 0

free_cells = []
for y in range(0, 10):
    for x in range(1, 9):
        if cells[y][x].type == 0:
            free_cells.append([x, y])

# ------------------------------------- #


player = Player(0, 0)

# -------- Строительство кувшинок -------- #


kuvshinki = []


def build():
    cords = randint(0, len(free_cells) - 1)
    kuvshinki.append(Kuvshinka(free_cells[cords][0], free_cells[cords][1]))
    free_cells.pop(cords)


for i in range(30):
    build()

# -------------------------------------- #

death_timer = 0
death_timeout = 90

run = True

death = False

pg.init()
while True:

    if death == False:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    player.move('w')
                elif event.key == pg.K_s:
                    player.move('s')
                elif event.key == pg.K_a:
                    player.move('a')
                elif event.key == pg.K_d:
                    player.move('d')

        for k in kuvshinki:
            cells[k.y][k.x].type = k.type
            k.timer -= 1
            if k.timer == 0:
                cells[k.y][k.x].type = 0
                kuvshinki.remove(k)
                if k.x == player.x and k.y == player.y:
                    death = True
                else:
                    build()

        for l in cells:
            for n in l:
                if player.x == n.x and player.y == n.y and n.type == 0:
                    death = True

    win.fill((255, 255, 255))
    for cells_x in cells:
        for cell in cells_x:
            cell.draw()
    player.draw()
    win.blit(text, (3, 747))

    if death:
        death_timer += 1
    if death_timer == death_timeout:
        sys.exit()

    pg.display.update()
    pg.time.wait(30)
