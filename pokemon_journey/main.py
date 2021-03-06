'''
código do A* baseando no algo do g4g: https://www.geeksforgeeks.org/a-search-algorithm/
'''
from itertools import product
import math

class Game:
    def __init__(self):
        self.gameMap = []
        self.start = (0, 0)
        self.end = (0, 0)
        self.pokemons = {4: 1.5, 3: 1.4, 2: 1.3,
        1: 1.2, 0: 1.1}
        self.bases = [55,60,65,70,75,80,85,90,95,100,110,120]
    
    def setPokeStrength(self, pokemon: str, val: float):
        self.pokemons[pokemon] = val
    
    def setBaseDifficulty(self, base: int, difficulty: int):
        self.bases[base-1] = difficulty

    def setStart(self, newStart: int):
        self.start = newStart
    
    def setEnd(self, newEnd: int):
        self.end = newEnd
    
    def getPokemonStrength(self, index):
        return self.pokemons[index]

    def getGymDifficulty(self, index):
        return self.bases[index]

    def readMap(self):
        path = input("Digite aqui o caminho para o arquivo .txt do mapa:\n")
        f = open(path, "r")
        j = 0
        for line in f:
            self.gameMap.append(line)
            for i in range(41):
                if line[i] == 'I':
                    self.start = (j, i)
                elif line[i] == 'F':
                    self.end = (j, i)
            j += 1
        f.close()
    
    def getMap(self):
        return self.gameMap
    


class BBGymCell:
    def __init__(self, parent, state, cost, gym, parentObj):
        self.cost = cost
        self.state = state
        self.parent = parent
        self.sons = []
        self.gym = gym
        self.parentObj = parentObj
    
    def renderSons(self, extendedList):
        if self.gym < 11:
            for son in possibleSons:
                boolNeg = False
                newState = [0, 0, 0, 0, 0]
                for i in range(5):
                    res = self.state[i] - son[i]   
                    if res < 0:
                        boolNeg = True
                        break
                    newState[i] = res
                if boolNeg == False:
                    #statestr -> [5, 5, 5, 5, 5] = '55555G' p/ usar como hash de dict
                    statestr = list(map(str, newState)) 
                    statestr.append(str(self.gym+1))
                    statestr = "".join(statestr) 

                    totalStrength = sum([game.getPokemonStrength(i)*son[i] for i in range(5)])
                    if totalStrength > 0:
                        gym = self.gym + 1
                        cost = (game.getGymDifficulty(gym) / totalStrength)
                        self.sons.append(BBGymCell(parent=self.state, state=newState, gym=gym, cost=self.cost + cost, parentObj = self))
        else:
            if sum(self.state) > 0:
                gym = self.gym + 1
                self.sons.append(BBGymCell(parent=self.state, state=self.state, gym=gym, cost=self.cost, parentObj = self))
    
    def getSons(self):
        return self.sons

    def getGym(self):
        return self.gym

    def getCost(self):
        return self.cost

    def getParent(self):
        return self.parent

    def getState(self):
        return self.state
    
    def getParentObj(self):
        return self.parentObj

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

def BBGyms():
    maxGym = 0
    maxGymSon = 0
    openList = []
    finalCost = 1e10
    chosenOne = None
    extendedList = {}
    openList.append(BBGymCell(parent=-1, state=[5, 5, 5, 5, 5], cost=0,  gym=-1, parentObj = None))

    while len(openList) > 0:
        node = openList.pop()
        cost = node.getCost()

        if cost < finalCost:
            if node.getGym() == 12:
                finalCost = cost
                chosenOne = node

            else:
                nodestr = list(map(str, node.getState()))
                nodestr.append('-')
                nodestr.append(str(node.getGym()))
                nodestr = "".join(nodestr)
                
                if extendedList.get(nodestr, False) == False:
                    node.renderSons(extendedList)
                    extendedList[nodestr] = True
                    sons = node.getSons()

                    for son in sons:
                        if(son.getGym()> maxGymSon):
                            maxGymSon = son.getGym()
                        openList.append(son)

                    if(node.getGym() > maxGym):
                        maxGym = node.getGym()
                        
                    print("Tamanho da openList = ", len(openList), " Ginásio atual = ", node.getGym(), " My parent = ", node.getParent(), " Cost = ", node.getCost())
                    openList.sort(key=lambda x: x.getCost(), reverse=True)
            
    return chosenOne


def inMap(x: int, y: int):
    return (x >= 0) and (y >= 0) and (x < 41) and (y < 41)
    
def manhattanDistance(x: int, y: int, dest):
    return (abs(x - dest[0]) + abs(y - dest[0]))/2

def crazyHeuristic(x, y, dest):
    return 0

# 
# Guarda o caminho percorrido
# 
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
    
    numericalMap = [list(map(numerify, gameMap[i])) for i in range(41)] # mapa dos custos
    closedList = [[False for i in range(41)] for j in range(41)]
    mapInfo = [[Cell(cost=numericalMap[j][i]) for i in range(41)] for j in range(41)]
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


game = Game()
# Cria todos os binários de tamanho 0 menos 00000
possibleSons = list(product(range(2), repeat = 5)) 
possibleSons.remove((0, 0, 0, 0, 0))

if __name__ == '__main__':
    game.readMap()
    gameMap = game.getMap()
    path, totalCost = aStar(game.start, game.end, gameMap, manhattanDistance)
    f = open("path.txt", "w")

    for coord in path:
        f.write(f"{coord[0]},{coord[1]}\n")
        s = list(gameMap[coord[0]])
        s[coord[1]] = '@'
        gameMap[coord[0]] = "".join(s)
    f.close()
    finalGymState = BBGyms()
    print("CUSTO FINAL É:", finalGymState.getCost())

    while(finalGymState.getParentObj() != None):
        parent = finalGymState.getParentObj()
        print(finalGymState.getState())
        print(f"Custo desse Gym é {finalGymState.getCost() - parent.getCost()}")
        finalGymState = parent