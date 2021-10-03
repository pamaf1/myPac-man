import pygame
vec = pygame.math.Vector2
from player import *
from set import *
from ghost import *
from BFS import *
from DFS import *
from UCS import *
from Astar import *
from lvl import *
import time

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((width, height))
        self.stage = "start"
        self.lvlPlay = 1
        self.index = 0
        self.running = True
        self.lvlWalls = []
        self.points = []
        self.ghosts = []
        self.cellWidth = lvlWidth//28
        self.cellHeight = lvlHeight//30
        self.ghostsCoord = []
        self.playerCoord = None
        self.map = randomWalls()
        self.bfs = BFS(self)
        self.dfs = DFS(self)
        self.ucs = UCS(self)
        self.aStar = Astar(None, None)
        self.createMap() 
        self.player = Player(self, vec(self.playerCoord))
        self.clock = pygame.time.Clock()
        self.createGhosts()
    
    def run(self):
        while self.running:
            if self.stage == "start":
                self.startMenu()
            elif self.stage == "play":
                self.playEvents()
                self.playerMoving()
                self.showObject()
            elif self.stage == "lose":
                self.loseEvents()
                self.loseMenu()
            elif self.stage == "win":
                self.winEvents()
                self.winMenu()
            else:
                self.running = False
            self.clock.tick(speed)
        pygame.quit()

    def showText(self, screen, text, coordinate, textStyle, textSize, textColor):
        style = pygame.font.SysFont(textStyle, textSize)
        screen.blit(style.render(text, True, textColor), coordinate)

    def createMap(self):
        self.screen.fill((0,0,0))
        self.lvl = pygame.image.load('image/back.jpg')
        self.lvl = pygame.transform.scale(self.lvl, (lvlWidth, lvlHeight))
        
        # if self.lvlPlay == 2:
        #     self.wallsImage = "walls2.txt"
        # elif self.lvlPlay == 3:
        #     self.wallsImage = "walls3.txt"
        # else:
        #     self.wallsImage = self.map.createRandomLvl()

        # self.wallsImage = self.map.createRandomLvl(13, 7)

        with open("randomWalls.txt", "r") as file:
            for y, line in enumerate(file):
                for x, element in enumerate(line):
                    if element == "t":
                        self.lvlWalls.append(vec(x, y))
                    elif element == "p":
                        self.points.append(vec(x, y))
                    elif element == "P":
                        self.playerCoord = [x, y]
                    elif element in ["1", "2", "3", "4"]:
                        self.ghostsCoord.append([x, y])
        
        # for y in range(30):
        #     for x in range(28):
        #         num = random.randint(0,2)
        #         if y == 0 or y == 29  or x == 0 or x == 27:
        #             self.lvlWalls.append(vec(x,y))
        #         elif y == 21 and x == 15:
        #             self.playerCoord = [x, y]
        #         elif y == 15 and x >= 12 and x <= 22:
        #             self.ghostsCoord.append([x, y])
        #         else:
        #             if num == 1:
        #                 self.lvlWalls.append(vec(x,y))
        #             else:
        #                 self.points.append(vec(x, y))

    def updateMap(self):
        for walls in self.lvlWalls:
            pygame.draw.rect(self.screen, (0, 0, 255), (walls.x*self.cellWidth+indent//2, walls.y*self.cellHeight+indent//2, self.cellWidth, self.cellHeight))
        
        self.changeAlgorithm()

    
    def createGhosts(self):
        for id, coord in enumerate(self.ghostsCoord):
            self.ghosts.append(Ghost(self, vec(coord), id))

    def startMenu(self):
        self.screen.fill((0,0,0))
        self.showText(self.screen, "Нажмите SPACE, чтобы начать играть", [
                       width//4.5+5, height//2.5], "bremen bd bt", 30, (0, 255, 0))
        self.showText(self.screen, "Нажмите ESCAPE, чтобы закрыть игру", [
                       width//4.5, height//2.5+70], "bremen bd bt", 30, (128, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.stage = "play"

        pygame.display.update()

    def playerMoving(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()

        for ghost in self.ghosts:
            if ghost.gridCoord == self.player.gridCoord:
                self.playerLostLife()

    def playerLostLife(self):
        self.player.playerLife -= 1
        if self.player.playerLife == 0:
            self.stage = "lose"
        else:
            self.player.gridCoord = vec(self.player.playerStartCoord)
            self.player.pixCoord = self.player.getPixCoord()
            self.player.direction *= 0
            for ghost in self.ghosts:
                ghost.gridCoord = vec(ghost.ghostStartCoord)
                ghost.pixCoord = ghost.getPixCoord()
                ghost.ghostDirection *= 0


    def showObject(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.lvl, (indent//2,indent//2))
        self.updateMap()
        self.showPoints()
        self.showText(self.screen, f"Score: {self.player.Score}", [10, 2], "bremen bd bt", 30, (255, 255, 255))
        self.player.drawPlayer()
        for ghost in self.ghosts:
            ghost.drawGhosts()
        pygame.display.update()

    
    def playEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # if event.key == pygame.K_LEFT:
                #     self.player.playerMove(vec(-1,0))
                # if event.key == pygame.K_RIGHT:
                #     self.player.playerMove(vec(1,0))
                # if event.key == pygame.K_UP:
                #     self.player.playerMove(vec(0,-1))
                # if event.key == pygame.K_DOWN:
                #     self.player.playerMove(vec(0,1))
                if event.key == pygame.K_z:
                    self.index += 1
                    if self.index == 4:
                        self.index = 0
    
    def showPoints(self):
        self.pointImage = pygame.image.load('image/dot.png')
        self.pointImage = pygame.transform.scale(self.pointImage, (self.cellWidth, self.cellHeight))
        for point in self.points:
            self.screen.blit(self.pointImage, (int(point.x*self.cellWidth)+indent//2,
                                int(point.y*self.cellHeight)+indent//2))
            # pygame.draw.circle(self.screen, (255, 255, 204),
            #                    (int(point.x*self.cellWidth)+self.cellWidth//2+indent//2,
            #                     int(point.y*self.cellHeight)+self.cellHeight//2+indent//2), 5)

    def resetLevel(self):
        self.screen.fill((0,0,0))
        self.player.playerLife = 3
        self.player.Score = 0
        self.player.gridCoord = vec(self.player.playerStartCoord)
        self.player.pixCoord = self.player.getPixCoord()
        self.player.direction *= 0
        for ghost in self.ghosts:
            ghost.gridCoord = vec(ghost.ghostStartCoord)
            ghost.pixCoord = ghost.getPixCoord()
            ghost.ghostDirection *= 0

        # if self.lvlPlay == 2:
        #     self.wallsImage = "walls2.txt"
        # elif self.lvlPlay == 3:
        #     self.wallsImage = "walls3.txt"
        # else:
        #     self.wallsImage = "walls.txt"

        self.wallsImage = self.map.createRandomLvl(13, 7)
        
        self.playerCoord = None
        self.lvlWalls = []
        self.points = []
        self.ghostsCoord = []

        with open(f"{self.wallsImage}", 'r') as file:
            for y, line in enumerate(file):
                for x, element in enumerate(line):
                    if element == "p":
                        self.points.append(vec(x, y))
                    if element == "t":
                        self.lvlWalls.append(vec(x, y))
                    elif element == "P":
                        self.playerCoord = [x, y]
                    elif element in ["1", "2", "3", "4"]:
                        self.ghostsCoord.append([x, y])
        self.stage = "play"

    def loseEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.resetLevel()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def loseMenu(self):
        self.screen.fill((0,0,0))
        self.showText(self.screen, "Конец игры(", [240, 100], "bremen bd bt", 30, (128, 0, 0))
        self.showText(self.screen, "Нажмите SPACE, чтобы играть снова", [
                       width//4.5+5, height//2.5], "bremen bd bt", 30, (0, 255, 0))
        self.showText(self.screen, "Нажмите ESCAPE, чтобы закрыть игру", [
                       width//4.5, height//2.5+70], "bremen bd bt", 30, (128, 0, 0))
        pygame.display.update()

    def winEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.lvlPlay += 1
                self.resetLevel()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def winMenu(self):
        self.screen.fill((0,0,0))
        self.showText(self.screen, "Победа)", [250, 100], "bremen bd bt", 30, (0, 255, 0))
        self.showText(self.screen, "Нажмите SPACE, чтобы играть снова", [
                       width//4.5+5, height//2.5], "bremen bd bt", 30, (0, 255, 0))
        self.showText(self.screen, "Нажмите ESCAPE, чтобы закрыть игру", [
                       width//4.5, height//2.5+70], "bremen bd bt", 30, (128, 0, 0))
        
        pygame.display.update()

    def changeAlgorithm(self):
        if self.index == 1: 
            start = time.time()
            for ghost in self.ghosts:
                self.bfs.BFS([int(self.player.gridCoord.x), int(self.player.gridCoord.y)], [int(ghost.gridCoord.x), int(ghost.gridCoord.y)]) 
            self.showText(self.screen, f'Время: {(time.time() - start)}', [
                       370, 650], "bremen bd bt", 20, (192, 192, 192))
                       
            # grid = [[0 for x in range(28)] for x in range(30)]
            # for step in self.lvlWalls:
            #     if step[0] < 28 and step[1] < 30:
            #         grid[int(step[1])][int(step[0])] = 1

            # path = self.aStar.astar(grid, (int(self.player.gridCoord.y), int(self.player.gridCoord.x)), (int(self.points[len(self.points)-1][1]), int(self.points[len(self.points)-1][0])))
            # for step in path:
            #     pygame.draw.rect(self.screen, (167,167,0), (step[1] * self.cellWidth + indent//2, step[0] * self.cellHeight + indent//2, self.cellWidth, self.cellHeight), 2)

            # grid = [[0 for x in range(28)] for x in range(30)]
            # for step in self.lvlWalls:
            #     if step[0] < 28 and step[1] < 30:
            #         grid[int(step[1])][int(step[0])] = 1

            # # path = []
            # for ghost in self.ghosts:
            #     path = self.aStar.astar(grid, (int(self.player.gridCoord.y), int(self.player.gridCoord.x)), (int(ghost.gridCoord.y), int(ghost.gridCoord.x)))
            #     for step in path:
            #         pygame.draw.rect(self.screen, (167,167,0), (step[1] * self.cellWidth + indent//2, step[0] * self.cellHeight + indent//2, self.cellWidth, self.cellHeight), 2)
        
        elif self.index == 2:
            start = time.time()
            for ghost in self.ghosts:
                self.dfs.DFS([int(self.player.gridCoord.x), int(self.player.gridCoord.y)], [int(ghost.gridCoord.x), int(ghost.gridCoord.y)])
            self.showText(self.screen, f'Время: {(time.time() - start)}', [
                       370, 650], "bremen bd bt", 20, (192, 192, 192))
        elif self.index == 3:
            start = time.time()
            for ghost in self.ghosts:
                self.ucs.UCS([int(self.player.gridCoord.x), int(self.player.gridCoord.y)], [int(ghost.gridCoord.x), int(ghost.gridCoord.y)])
            self.showText(self.screen, f'Время: {(time.time() - start)}', [
                       370, 650], "bremen bd bt", 20, (192, 192, 192))
    

app = App()
app.run()