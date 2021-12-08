from ghost import *
from pygame.locals import *
from app import *


class Algorithm(object):
    def __init__(self, grid, ghosts, points, algo):
        self.grid = grid
        self.visited = []
        self.graph = {}
        self.ghosts = ghosts
        self.points = points
        self.max = 100000000
        self.min = -100000000
        self.algo = algo

    def minimax(self, depth, current, maximizing_player, alpha, beta, path):

        neighbour_count = list(set(self.graph[current].keys()) - set(path))
        if depth == 0 or len(neighbour_count) == 0:
            return self.getScore(path)

        if maximizing_player:

            best = self.min
            best_path = path.copy()


            for vertex in list(set(self.graph[current].keys()) - set(path)):
                path.append(vertex)
                val = self.minimax(depth - 1, vertex, False, alpha, beta, path)
                best = max(best, val[0])
                if best == val[0]:
                    best_path.append(vertex)
                path.remove(vertex)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best, best_path

        else:
            best = self.max
            best_path = path.copy()

            for vertex in list(set(self.graph[current].keys()) - set(path)):
                path.append(vertex)
                val = self.minimax(depth - 1, vertex, True, alpha, beta, path)
                best = min(best, val[0])
                if best == val[0]:
                    best_path.append(vertex)
                path.remove(vertex)
                beta = min(beta, best)

                if beta <= alpha:
                    break
            return best, best_path

    def expectimax(self, depth, current, path, is_max):
        neighbour_count = list(set(self.graph[current].keys()) - set(path))
        if depth == 0 or len(neighbour_count) == 0:
            return self.getScore(path)

        if is_max:
            best = self.min
            best_path = path.copy()

            for vertex in self.graph[current].keys():
                path.append(vertex)
                val = self.expectimax(depth-1, vertex, path, False)
                if best < val[0]:
                    best_path.append(vertex)
                    best = val[0]
                path.remove(vertex)
            return best, best_path
        else:
            best = 0
            best_path = path.copy()

            count = 0
            for vertex in self.graph[current].keys():
                path.append(vertex)
                count += 1
                best += self.expectimax(depth - 1, vertex, path, True)[0]
                path.remove(vertex)
            if count != 0:
                best = best/count
            return best, best_path


    def getScore(self, path):
        priority = 0
        for vertex in path:
            index = path.index(vertex)
            if index + 1 < len(path):
                next = path[index + 1]
                for point in self.points:
                    if vertex.position.x == next.position.x == point.position.x:
                        if point.position.y in range(vertex.position.y, next.position.y) or \
                                point.position.y in range(next.position.y, vertex.position.y):
                            priority += 10
                    if vertex.position.y == next.position.y == point.position.y:
                        if point.position.x in range(vertex.position.x, next.position.x) or \
                                point.position.x in range(next.position.x, vertex.position.x):
                            priority += 10
            if vertex in self.ghosts.get_road_blocks():
                priority -= 100
        return priority, path

    def getPath(self, path, start, goal):
        road = []
        current = goal
        while current != start:
            road.append(current)
            current = path[current]
        road.reverse()
        return road

