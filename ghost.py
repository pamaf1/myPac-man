import pygame
import random
from set import *
vec = pygame.math.Vector2
# from Mini import *
from collections import deque 
import numpy as np
# from MinimaxEcpectimax import *

class Ghost():
    def __init__(self, app, coord, number):
        self.app = app
        # self.mini = Mini(None, None)
        self.gridCoord = coord
        self.ghostStartCoord = [coord.x, coord.y]
        self.pixCoord = self.getPixCoord()
        self.number = number
        self.ghostDirection = vec(0,0)
        self.mode = self.ghostMode()
        self.goal = None
        self.speed = 1

    def update(self):
        self.goal = self.set_target()
        if self.goal != self.gridCoord:
            self.pixCoord += self.ghostDirection* self.speed
            if self.inGridMove():
                self.move()

        self.gridCoord[0] = (self.pixCoord[0]- indent +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridCoord[1] = (self.pixCoord[1]- indent +
                            self.app.cellHeight//2)//self.app.cellHeight+1

    def getPixCoord(self):
        return  vec((self.gridCoord[0]*self.app.cellWidth)+indent//2+self.app.cellWidth//2,
                   (self.gridCoord[1]*self.app.cellHeight) +
                   indent//2+self.app.cellHeight//2)

    def drawGhosts(self): 
        self.ghostImage = pygame.image.load('image/Pac-Man-Ghost.png')
        self.ghostImage = pygame.transform.scale(self.ghostImage, (self.app.cellWidth, self.app.cellHeight))
        self.app.screen.blit(self.ghostImage, (int(self.pixCoord.x-indent//5),int(self.pixCoord.y-indent//5)))
    

    def ghostGoat(self):
        if self.mode == "random":
            if self.app.player.gridCoord[0] > 28//2 and self.app.player.gridCoord[1] > 30//2:
                return vec(1, 1)
            if self.app.player.gridCoord[0] > 28//2 and self.app.player.gridCoord[1] < 30//2:
                return vec(1, 30-4)
            if self.app.player.gridCoord[0] < 28//2 and self.app.player.gridCoord[1] > 30//2:
                return vec(28-2, 1)
            else:
                return vec(28-2, 30-2)

    def inGridMove(self):
        if int(self.pixCoord.x+indent//2) % self.app.cellWidth == 0:
            if self.ghostDirection == vec(1, 0) or self.ghostDirection == vec(-1, 0) or self.ghostDirection == vec(0, 0):
                return True
        if int(self.pixCoord.y+indent//2) % self.app.cellHeight == 0:
            if self.ghostDirection == vec(0, 1) or self.ghostDirection == vec(0, -1) or self.ghostDirection == vec(0, 0):
                return True
        return False

    def move(self):
        if self.mode == "speedy":
            self.ghostDirection = self.get_path_direction(self.goal)
        if self.mode == "random":
             self.ghostDirection = self.ghostRandomMove()

    def ghostRandomMove(self):
        while True:
            number = random.randint(0, 3)
            if number == 0:
                x_dir, y_dir = 1, 0
            elif number == 1:
                x_dir, y_dir = 0, 1
            elif number == 2:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.gridCoord.x + x_dir, self.gridCoord.y + y_dir)
            # if self.app.wallsImage == "walls2.txt" or self.app.wallsImage == "walls3.txt":
            #     if vec(self.gridCoord.x, self.gridCoord.y) == vec(0, 13):
            #         self.pixCoord = vec(530, 295)
            #     if vec(self.gridCoord.x, self.gridCoord.y) == vec(28, 13):
            #         self.pixCoord = vec(70, 295)
            #     if next_pos not in self.app.lvlWalls:
            #         break
            # else:
            if next_pos not in self.app.lvlWalls:
                break
        return vec(x_dir, y_dir)

    def set_target(self):
        return self.app.player.gridCoord

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        # xdir = next_cell[1] - self.gridCoord[0]
        # ydir = next_cell[0] - self.gridCoord[1]
        # xdir = next_cell[0] - self.gridCoord[0]
        # ydir = next_cell[1] - self.gridCoord[1]
        # return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for step in self.app.lvlWalls:
            if step[0] < 28 and step[1] < 30:
                grid[int(step[1])][int(step[0])] = 1
        # path = self.mini.mini(grid, (int(self.gridCoord[1]), int(self.gridCoord[0])), (int(target[1]), int(target[0])))
        # path = self.Alg([int(self.gridCoord[0]), int(self.gridCoord[1])], [int(target[0]), int(target[1])])
        #return path[1]

    def ghostMode(self):
        if self.number == 0 or self.number == 2:
            return "random"
        else:
         return "speedy"


    
