import pygame
vec = pygame.math.Vector2
from set import *

class BFS:   

    def __init__(self, app):
        self.app = app

    def BFS(self, start, target):   
        grid = [[0 for x in range(28)] for x in range(30)]
        for step in self.app.lvlWalls:
            if step.x < 28 and step.y < 30:
                grid[int(step.y)][int(step.x)] = 1

        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                besides = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for beside in besides:
                    if beside[0] + current[0] >= 0 and beside[0] + current[0] < len(grid[0]):
                        if beside[1] + current[1] >= 0 and beside[1] + current[1] < len(grid):
                            nextCell = [beside[0] + current[0], beside[1] + current[1]]
                            if nextCell not in visited:
                                if grid[nextCell[1]][nextCell[0]] != 1:
                                    queue.append(nextCell)
                                    path.append({"Current": current, "Next": nextCell})
        bestPath = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    bestPath.insert(0, step["Current"])
         
        for step in bestPath:
            pygame.draw.rect(self.app.screen, (107,107,107), (step[0] * self.app.cellWidth + indent//2, step[1] * self.app.cellHeight + indent//2, self.app.cellWidth, self.app.cellHeight), 2)
