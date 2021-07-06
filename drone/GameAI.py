#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position
import astar as AS
import numpy as np
from threading import Timer

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0




    triedToPickUpTreasure = False

    botCompass = {'front':0,'back':0,'right':0,'left':0,'upright':0,'upleft':0,'lowright':0,'lowleft':0}

    # botEnvironment Item1, Item2, Item3, Enemy
    botEnvironment = [0,0,0,0,0]

    botMap = np.array(34*[59*['?']])

    countRotate = 0

    countShots = 0

    isTryingToFindTreasure = False

    # lista de tesouros 
    treasureList = []
    cdTreasureList = []
    timerTL = []

    # lista de vidas
    lifeList = []
    cdLifeList = []
    timerLL = []

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    def hasExplored(self,cX,cY):
        if(cX > 58 or cX < 0):
            return True
        if(cY > 33 or cY < 0):
            return True
        # print(coordX, coordY)
        if(self.botMap[cY,cX] != '?'):
            return True
        else:
            return False

    def isDanger(self, cY, cX):
        return self.botMap[cY,cX] == 'X'


    def setDanger(self, cY, cX):

        newDangers = []

        if(self.dir =="north"):
            newDangers.append((self.player.y,self.player.x+1))
            newDangers.append((self.player.y,self.player.x-1))
            newDangers.append((self.player.y-1,self.player.x))
        if(self.dir =="south"):
            newDangers.append((self.player.y,self.player.x-1))
            newDangers.append((self.player.y,self.player.x+1))
            newDangers.append((self.player.y+1,self.player.x))
        if(self.dir =="east"):
            newDangers.append((self.player.y+1,self.player.x))
            newDangers.append((self.player.y-1,self.player.x))
            newDangers.append((self.player.y,self.player.x+1))
        if(self.dir =="west"):
            newDangers.append((self.player.y-1,self.player.x))
            newDangers.append((self.player.y+1,self.player.x))
            newDangers.append((self.player.y,self.player.x-1))

        hasDanger = []

        for i in newDangers:
            if(self.isDanger(i[0],i[1])):
                hasDanger.append(i)

        if(len(hasDanger)==0):
            for j in newDangers:
                self.updateMap(j[0],j[1],"X")
            return newDangers
        else:
            return hasDanger

        
        

    def updateMap(self,cY,cX,tile):
        # ? - Unknown 
        # . - Empty
        # T - Treasure
        # H - PowerUp
        # X - Danger
        # W - Wall
        if (cX > 58 or cX < 0 or cY > 33 or cY < 0):
            return
        elif(self.botMap[cY,cX] == '.' or self.botMap[cY,cX] == '?'):
            if(self.botMap[cY,cX] == '.' and not (tile == "T" or tile == 'H')):
                return

            self.botMap[cY,cX] = tile

    def printMap(self):
        print(self.player.x,self.player.y)
        for i in self.botMap:
            for j in i:
                print(j,end=" ")
            print()
        print("\n\n")

    # def printCompass(self,oldStatex):
    #     botSymbol = {"north": '^',"south": 'v',"east": '>',"west": '<'}

    #     print("Antes:")
    #     print(oldState[7],oldState[0],oldState[4])
    #     print(oldState[3],"*",oldState[2])
    #     print(oldState[6],oldState[1],oldState[5])
    #     print("\n\nDepois:")
    #     print(self.botCompass[7],self.botCompass[0],self.botCompass[4])
    #     print(self.botCompass[3],botSymbol[self.dir],self.botCompass[2])
    #     print(self.botCompass[6],self.botCompass[1],self.botCompass[5])

    def GetAdjacentCoordinate(self,side):
        if(side == 'right'):
            if(self.dir == 'north'):
                return self.player.x + 1, self.player.y
            if(self.dir == 'south'):
                return self.player.x - 1, self.player.y
            if(self.dir == 'east'):
                return self.player.x , self.player.y + 1
            if(self.dir == 'west'):
                return self.player.x , self.player.y - 1
        if(side == 'left'):
            if(self.dir == 'north'):
                return self.player.x - 1, self.player.y
            if(self.dir == 'south'):
                return self.player.x + 1, self.player.y
            if(self.dir == 'east'):
                return self.player.x , self.player.y - 1
            if(self.dir == 'west'):
                return self.player.x , self.player.y + 1

    def getRelDirection(self,cY, cX, oY, oX):
        print(self.dir,cY, cX, oY, oX)
        if (self.dir == "north"):
            if (oX == cX):
                if (oY > cY):
                    return "back"
                elif (oY < cY):
                    return "front"
            elif (oY == cY):
                if (oX < cX):
                    return "left"
                elif (oX > cX):
                    return "right"
        elif (self.dir == "south"):
            if (oX == cX):
                if (oY > cY):
                    return "front"
                elif (oY < cY):
                    return "back"
            elif (oY == cY):
                if (oX < cX):
                    return "right"
                elif (oX > cX):
                    return "left"
        elif (self.dir == "west"):
            if (oX == cX):
                if (oY > cY):
                    return "left"
                elif (oY < cY):
                    return "right"
            elif (oY == cY):
                if (oX < cX):
                    return "front"
                elif (oX > cX):
                    return "back"
        elif (self.dir == "east"):
            if (oX == cX):
                if (oY > cY):
                    return "right"
                elif (oY < cY):
                    return "left"
            elif (oY == cY):
                if (oX < cX):
                    return "back"
                elif (oX > cX):
                    return "front"
        else:
            return ""


    def UpdateBotCompass(self,command):
        # print("Energy: ", self.energy)
        # print("Score: ", self.score)
        print(self.treasureList)
        if(self.energy > 0):
            self.printMap()
        # print(self.dir)

    # botCompass N(0), S(1), E(2), W(3), NE(4), SE(5), SW(6), NW(7)

        oldCompass = self.botCompass
        if(command == 'right'):
            self.botCompass['front'] = oldCompass['right']
            self.botCompass['right'] = oldCompass['back']
            self.botCompass['left'] = oldCompass['front']
            self.botCompass['back'] = oldCompass['left']
            self.botCompass['upright'] = oldCompass['lowleft']
            self.botCompass['upleft'] = oldCompass['upright']
            self.botCompass['lowright'] = oldCompass['lowleft']
            self.botCompass['lowleft'] = oldCompass['upleft']


        if(command == 'left'):
            self.botCompass['front'] = oldCompass['left']
            self.botCompass['right'] = oldCompass['front']
            self.botCompass['left'] = oldCompass['back']
            self.botCompass['back'] = oldCompass['right']
            self.botCompass['upright'] = oldCompass['upleft']
            self.botCompass['upleft'] = oldCompass['lowleft']
            self.botCompass['lowright'] = oldCompass['upright']
            self.botCompass['lowleft'] = oldCompass['lowright']

        if(command == 're'):
            self.botCompass['front'] = 1
            self.botCompass['right'] = oldCompass['lowright']
            self.botCompass['left'] = oldCompass['lowleft']
            self.botCompass['back'] = 0
            self.botCompass['upright'] = oldCompass['right']
            self.botCompass['upleft'] = oldCompass['left']
            self.botCompass['lowright'] = 0
            self.botCompass['lowleft'] = 0

        if(command == 'front'):
            self.botCompass['front'] = 0
            self.botCompass['right'] = oldCompass['upright']
            self.botCompass['left'] = oldCompass['upleft']
            self.botCompass['back'] = 0
            self.botCompass['upright'] = 0
            self.botCompass['upleft'] = 0
            self.botCompass['lowright'] = oldCompass['right']
            self.botCompass['lowleft'] = oldCompass['left']




    def StateAction(self):

        self.updateMap(self.player.y,self.player.x,'.')



        action = 2

        # ===========================================================
        #  Attack State

        if(self.botEnvironment[3] == 1 and self.countShots<30): # Enemy in line
            action = 3
            self.countShots +=1
            self.botEnvironment[3] = 0



        # ===========================================================
        #  Escape State
        elif(self.botEnvironment[4] == 1 and self.botEnvironment[3] != 1 ): 
            action = 0
            self.botEnvironment[4] = 0
            self.countShots = 0


        # ===========================================================
        #  Scavenger State

        elif(self.botEnvironment[0] == 1 or self.botEnvironment[2] == 1): # Treasure
            self.updateMap(self.player.y,self.player.x,'T')
            self.isTryingToFindTreasure = False
            if(self.triedToPickUpTreasure):
                action = 4
            else:
                action = 5
                self.triedToPickUpTreasure = True
                if((self.player.x,self.player.y) not in self.treasureList):
                    self.treasureList.append((self.player.x,self.player.y))
                self.treasureList.remove((self.player.x,self.player.y))
                self.cdTreasureList.append((self.player.x,self.player.y))
                self.timerTL.append(Timer(15.0,self.finishedTimerTL))
                self.timerTL[len(self.timerTL) - 1].start()
            self.countShots = 0


        elif(self.botEnvironment[1] == 1 and self.energy < 100): # Power
            self.updateMap(self.player.y,self.player.x,'H')
            self.botEnvironment[1] = 0
            action = 6

            #print("oi",self.lifeList, (self.player.x,self.player.y) )
            if((self.player.x,self.player.y) not in self.lifeList):
                self.lifeList.append((self.player.x,self.player.y))

            self.lifeList.remove((self.player.x,self.player.y))
            self.cdLifeList.append((self.player.x,self.player.y))
            self.timerLL.append(Timer(15.0,self.finishedTimerLL))
            self.timerLL[len(self.timerLL) - 1].start()
            self.countShots = 0


        # ===========================================================
        #  Explorer State
        else:
            if(self.botCompass['front'] == 1): # Front Blocked
                rotDir = np.random.randint(0,2)
                if(rotDir == 0):
                    if(self.botCompass['right'] == 0 and self.countRotate < 10): # Right free
                        action = 0
                        self.countRotate += 1
                    elif(self.botCompass['left'] == 0 and self.countRotate < 10): # Left free
                        action = 1
                        self.countRotate += 1
                    elif(self.botCompass['back'] == 0): # Back free
                        action = 7
                        self.countRotate = 0
                else:
                    if(self.botCompass['left'] == 0 and self.countRotate < 10): # Right free
                        action = 1
                        self.countRotate += 1
                    elif(self.botCompass['right'] == 0 and self.countRotate < 10): # Left free
                        action = 0
                        self.countRotate += 1
                    elif(self.botCompass['back'] == 0): # Back free
                        action = 7
                        self.countRotate = 0 
                self.countShots = 0
                return action
            else:
                nextCx, nextCy = self.NextPosition().x,self.NextPosition().y 
                if(self.hasExplored(nextCx,nextCy) and self.isTryingToFindTreasure == False):
                    print("Já explorei")
                    rightX, rightY = self.GetAdjacentCoordinate("right")
                    leftX, leftY = self.GetAdjacentCoordinate("left")
                    if(not self.hasExplored(rightX, rightY) and self.countRotate < 10):
                        action = 0
                        self.countRotate += 1
                    elif(not self.hasExplored(leftX, leftY) and self.countRotate < 10 ):
                        action = 1
                        self.countRotate += 1
                elif(self.isTryingToFindTreasure == False):
                    if(self.dir == 'east'):
                        r = self.player.y + 1
                        while r < 34:
                            if(self.botMap[r,self.player.x] == 'W' or self.botMap[r,self.player.x] == 'X'):
                                break
                            if(self.botMap[r,self.player.x] == 'T' and (self.player.x, r) in self.treasureList):
                                action = 0 
                                self.isTryingToFindTreasure = True
                                return action
                            r +=1
                        l = self.player.y -1
                        while l >= 0:
                            if(self.botMap[l,self.player.x] == 'W' or self.botMap[l,self.player.x] == 'X'):
                                    break
                            if(self.botMap[l,self.player.x] == 'T' and (self.player.x, l) in self.treasureList):
                                action =  1
                                self.isTryingToFindTreasure = True
                                return action
                            l -=1
                    elif(self.dir == 'west'):
                        r = self.player.y -1
                        while r >= 0:
                            if(self.botMap[r,self.player.x] == 'W' or self.botMap[r,self.player.x] == 'X'):
                                break
                            if(self.botMap[r,self.player.x] == 'T' and (self.player.x, r) in self.treasureList):
                                action = 0 
                                self.isTryingToFindTreasure = True
                                return action
                            r -=1
                        l = self.player.y +1
                        while l < 34:
                            if(self.botMap[l,self.player.x] == 'W' or self.botMap[l,self.player.x] == 'X'):
                                    break
                            if(self.botMap[l,self.player.x] == 'T' and (self.player.x, l) in self.treasureList):
                                action =  1
                                self.isTryingToFindTreasure = True
                                return action
                            l +=1
                    elif(self.dir == 'north'):
                        r = self.player.x +1
                        while r < 59:
                            if(self.botMap[self.player.y,r] == 'W' or self.botMap[self.player.y,r] == 'X'):
                                break
                            if(self.botMap[self.player.y,r] == 'T' and (r, self.player.y) in self.treasureList):
                                action = 0 
                                self.isTryingToFindTreasure = True
                                return action
                            r +=1
                        l = self.player.x -1
                        while l >= 0:
                            if(self.botMap[self.player.y,l] == 'W' or self.botMap[self.player.y,l] == 'X'):
                                    break
                            if(self.botMap[self.player.y,l] == 'T' and (l, self.player.y) in self.treasureList):
                                action =  1
                                self.isTryingToFindTreasure = True
                                return action
                            l -=1
                    elif(self.dir == 'south'):
                        r = self.player.x -1
                        while r >= 0:
                            if(self.botMap[self.player.y,r] == 'W' or self.botMap[self.player.y,r] == 'X'):
                                break
                            if(self.botMap[self.player.y,r] == 'T' and (r, self.player.y) in self.treasureList):
                                action = 0 
                                self.isTryingToFindTreasure = True
                                return action
                            r -=1
                        l = self.player.x +1
                        while l < 59:
                            if(self.botMap[self.player.y,l] == 'W' or self.botMap[self.player.y,l] == 'X'):
                                    break
                            if(self.botMap[self.player.y,l] == 'T' and (l, self.player.y) in self.treasureList):
                                action =  1
                                self.isTryingToFindTreasure = True
                                return action
                            l +=1
                else:
                    action = 2
                    self.countRotate = 0
                    self.countShots = 0


        # print("Mandando a action ", action)


        # print(self.player.x)

        return action

    def finishedTimerTL(self):
        self.timerTL[0].cancel()
        self.timerTL = self.timerTL[1:]
        self.treasureList.append(self.cdTreasureList[0])
        self.cdTreasureList = self.cdTreasureList[1:]

    def finishedTimerLL(self):
        self.timerLL[0].cancel()
        self.timerLL = self.timerLL[1:]
        self.lifeList.append(self.cdLifeList[0])
        self.cdLifeList = self.cdLifeList[1:]


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x + 1, self.player.y - 1))

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))

        ret.append(Position(self.player.x - 1, self.player.y + 1))
        ret.append(Position(self.player.x, self.player.y + 1))
        ret.append(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y


    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):  
       
        for s in o:
            # print(s)
            if s == 'blocked':
                # self.botCompass[0] = 1
                self.botCompass['front'] = 1

                coordX, coordY = self.NextPosition().x, self.NextPosition().y

                self.updateMap(coordY,coordX,'W')


            if s == 'shooting':

                self.botCompass['front'] = 1
                # pass
            
            elif s == "steps":
                # self.botCompass[0] = 1
                self.botCompass['front'] = 1
                # pass


            elif s == "flash" or s == "breeze":
                print("Amigo estou aqui")
                next_pos = self.NextPosition()
                coordX, coordY = next_pos.x, next_pos.y

                dangers = self.setDanger(coordY,coordX)
                print(dangers)

                for el in dangers:
                    rel_dir = self.getRelDirection(self.player.y, self.player.x, el[0],el[1])
                    print(rel_dir)
                    if rel_dir != "":

                        self.botCompass[rel_dir] = 1
                        print(self.botCompass)

                                

                # self.botCompass['front'] = 1
                # self.botCompass['left'] = 1
                # self.botCompass['right'] = 1
                # self.botCompass['upright'] = 1
                # self.botCompass['upleft'] = 1
 
                # coordX, coordY = self.NextPosition().x, self.NextPosition().y

                # self.updateMap(coordY,coordX,'X')
                # if(self.dir =="north"):
                #     self.updateMap(coordY-1,coordX+1,'X')
                #     self.updateMap(coordY-1,coordX-1,'X')
                # if(self.dir =="south"):
                #     self.updateMap(coordY+1,coordX+1,'X')
                #     self.updateMap(coordY+1,coordX-1,'X')
                # if(self.dir =="east"):
                #     self.updateMap(coordY+1,coordX-1,'X')
                #     self.updateMap(coordY-1,coordX-1,'X')
                # if(self.dir =="west"):
                #     self.updateMap(coordY+1,coordX+1,'X')
                #     self.updateMap(coordY-1,coordX+1,'X')
                

            elif s == "blueLight":
                self.updateMap(self.player.y,self.player.x,'T')

                self.botEnvironment[0] = 1

                if((self.player.x,self.player.y) not in self.treasureList):
                    self.treasureList.append((self.player.x, self.player.y))


            elif s == "redLight":
                self.updateMap(self.player.y,self.player.x,'H')

                self.botEnvironment[1] = 1

                if((self.player.x,self.player.y) not in self.lifeList):
                    self.lifeList.append((self.player.x,self.player.y))

                


            elif s == "greenLight":
                pass

            elif s == "weakLight":
                self.botEnvironment[2] = 1
                self.updateMap(self.player.y,self.player.x,'T')
                if((self.player.x,self.player.y) not in self.treasureList):
                    self.treasureList.append((self.player.x, self.player.y))
                

            elif "enemy#" in s:
                self.botEnvironment[3] = 1

            elif s == "hit":
                self.botEnvironment[4] = 1




    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pass
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):
        # self.updateMap(self.player.x,self.player.y,'0')
        # self.printMap()


        # n = random.randint(0,7)

        n = self.StateAction()

        if(n!=5):
            self.triedToPickUpTreasure = False
            self.botEnvironment[0] = 0

        if n == 0:
            self.UpdateBotCompass('right')
            return "virar_direita"
        elif n == 1:
            self.UpdateBotCompass('left')
            return "virar_esquerda"
        elif n == 2:
            self.UpdateBotCompass('front')
            
            return "andar"
        elif n == 3:
            # print("Shooting")
            return "atacar"
        elif n == 4:
            return "pegar_ouro"
        elif n == 5:
            return "pegar_anel"
        elif n == 6:
            return "pegar_powerup"
        elif n == 7:
            self.UpdateBotCompass('re')
            return "andar_re"

        return ""

