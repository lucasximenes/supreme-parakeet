'''
baseando no algo do g4g: https://www.geeksforgeeks.org/a-search-algorithm/
provavelmente dá pra otimizar o openList, vou dar uma olhada
jeito de otimizar:
ao invés de fazer sort depois de todo append no open list
é só dar no final do while
'''
from itertools import product
import math

class Game:
    def __init__(self):
        self.gameMap = []
        self.start = (0, 0)
        self.end = (0, 0)
        self.bases = []
        self.pokemons = {4: 1.5, 3: 1.4, 2: 1.3,
        1: 1.2, 0: 1.1}
        for i in range(12):
            if i < 10:
                self.bases.append(55 + i*5)
            else:
                self.bases.append(55 + (i+1)*5)
    
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
    
class GymCell():
    def __init__(self, parent, state, f, g, gym):
        self.f = f
        self.g = g
        self.h = 0
        self.cost = 0
        self.state = state
        self.parent = parent
        self.sons = []
        self.gym = gym
    
    def renderSons(self):
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
                    totalStrength = sum([game.getPokemonStrength(i)*son[i] for i in range(5)])
                    self.cost = (game.getGymDifficulty(self.gym) / totalStrength)
                    gym = self.gym + 1
                    g = self.g + self.cost
                    h = heuristicfunc(newState, gym)
                    f = g + h
                    self.sons.append(GymCell(parent=self.state, state=newState, gym=gym, f=f, g=g))
        else:
            mask = [0, 0, 0, 0, 0]
            newState = self.state
            for i,st in enumerate(self.state):
                if st != 0:
                    newState[i] = self.state[i] - 1
                    mask[i] = 1                    
            totalStrength = sum([game.getPokemonStrength(i)*mask[i] for i in range(5)])
            self.cost = (game.bases[self.gym] / totalStrength)
            gym = self.gym + 1
            g = self.g + self.cost
            h = heuristicfunc(newState, gym)
            if h != 1e10:
                f = g + h
                self.sons.append(GymCell(parent=self.state, state=newState, gym=gym, f=f, g=g))
    
    def getSons(self):
        return self.sons

    def getF(self):
        return self.f

    def getGym(self):
        return self.gym

    def getG(self):
        return self.g

    def getParent(self):
        return self.parent

    def getState(self):
        return self.state


class BBGymCell:
    def __init__(self, parent, state, cost, gym):
        self.cost = cost
        self.state = state
        self.parent = parent
        self.sons = []
        self.gym = gym
    
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
                    if(self.gym == 5):
                        print("\n\n\n\n\n\n\n AQUI \n\n\n\n")
                    if extendedList.get(statestr, False) == False:
                        totalStrength = sum([game.getPokemonStrength(i)*son[i] for i in range(5)])
                        cost = (game.getGymDifficulty(self.gym) / totalStrength)
                        gym = self.gym + 1
                        self.sons.append(BBGymCell(parent=self.state, state=newState, gym=gym, cost=self.cost + cost))
                    else:
                        print("Cai aqui")
        else:
            mask = [0, 0, 0, 0, 0]
            newState = self.state
            for i,st in enumerate(self.state):
                if st != 0:
                    newState[i] = self.state[i] - 1
                    mask[i] = 1                    
            totalStrength = sum([game.getPokemonStrength(i)*mask[i] for i in range(5)])
            if(totalStrength > 0):
                cost = (game.getGymDifficulty(self.gym) / totalStrength)
                gym = self.gym + 1
                self.sons.append(BBGymCell(parent=self.state, state=newState, gym=gym, cost=self.cost + cost))
    
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

def heuristicfunc(state, gym):
    if gym == 12:
        return 0
    soma = sum(state)
    if soma == 0 or soma < 11 - gym:
        return 1e10
    else:
        return 300 - sum([1 if i > 0 else 0 for i in state])*50 - soma


def BBGyms():

    maxGym = 0
    maxGymSon = 0

    openList = []
    finalCost = 1e10
    chosenOne = None
    extendedList = {}
    openList.append(BBGymCell(parent=-1, state=[5, 5, 5, 5, 5], cost=0,  gym=-1))
    while len(openList) > 0:
        node = openList.pop()
        cost = node.getCost()
        if cost < finalCost:
            if node.getGym() == 12:
                finalCost = cost
                chosenOne = node
            nodestr = list(map(str, node.getState()))
            nodestr.append(str(node.getGym()))
            nodestr = "".join(nodestr)
            
            if extendedList.get(nodestr, False) == False:
                
                node.renderSons(extendedList)
                extendedList[nodestr] = True
                sons = node.getSons()
                for son in sons:
                    print(son.getState())


                    if(son.getGym()> maxGym):
                        print("Son greater than max ", son.getGym())
                        maxGymSon = son.getGym()

                    sonstr = list(map(str, son.getState()))
                    sonstr.append(str(son.getGym()))
                    sonstr = "".join(sonstr)



                    # if extendedList.get(sonstr, False) == False:
                    openList.append(son)
                    # else:
                        # print("Pó entrar nao")
                if(node.getGym() > maxGym):
                    maxGym = node.getGym()
                print("Tamanho da openList = ", len(openList), " Ginásio atual = ", node.getGym(), " my daddy = ", node.getParent(), " cost = ", node.getCost())
                print("Maximo ", maxGym, " Maximo son ", maxGymSon)
                print("Nodestr", nodestr, " -- > " , node.getState())

                openList.sort(key=lambda x: x.getCost(), reverse=True)
            
    return chosenOne

def aStarGyms():
    openList = []
    openList.append(GymCell(parent=-1, state=[5, 5, 5, 5, 5], f=0, g=0, gym=-1))
    while len(openList) > 0:
        node = openList.pop()
        if node.getGym() == 12:
            return node
        node.renderSons()
        sons = node.getSons()
        for son in sons:
            openList.append(son)
        print("Tamanho da openList = ", len(openList), " Ginásio atual = ", node.getGym(), " my daddy = ", node.getParent(), " g = ", node.getG(),  " f = ", node.getF())
        openList.sort(key=lambda x: x.getF(), reverse=True)
    
    print("could not find this sh**")
    return

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
possibleSons = list(product(range(2), repeat = 5)) 

possibleSons.remove((0, 0, 0, 0, 0))


for possible in possibleSons:
    print(possible)


if __name__ == '__main__':
    game.readMap()
    gameMap = game.getMap()
    path, totalCost = aStar(game.start, game.end, gameMap, manhattanDistance)
    print("\n", path, "\n")
    for coord in path:
        s = list(gameMap[coord[0]])
        s[coord[1]] = '@'
        gameMap[coord[0]] = "".join(s)
    f = open("outMan.txt", "w")
    for line in gameMap:
        f.write(line)
    f.write(f"\nTotal cost = {totalCost}")
    f.close()
    BBGyms()
    # print("CUSTO FINAL É:", caboo.getCost())

