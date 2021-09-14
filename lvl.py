from random import shuffle
 

class randomWalls():

    def createRandomLvl(self, widths, heights):

        self.visited = [[0] * widths + [1] for i in range(heights)] + [[1] * (widths + 1)]
        self.verticalLine = [["tp"] * widths + ['tt'] for i in range(heights)]
        self.horizontalLine = [["tt"] * widths + ['tt'] for i in range(heights + 1)]

        def recursiveDfs(x, y):
            self.visited[y][x] = 1
            self.d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(self.d)
            for (x1, y1) in self.d:
                if self.visited[y1][x1]: 
                    continue
                if x1 == x: 
                    self.horizontalLine[max(y, y1)][x] = "tp"
                if y1 == y: 
                    self.verticalLine[y][max(x, x1)] = "pp"
                recursiveDfs(x1, y1)

        recursiveDfs(1, 1)

        self.s = ""
        for (h, v) in zip(self.horizontalLine, self.verticalLine):
            self.s += ''.join(h + ['\n'] + v + ['\n'])

        self.reversed_string = self.s[::-1]

        self.s = 'tttttttttttttttttttttttttttt'+'\n'+self.s+self.reversed_string.lstrip()+'\n'+'tttttttttttttttttttttttttttt'+'\n'+'tttttttttttttttttttttttttttt'
        
        self.walls = list(self.s)
        self.s = ''

        self.walls[410] = 'P'
        self.walls[301] = '1'
        self.walls[302] = '2'
        self.walls[303] = '3'
        self.walls[304] = '4'

        for i in zip(self.walls):
            self.s += ''.join(i)
        
        

        file = open('randomWalls.txt', 'w')
        for index in self.s:
            file.write(index)
        
        file.close()

        return 'randomWalls.txt'

