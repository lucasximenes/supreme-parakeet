'''
baseando no algo do g4g: https://www.geeksforgeeks.org/a-search-algorithm/
provavelmente dá pra otimizar o openList, vou dar uma olhada
'''

class Game:
    def __init__(self):
        self.map = []
        self.bases = []
        self.pokemons = {'Pikachu': 1.5, 'Bulbassauro': 1.4, 'Rattata': 1.3,
        'Caterpie': 1.2, 'Weedle': 1.1}
        for i in range(12):
            if i < 10:
                self.bases.append(55 + i*5)
            else:
                self.bases.append(55 + (i+1)*5)
    
    def setPokeStrenght(self, pokemon: str, val: float):
        self.pokemons[pokemon] = val
    
    def setBaseDifficulty(self, base: int, difficulty: int):
        self.bases[base-1] = difficulty

    def readMap(self):
        path = input()
        f = open(path, "r")
        for line in f:
            self.mapa.append(line)
        f.close()

class Cell:
    def __init__(self):
        self.f = 1e10
        self.g = 1e10
        self.h = 1e10
        self.cost = 1e10
        self.parent_x = -1
        self.parent_y = -1
    
    def update(self, x = None, y = None, f = None, g = None, h = None, cost = None):
        if x is not None:
            self.parent_x = x
        
        if y is not None:
            self.parent_y = y
        
        if f is not None:
            self.f = f
        
        if g is not None:
            self.g = g

        if h is not None:
            self.h = h

        if cost is not None:
            self.cost = cost


def inMap(x: int, y: int):
    return (x >= 0) and (y >= 0) and (x < 41) and (y < 41)
    
def manhattanDistance(x: int, y: int, dest_x: int, dest_y: int):
    return abs(x - dest_x) + abs(y - dest_y)

def tracePath(end: int, mapInfo: list):
    x, y = end[0], end[1]
    path = []
    while(mapInfo[x][y].parent_x != x and mapInfo[x][y].parent_y != y):
        path.append((x,y))
        x, y = mapInfo[x][y].parent_x, mapInfo[x][y].parent_y
    path.append((x,y))
    path.reverse()
    return path

def aStar(start, end, map: list):
    if inMap(start[0], start[1]) == False:
        print("Nonexistent inital position\n")
        return
    
    if inMap(end[0], end[1]) == False:
        print("Nonexistent final position\n")
        return
    
    if start == end:
        print("Initial position is the same as the final\n")
        return
    
    closedList = [[False for i in range(41)] for j in range(41)]
    mapInfo = [[Cell() for i in range(41)] for j in range(41)]
    mapInfo[start[0]][start[1]].update(x = start[0], y=start[1])
    openList = []
    openList.append([0, ([start[0], start[1])])
    endFound = False
    while len(openList) > 0:
        node = openList.pop()
        x = node[1][0]
        y = node[1][1]
        f = node[0]
        closedList[x][y] = True
        #Look at north neighbour
        if isValid(x - 1, y) == True:
            if (x - 1, y) == end:
                mapInfo[x - 1][y].parent_x = x
                mapInfo[x - 1][y].parent_y = y
                printf("The destination cell is found\n")
                tracePath(mapInfo, dest)
                foundDest = True
            elif closedList[x - 1][y] == False:
                gNew = mapInfo[x][y].g + mapInfo[x - 1][y].cost
                hNew = manhattanDistance(x - 1, y, end)
                fNew = gNew + hNew
 
                if (mapInfo[x - 1][y].f == 1e10 or mapInfo[x - 1][y].f > fNew):
                    openList.insert([fNew, [x - 1, y]])
                    openList.sort(key=lambda x: x[0], reverse=True)
                    mapInfo[x - 1][y].update(x, y, fNew, gNew, hNew)
        
        #Look at south neighbour
        if isValid(x + 1, y) == True:
            if (x + 1, y) == end:
                mapInfo[x + 1][y].parent_x = x
                mapInfo[x + 1][y].parent_y = y
                printf("The destination cell is found\n")
                tracePath(mapInfo, dest)
                foundDest = True
            elif closedList[x + 1][y] == False:
                gNew = mapInfo[x][y].g + mapInfo[x + 1][y].cost
                hNew = manhattanDistance(x + 1, y, end)
                fNew = gNew + hNew
 
                if (mapInfo[x + 1][y].f == 1e10 or mapInfo[x + 1][y].f > fNew):
                    openList.insert([fNew, [x + 1, y]])
                    openList.sort(key=lambda x: x[0], reverse=True)
                    mapInfo[x + 1][y].update(x, y, fNew, gNew, hNew)
        
        #Look at west neighbour
        if isValid(x, y - 1) == True:
            if (x, y - 1) == end:
                mapInfo[x][y - 1].parent_x = x
                mapInfo[x][y - 1].parent_y = y
                printf("The destination cell is found\n")
                tracePath(mapInfo, dest)
                foundDest = True
            elif closedList[x][y - 1] == False:
                gNew = mapInfo[x][y].g + mapInfo[x][y - 1].cost
                hNew = manhattanDistance(x, y - 1, end)
                fNew = gNew + hNew
 
                if (mapInfo[x][y - 1].f == 1e10 or mapInfo[x][y - 1].f > fNew):
                    openList.insert([fNew, [x, y - 1]])
                    openList.sort(key=lambda x: x[0], reverse=True)
                    mapInfo[x][y - 1].update(x, y, fNew, gNew, hNew)
        
        #Look at east neighbour
        if isValid(x, y + 1) == True:
            if (x, y) == end:
                mapInfo[x][y + 1].parent_x = x
                mapInfo[x][y + 1].parent_y = y
                printf("The destination cell is found\n")
                tracePath(mapInfo, dest)
                foundDest = True
            elif closedList[x][y + 1] == False:
                gNew = mapInfo[x][y].g + mapInfo[x][y + 1].cost
                hNew = manhattanDistance(x, y + 1, end)
                fNew = gNew + hNew
 
                if (mapInfo[x][y + 1].f == 1e10 or mapInfo[x][y + 1].f > fNew):
                    openList.insert([fNew, [x, y + 1]])
                    openList.sort(key=lambda x: x[0], reverse=True)
                    mapInfo[x][y + 1].update(x, y, fNew, gNew, hNew)

    if foundDest == False:
        print("Could not find your destination")
    return
