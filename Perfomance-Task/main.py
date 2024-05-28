# All Images used in this Game is drawn in Pixilart.com

import pygame as pg
import sys
from pygame.locals import *
from random import *

screen_width=550
screen_height= 800

pancakeH = 33
pancakeW = 100

bg_color = (220,200,190) #Blue
text_color = (246, 240, 241) #White

fps = 60
timer = pg.time.Clock()

score = 0
speed = 25

pg.init()
gameScreen = pg.display.set_mode([screen_width, screen_height])
pg.display.set_caption("Pancake Stacker!!!")

#font downloaded from: https://www.dafont.com/grand9k-pixel.font
font = pg.font.Font("Perfomance-Task/Assets/fonts/Grand9K Pixel.ttf", 50)
large_font = pg.font.Font("Perfomance-Task/Assets/fonts/Grand9K Pixel.ttf", 90)

#Class 
class gameObject(): #Creates Game Objects
    def __init__(self, x, y, image, size):
        w = image.get_width()
        h = image.get_height()
        self.image = pg.transform.scale(image, (int(w * size), int(h * size)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ButtonClicked = False

    def draw_frame(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_button(self, screen):
        RunProcedure = False
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and self.ButtonClicked == False:
                self.ButtonClicked = True
                RunProcedure= True
                return RunProcedure

        if pg.mouse.get_pressed()[0] == 0:
            self.ButtonClicked = False
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_text(text, y_pos, fontsize):
        text = fontsize.render(text, True, text_color)
        text_rect = text.get_rect(center=(screen_width/2, y_pos))
        gameScreen.blit(text, text_rect)

class Sprite(pg.sprite.Sprite): # Creates Sprites
    def __init__(self, x, y, image, speed):
        self.x = x
        self.y = y
        self.w = image.get_width()/3
        self.h = image.get_height()/3
        self.speed = speed
        self.image = pg.transform.scale(image, (int(self.w), int(self.h)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_pancakes(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_platform(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.x += self.speed
        if self.x > screen_width:
            self.speed *= -1
        if self.x + self.w < 1:
            self.speed *= -1
        self.rect.x = self.x

class Stack:
    def __init__(self):
        global speed
        self.stack = []
        self.initSize = 10
        for i in range(self.initSize):
            newPancake = Sprite(screen_width/2, screen_height - i*pancakeH, pg.image.load("Perfomance-Task/Assets/images/pancakes.png"), speed)
            self.stack.append(newPancake)

    def show(self):
        for i in range(self.initSize):
            self.stack[i].update_pancakes(gameScreen)

    def move(self):
        for i in range(self.initSize):
            if i == len(self.stack) - 1:
                self.stack[i].move()
            self.stack[i].update_pancakes(gameScreen)

    def newPancake(self):
        global speed, score, pancakeH, pancakeW

        if score%4 == 0:
            speed = speed*1.2

        newPancake = Sprite(screen_width, screen_height - 10*pancakeH, pg.image.load("Perfomance-Task/Assets/images/pancakes.png"), speed)
        self.initSize += 1
        self.stack.append(newPancake)  

    def pushStack(self):
        global score, pancakeH, pancakeW
        side1 = self.stack[self.initSize - 2]
        side2 = self.stack[self.initSize - 1]
        if side2.x <= side1.x and not (side2.x + side2.w < side1.x):
            self.stack[self.initSize - 1].speed = 0
            score += 1
        elif side1.x <= side2.x <= side1.x + side1.w:
            self.stack[self.initSize - 1].speed = 0
            score += 1
        else:
            game_over()
        for i in range(self.initSize):
            self.stack[i].rect.y += pancakeH

Start_Button = gameObject(screen_width/3, screen_height*4.1/5, pg.image.load("Perfomance-Task/Assets/images/Play.png"), 0.35)
Exit_Button = gameObject(screen_width*2/3, screen_height*4.1/5, pg.image.load("Perfomance-Task/Assets/images/Exit.png"), 0.35)
Restart_Button = gameObject(screen_width/3, screen_height*3/4, pg.image.load("Perfomance-Task/Assets/images/Restart.png"), 0.35)
Home_Button = gameObject(screen_width*2/3, screen_height*3/4, pg.image.load("Perfomance-Task/Assets/images/home.png"), 0.35)
Game_Title = gameObject(screen_width/2, screen_height*1.7/4, pg.image.load("Perfomance-Task/Assets/images/title.png"), 1.05)


def terminate():
    pg.quit()
    sys.exit()    

def game_loop():
    global score, speed
    run = True
    speed = 3
    score = 0

    stack = Stack()
    stack.newPancake()

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    stack.pushStack()
                    stack.newPancake()
                if event.key == pg.K_ESCAPE:
                    game_over()
                    run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                stack.pushStack()
                stack.newPancake()

        gameScreen.fill(bg_color)
        gameObject.draw_text(str(score), screen_height/6, font)
        stack.move()
        stack.show()
        pg.display.update()
        timer.tick(60)

def start_screen(screen):  
    run = True
    screen.fill(bg_color)
    while run:
        timer.tick(fps)
        Game_Title.draw_frame(screen)
        for event in pg.event.get():
            if Start_Button.draw_button(screen):
                game_loop()
                run = False
            if Exit_Button.draw_button(screen):
                run = False
            if event.type == KEYDOWN:
                if event.key == K_s:
                    run = False
                if event.key == K_ESCAPE:
                    run = False
            if event.type == QUIT:
                terminate()
            pg.display.update()

def game_over():
    pg.time.wait(1000)
    run = True
    gameScreen.fill(bg_color)
    while run:
        timer.tick(fps)
        gameObject.draw_text("Game Over!", screen_height/6, font)
        gameObject.draw_text("Your score:", screen_height*1.8/6, font)
        gameObject.draw_text(str(score), screen_height/2.2, large_font)

        for event in pg.event.get():
            if Home_Button.draw_button(gameScreen):
                start_screen(gameScreen)
                run = False
            if Restart_Button.draw_button(gameScreen):
                game_loop()
                run = False
            if event.type == QUIT:
                terminate()
            pg.display.update()

start_screen(gameScreen)
