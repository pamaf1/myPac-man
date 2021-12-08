import pygame
vec = pygame.math.Vector2
from set import *

class Astar:
    
    def __init__(self, beforeCoordinate, coordinate):
        self.beforeCoordinate = beforeCoordinate
        self.coordinate = coordinate
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.coordinate == other.coordinate

    def astar(self, grid, start, end):
        indexList = []
        nodeList = []

        currentStage = 0
        neighbours = ((0, -1), (0, 1), (-1, 0), (1, 0))
        maxStage = (len(grid) // 2) ** 2

        endSearch = Astar(None, end)
        startSearch = Astar(None, start)
        startSearch.g = startSearch.h = startSearch.f = 0
        endSearch.g = endSearch.h = endSearch.f = 0
        indexList.append(startSearch)

        while len(indexList) > 0:
            currentStage += 1
            currentNode = indexList[0]
            currentIndex = 0

            for index, item in enumerate(indexList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index
                    
            if currentStage > maxStage:
                path = []
                current = currentNode
                
                while current is not None:
                    path.append(current.coordinate)
                    current = current.beforeCoordinate
                return path[::-1] 

            indexList.pop(currentIndex)
            nodeList.append(currentNode)

            if currentNode == endSearch:
                path = []
                current = currentNode
                
                while current is not None:
                    path.append(current.coordinate)
                    current = current.beforeCoordinate
                return path[::-1]

            children = []

            for next in neighbours:
                currenNodeCoordinate = (currentNode.coordinate[0] + next[0], currentNode.coordinate[1] + next[1])

                inGraph = [currenNodeCoordinate[0] > (len(grid) - 1), currenNodeCoordinate[0] < 0, currenNodeCoordinate[1] > (len(grid[len(grid) - 1]) - 1), currenNodeCoordinate[1] < 0]
                
                if any(inGraph):
                    continue
                if grid[currenNodeCoordinate[0]][currenNodeCoordinate[1]] != 0:
                    continue

                newSearch = Astar(currentNode, currenNodeCoordinate)

                children.append(newSearch)

            for child in children:
                if len([nodeChild for nodeChild in nodeList if nodeChild == child]) > 0:
                    continue

                child.g = currentNode.g + 1
                child.h = ((child.coordinate[0] - endSearch.coordinate[0]) ** 2) + ((child.coordinate[1] - endSearch.coordinate[1]) ** 2)
                child.f = child.g + child.h

                if len([indexChild for indexChild in indexList if child == indexChild and child.g > indexChild.g]) > 0:
                    continue

                indexList.append(child)
