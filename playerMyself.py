import pygame
from set import *
vec = pygame.math.Vector2
import random
from Astar import *


class Player():
    def __init__(self, app, coord):
        self.app = app
        self.aStar = Astar(None, None)
        self.gridCoord = coord
        self.playerStartCoord = [coord.x, coord.y]
        self.pixCoord = self.getPixCoord()
        self.Score = 0
        self.direction = vec(0,0)
        self.goal = None
        self.speed = 2
        self.playerLife = 3

    def update(self):
        self.goal = self.set_target()
        if self.goal != self.gridCoord:
            self.pixCoord += self.direction* self.speed
            if self.Score % 10 == 0:
                random.shuffle(self.app.points)
            if self.inGridMove():
                self.move()

        self.gridCoord[0] = (self.pixCoord[0]- indent +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridCoord[1] = (self.pixCoord[1]- indent +
                            self.app.cellHeight//2)//self.app.cellHeight+1
        if self.playerMeetPoint() == True:
            self.playerEatPoint()


    def getPixCoord(self):
        return  vec((self.gridCoord[0]*self.app.cellWidth)+indent//2+self.app.cellWidth//2,
                   (self.gridCoord[1]*self.app.cellHeight) +
                   indent//2+self.app.cellHeight//2)

    def drawPlayer(self): 
        if self.direction == vec(1, 0):
            image = 'image/Original_PacMan2.png'
        if self.direction == vec(-1, 0):
            image = 'image/Original_PacMan1.png'
        if self.direction == vec(0, 1):
            image = 'image/Original_PacMan3.png'
        if self.direction == vec(0, -1):
            image = 'image/Original_PacMan4.png'
        if self.direction == vec(0, 0):
            image = 'image/Original_PacMan2.png'
        self.playerImage = pygame.image.load(image)
        self.playerImage = pygame.transform.scale(self.playerImage, (self.app.cellWidth, self.app.cellHeight))
        self.app.screen.blit(self.playerImage, (int(self.pixCoord.x-indent//5),int(self.pixCoord.y-indent//5)))

        for i in range(self.playerLife):
            pygame.draw.circle(self.app.screen, (190, 194, 15), (50 + 30*i, height - 15), 7)

    def inGridMove(self):
        if int(self.pixCoord.x+indent//2) % self.app.cellWidth == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixCoord.y+indent//2) % self.app.cellHeight == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    
    def playerMeetPoint(self):
        if self.gridCoord in self.app.points:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                return True
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def playerEatPoint(self):
        self.app.points.remove(self.gridCoord)
        self.Score += 1
        if len(self.app.points) == 0:
            self.app.stage = "win"

    def move(self):
        self.direction = self.get_path_direction(self.goal)

    def set_target(self):
        # if self.Score % 2 == 0:
        #     number = random.randint(0,len(self.app.points)-1)
        #     return self.app.points[number]
        # else:
        #     return self.app.points[0]
        return self.app.points[0]

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[1] - self.gridCoord[0]
        ydir = next_cell[0] - self.gridCoord[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for step in self.app.lvlWalls:
            if step[0] < 28 and step[1] < 30:
                grid[int(step[1])][int(step[0])] = 1
        
        path = self.aStar.astar(grid, (int(self.gridCoord[1]), int(self.gridCoord[0])), (int(target[1]), int(target[0])))
        return path[1]
