import pygame
import numpy as np
vec = pygame.math.Vector2
from collections import deque 
from set import *
from queue import PriorityQueue
from collections import deque 


class UCS:   
    def __init__(self, app):
        self.app = app

    def UCS(self, start, target):
        grid = np.zeros((30, 28))
        visited = np.zeros((30,28))
        cost = np.zeros((30,28))
        for step in self.app.lvlWalls:
            if step[0] < 28 and step[1] < 30:
                grid[int(step[1])][int(step[0])] = 1

        paths = []

        for j in range(30*30):
            paths.append([0,0])
        
        queue = deque()

        bestPath = []
        bestCost = 50000 
        
        queue.append(start)

        while queue:
            current = queue.popleft()
            currentCost = -1

            for point in self.app.points:
                if point[0] == current[0] and point[1] == current[1]:
                    currentCost -= 1

            if current[0] == target[0] and current[1] == target[1]:
                if bestCost > cost[current[1]][current[0]]:
                    bestCost = cost[current[1]][current[0]]
                    bestPath = []
                    saveCur = current
        
                    while saveCur[0] != start[0] or saveCur[1] != start[1]:
                        saveCur[0] = paths[saveCur[0] * 30 + saveCur[1]][0]
                        saveCur[1] = paths[saveCur[0] * 30 + saveCur[1]][1]
                        bestPath.append([saveCur[0], saveCur[1]])

            besides = [[1, 0], [-1, 0]]
            for beside in besides:
                 if beside[0] + current[0] >= 0 and visited[current[1]][beside[0] + current[0]] == 0 and beside[0] + current[0] < 28:
                        if grid[current[1]][beside[0] + current[0]] != 1:
                            paths[(beside[0] + current[0])*30 + current[1]] = [current[0], current[1]]
                            visited[current[1]][beside[0] + current[0]] = 1
                            cost[current[1]][beside[0] + current[0]] -= currentCost
                            queue.append([beside[0] + current[0], current[1]])
                                
            besides2 = [[0, -1], [0, 1]]
            for beside in besides2:
                    if beside[1] + current[1] >= 0 and visited[beside[1] + current[1]][current[0]] == 0 and beside[1] + current[1] < 30:
                        if grid[beside[1] + current[1]][current[0]] != 1:
                            paths[(current[0])*30 + beside[1] + current[1]] = [current[0], current[1]]
                            visited[beside[1] + current[1]][current[0]] = 1
                            cost[beside[1] + current[1]][current[0]] -= currentCost
                            queue.append([current[0], beside[1] + current[1]])

        for step in bestPath:
            pygame.draw.rect(self.app.screen, (127,0,127), (step[0] * self.app.cellWidth + indent//2, step[1] * self.app.cellHeight + indent//2, self.app.cellWidth, self.app.cellHeight), 2)
