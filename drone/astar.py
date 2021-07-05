class Cell:
    def __init__(self, cost = 1e10):
        self.f = 1e10
        self.g = 1e10
        self.h = 1e10
        self.cost = cost
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

def numerify(val):
    if val == 'M':
        return 200
    elif val == 'R':
        return 5
    elif val == '.':
        return 1
    else:
        return 0

def inMap(x: int, y: int):
    return (x >= 0) and (y >= 0) and (x < 58) and (y < 33)
    
def manhattanDistance(x: int, y: int, dest):
    return (abs(x - dest[0]) + abs(y - dest[0]))/2

def tracePath(mapInfo, end):
    x, y = end[0], end[1]
    totalCost = 0
    path = []
    while(mapInfo[x][y].parent_x != x or mapInfo[x][y].parent_y != y):
        path.append((x,y))
        totalCost += mapInfo[x][y].cost
        x, y = mapInfo[x][y].parent_x, mapInfo[x][y].parent_y
    path.append((x,y))
    path.reverse()
    return path, totalCost

def aStar(start, end, gameMap: list, heuristicFunction):
    if inMap(start[0], start[1]) == False:
        print("Nonexistent inital position\n")
        return
    
    if inMap(end[0], end[1]) == False:
        print("Nonexistent final position\n")
        return
    
    if start == end:
        print("Initial position is the same as the final\n")
        return
    
    numericalMap = [list(map(numerify, gameMap[i])) for i in range(58)] # mapa dos custos
    closedList = [[False for i in range(33)] for j in range(58)]
    mapInfo = [[Cell(cost=numericalMap[j][i]) for i in range(33)] for j in range(58)]
    mapInfo[start[0]][start[1]].update(x = start[0], y=start[1], f=0, g=0, h=0, cost=0)
    openList = []
    openList.append([0, [start[0], start[1]]])

    while len(openList) > 0:
        node = openList.pop()
        x = node[1][0]
        y = node[1][1]
        f = node[0]
        closedList[x][y] = True
        #Look at north neighbour
        if inMap(x - 1, y) == True:
            if (x - 1, y) == end:
                mapInfo[x - 1][y].parent_x = x
                mapInfo[x - 1][y].parent_y = y
                print("The destination cell is found\n")
                return tracePath(mapInfo, end)
                
            elif closedList[x - 1][y] == False:
                gNew = mapInfo[x][y].g + mapInfo[x - 1][y].cost
                hNew = heuristicFunction(x - 1, y, end)
                fNew = gNew + hNew
 
                if (mapInfo[x - 1][y].f == 1e10 or mapInfo[x - 1][y].f > fNew):
                    openList.append([fNew, [x - 1, y]])
                    mapInfo[x - 1][y].update(x, y, fNew, gNew, hNew)
        
        #Look at south neighbour
        if inMap(x + 1, y) == True:
            if (x + 1, y) == end:
                mapInfo[x + 1][y].parent_x = x
                mapInfo[x + 1][y].parent_y = y
                print("The destination cell is found\n")
                return tracePath(mapInfo, end)

            elif closedList[x + 1][y] == False:
                gNew = mapInfo[x][y].g + mapInfo[x + 1][y].cost
                hNew = heuristicFunction(x + 1, y, end)
                fNew = gNew + hNew
 
                if (mapInfo[x + 1][y].f == 1e10 or mapInfo[x + 1][y].f > fNew):
                    openList.append([fNew, [x + 1, y]])
                    mapInfo[x + 1][y].update(x, y, fNew, gNew, hNew)
        
        #Look at west neighbour
        if inMap(x, y - 1) == True:
            if (x, y - 1) == end:
                mapInfo[x][y - 1].parent_x = x
                mapInfo[x][y - 1].parent_y = y
                print("The destination cell is found\n")
                return tracePath(mapInfo, end)

            elif closedList[x][y - 1] == False:
                gNew = mapInfo[x][y].g + mapInfo[x][y - 1].cost
                hNew = heuristicFunction(x, y - 1, end)
                fNew = gNew + hNew
 
                if (mapInfo[x][y - 1].f == 1e10 or mapInfo[x][y - 1].f > fNew):
                    openList.append([fNew, [x, y - 1]])
                    mapInfo[x][y - 1].update(x, y, fNew, gNew, hNew)
        
        #Look at east neighbour
        if inMap(x, y + 1) == True:
            if (x, y) == end:
                mapInfo[x][y + 1].parent_x = x
                mapInfo[x][y + 1].parent_y = y
                print("The destination cell is found\n")
                return tracePath(mapInfo, end)

            elif closedList[x][y + 1] == False:
                gNew = mapInfo[x][y].g + mapInfo[x][y + 1].cost
                hNew = heuristicFunction(x, y + 1, end)
                fNew = gNew + hNew
 
                if (mapInfo[x][y + 1].f == 1e10 or mapInfo[x][y + 1].f > fNew):
                    openList.append([fNew, [x, y + 1]])
                    mapInfo[x][y + 1].update(x, y, fNew, gNew, hNew)
        
        openList.sort(key=lambda x: x[0], reverse=True)
    
    print("Could not find your destination")
    return