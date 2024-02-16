#!/usr/bin/env python
import sys, pygame
from pygame.locals import *
import recognition as recog

pygame.init()
screen = pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pygame.display.set_caption ('$1 Unistroke Recognizer')
clock = pygame.time.Clock()

def showtext(text, x, y):
    font = pygame.font.SysFont("lucidaconsole", 20)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))
    pygame.display.update()



done = False
judge=0
start = 0
score=0
position= []



numpos=190
scorepos=450



while not done:
    clock.tick(150)
    x,y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           done = True
           
        elif event.type == MOUSEBUTTONDOWN:
            judge=1      
            if start == 0:
                screen.fill((255,255,255))
                position = []
                start = 1                
        elif event.type == MOUSEBUTTONUP:
            judge=0
            start = 0
            if len(position)>10:

                score=recog.recognize(position)

                if score[1]<0:
                    showtext("xx", numpos, 0)
                    showtext("xx  unable to recognize", scorepos, 0)
                else:                
                    showtext("%s"%score[0], numpos, 0)
                    showtext("%f"%score[1], scorepos, 0)
            else:
                showtext("xx", numpos, 0)
                showtext("xx  too small to see", scorepos, 0)
        if judge == 1:
            pygame.draw.circle(screen, (0,0,255), (x,y), 4)
            position.append((x,y))
            pygame.display.update()
     
    showtext("Pattern:", 90, 0)
    showtext("Score:", 350, 0)

    pygame.display.update()

