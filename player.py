import pygame
from set import *
vec = pygame.math.Vector2

class Player():
    def __init__(self, app, coord):
        self.app = app
        self.gridCoord = coord
        self.playerStartCoord = [coord.x, coord.y]
        self.pixCoord = self.getPixCoord()
        self.direction = vec(0,0)
        self.Score = 0
        self.saveDirection = None
        self.allowedToMove = True
        self.playerSpeed = 2
        self.playerLife = 3

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

    def getPixCoord(self):
        return  vec((self.gridCoord[0]*self.app.cellWidth)+indent//2+self.app.cellWidth//2,
                   (self.gridCoord[1]*self.app.cellHeight) +
                   indent//2+self.app.cellHeight//2)

    def update(self):
        
        if self.allowedToMove:
            self.pixCoord += self.direction*self.playerSpeed 
        if self.inGridMove():
            if self.saveDirection != None:
                self.direction = self.saveDirection
            self.allowedToMove = self.notInWallsMove()

        self.gridCoord[0] = (self.pixCoord[0]- indent +
                            self.app.cellWidth//2)//self.app.cellWidth+1
        self.gridCoord[1] = (self.pixCoord[1]- indent +
                            self.app.cellHeight//2)//self.app.cellHeight+1

        if self.playerMeetPoint() == True:
            self.playerEatPoint()


    def playerMeetPoint(self):
        if self.gridCoord in self.app.points:
            if int(self.pixCoord.x + indent//2) % self.app.cellWidth == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pixCoord.y+indent//2) % self.app.cellHeight == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                    return True
        return False

    def playerEatPoint(self):
        self.app.points.remove(self.gridCoord)
        self.Score += 1
        if len(self.app.points) == 0:
            self.app.stage = "win"

    def playerMove(self, direction):
        self.saveDirection = direction

    def inGridMove(self):
        if int(self.pixCoord.x+indent//2) % self.app.cellWidth == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixCoord.y+indent//2) % self.app.cellHeight == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def notInWallsMove(self):
        for wall in self.app.lvlWalls:
            # if self.app.wallsImage == "walls2.txt" or self.app.wallsImage == "walls3.txt":
            #     if vec(self.gridCoord+self.direction) == vec(-2, 13):
            #         self.pixCoord = vec(615, 295)
            #     if vec(self.gridCoord+self.direction) == vec(30, 13):
            #         self.pixCoord = vec(15, 295)
            #     if vec(self.gridCoord+self.direction) == wall:
            #         return False
            # else:
            if vec(self.gridCoord+self.direction) == wall:
                return False

        return True