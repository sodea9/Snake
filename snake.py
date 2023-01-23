#Author: Sean O'Dea
#Publication Date 1/15/2023
#Beta 0.9

import pygame as pg
import random
from constants import *

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pg.init()

class BodyBlock(pg.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super(BodyBlock, self).__init__()
        self.surf = pg.Surface((SQ, SQ))
        self.surf.fill(GREEN)
        self.rect = pg.Rect(x, y, SQ, SQ)

    def update(self, x, y):
        self.rect = pg.Rect(x, y, SQ, SQ)

class Head(BodyBlock):
    def __init__(self):
        super(Head, self).__init__()
        self.rect = pg.Rect(168,SCREEN_HEIGHT//2,SQ,SQ)

    def update(self, direction):
        """
        moves head of snake to next position based on current direction
        """
        if direction == "RIGHT":
           self.rect.move_ip(SQ+1, 0)
        elif direction == "LEFT":
           self.rect.move_ip(-(SQ+1), 0)
        elif direction == "DOWN":
           self.rect.move_ip(0, SQ+1)
        elif direction == "UP":
           self.rect.move_ip(0, -(SQ+1))

class Snake():
    def __init__(self):
        self.head = Head()
        self.parts = [self.head,BodyBlock(self.head.rect.left-(SQ+1), self.head.rect.top),
                    BodyBlock(self.head.rect.left-((SQ+1)*2), self.head.rect.top)]
        snakeBodyGroup.add(self.parts[1], self.parts[2])

    def append(self):
        self.parts.append(BodyBlock(self.tailx, self.taily))
        snakeBodyGroup.add(self.parts[-1])

    def update(self,direction):
        self.tailx, self.taily = self.parts[-1].rect.left, self.parts[-1].rect.top
        i = len(self.parts)-1
        while i >= 0:
            nextPartx, nextParty = self.parts[i-1].rect.left, self.parts[i-1].rect.top
            if isinstance(self.parts[i], Head):
                self.parts[i].update(direction)
            else:
                self.parts[i].update(nextPartx, nextParty)
            i-=1
        self.tailx, self.taily = self.parts[-1].rect.left, self.parts[-1].rect.top
  
    def toDisplay(self):
        for part in self.parts:
            screen.blit(part.surf, part.rect)

class Apple(BodyBlock):
    def __init__(self):
        super(Apple, self).__init__()
        self.surf.fill(RED)
        self.rect = pg.Rect(525,315,SQ,SQ)
  
    def update(self):
        """
        randomly moves apple location, makes sure apple doesn't spawn in snake
        """
        while pg.sprite.spritecollideany(apple, snakeBodyGroup) or\
                                            pg.sprite.collide_rect(apple, snake.head):
            randomx = random.randrange(0,SCREEN_WIDTH,SQ+1)
            randomy = random.randrange(0,SCREEN_HEIGHT,SQ+1)
            self.rect = pg.Rect(randomx, randomy, SQ, SQ)
        
    def toDisplay(self):
        screen.blit(apple.surf, apple.rect)

def endGame(head):
    #checks if head hits edge
    if head.rect.left < 0 or head.rect.right > SCREEN_WIDTH or head.rect.top < 0\
                                             or head.rect.bottom >= SCREEN_HEIGHT:
        return True
    #checks if head hits body
    elif pg.sprite.spritecollideany(snake.head, snakeBodyGroup):
        return True
    else:
        return False

def eventHandler(initial_direction):
    global running
    global snakeDirection
    for event in pg.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False                        #BUG: 
            elif event.key == K_UP and initial_direction != "DOWN":
                snakeDirection = "UP"
            elif event.key == K_DOWN and initial_direction != "UP":
                snakeDirection = "DOWN"
            elif event.key == K_LEFT and initial_direction != "RIGHT":
                snakeDirection = "LEFT"
            elif event.key == K_RIGHT and initial_direction != "LEFT":
                snakeDirection = "RIGHT"
        elif event.type == QUIT:
            running = False
    
if __name__ == '__main__':
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pg.display.set_caption("Snake v0.9")
    screen.fill(BLACK)

    snakeDirection = "RIGHT"

    snakeBodyGroup = pg.sprite.Group()
    snake = Snake()
    apple = Apple()

    clock = pg.time.Clock()
    running = True
    print("Snake by Sean v0.9")

    #MAIN GAME LOOP
    while running:
        #handles user input
        eventHandler(snakeDirection)

        #change state of snake and apple
        snake.update(snakeDirection)
        if pg.sprite.collide_rect(snake.head, apple):
            snake.append()
            apple.update()

        #checks for quit condition
        if endGame(snake.head):
            running = False

        #update display
        screen.fill(BLACK)
        snake.toDisplay()
        apple.toDisplay()

        pg.display.flip()
        clock.tick(GAMESPEED)

    pg.quit()