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
# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0



    nearDanger = False
    triedToPickUpTreasure = False

    botCompass = {'front':0,'back':0,'right':0,'left':0,'upright':0,'upleft':0,'lowright':0,'lowleft':0}

    # botEnvironment Item1, Item2, Item3, Enemy
    botEnvironment = [0,0,0,0,0]

    botMap = np.array(34*[59*['?']])

    countRotate = 0

    # lista de tesouros 
    treasureList = []
    cdTreasureList = []

    # lista de vidas
    lifeList = []

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



    def updateMap(self,cX,cY,tile):
        # ? - Unknown 
        # . - Empty
        # T - Treasure
        # H - PowerUp
        # X - Danger
        # W - Wall
        if(cX > 58 or cX < 0 or cY > 33 or cY < 0):
            return
        elif(self.botMap[cY,cX] == '.' or self.botMap[cY,cX] == '?' or self.botMap[cY,cX] == '0' ):
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



    def UpdateBotCompass(self,command):
        self.printMap()

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

        self.updateMap(self.player.x,self.player.y,'.')
        action = 0

        # ===========================================================
        #  Attack State

        if(self.botEnvironment[3] == 1): # Enemy in line
            action = 3
            self.botEnvironment[3] = 0



        # ===========================================================
        #  Escape State
        elif(self.botEnvironment[4] == 1): 
            action = 0
            self.botEnvironment[4] = 0


        # ===========================================================
        #  Scavenger State

        elif(self.botEnvironment[0] == 1 or self.botEnvironment[2] == 1): # Treasure
            if(self.triedToPickUpTreasure):
                action = 4
                self.cdTreasureList.append((self.player.y,self.player.x))
            else:
                action = 5
                self.triedToPickUpTreasure = True
                self.cdTreasureList.append((self.player.y,self.player.x))


        elif(self.botEnvironment[1] == 1 and self.energy < 100): # Power
            self.botEnvironment[1] = 0
            action = 6


        # ===========================================================
        #  Explorer State
        else:
            if(self.botCompass['front'] == 1): # Front Blocked
                if(self.botCompass['right'] == 0 and self.countRotate < 10): # Right free
                    action = 0
                    self.countRotate += 1
                elif(self.botCompass['left'] == 0 and self.countRotate < 10): # Left free
                    action = 1
                    self.countRotate += 1
                elif(self.botCompass['back'] == 0): # Back free
                    action = 7
                    self.countRotate = 0
                return action
            else:
                nextCx, nextCy = self.NextPosition().x,self.NextPosition().y 
                if(self.hasExplored(nextCx,nextCy)):
                    print("Já explorei")
                    rightX, rightY = self.GetAdjacentCoordinate("right")
                    leftX, leftY = self.GetAdjacentCoordinate("left")
                    if(not self.hasExplored(rightX, rightY) and self.countRotate < 10):
                        action = 0
                        self.countRotate += 1
                    elif(not self.hasExplored(leftX, leftY) and self.countRotate < 10 ):
                        action = 1
                        self.countRotate += 1
                    else:
                        action = 2
                        self.countRotate = 0
                else:
                    action = 2
                    self.countRotate = 0


        # print("Mandando a action ", action)

        if(action!=5):
            self.triedToPickUpTreasure = False
            self.botEnvironment[0] = 0

        # print(self.player.x)

        return action


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

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

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
            print(s)
            if s == 'blocked':
                # self.botCompass[0] = 1
                self.botCompass['front'] = 1

                coordX, coordY = self.NextPosition().x, self.NextPosition().y

                self.updateMap(coordX,coordY,'W')


            if s == 'shooting':

                self.botCompass['front'] = 1
                # pass
            
            elif s == "steps":
                # self.botCompass[0] = 1
                self.botCompass['front'] = 1
                # pass
            
            elif s == "breeze":

                # if(self.nearDanger == False):
                self.botCompass['front'] = 1
                self.botCompass['left'] = 1
                self.botCompass['right'] = 1
                    # self.nearDanger = True
                # else:
                    # self.nearDanger = False
                coordX, coordY = self.NextPosition().x, self.NextPosition().y

                self.updateMap(coordX,coordY,'X')
                if(self.dir =="north"):
                    self.updateMap(coordX+1,coordY-1,'X')
                    self.updateMap(coordX-1,coordY-1,'X')
                if(self.dir =="south"):
                    self.updateMap(coordX+1,coordY+1,'X')
                    self.updateMap(coordX-1,coordY+1,'X')
                if(self.dir =="east"):
                    self.updateMap(coordX-1,coordY+1,'X')
                    self.updateMap(coordX-1,coordY-1,'X')
                if(self.dir =="west"):
                    self.updateMap(coordX+1,coordY+1,'X')
                    self.updateMap(coordX+1,coordY-1,'X')


            elif s == "flash":

                # if(self.nearDanger == False):
                self.botCompass['front'] = 1
                self.botCompass['left'] = 1
                self.botCompass['right'] = 1
                    # self.nearDanger = True
                # else:
                #     self.nearDanger = False
                coordX, coordY = self.NextPosition().x, self.NextPosition().y

                self.updateMap(coordX,coordY,'X')
                if(self.dir =="north"):
                    self.updateMap(coordX+1,coordY-1,'X')
                    self.updateMap(coordX-1,coordY-1,'X')
                if(self.dir =="south"):
                    self.updateMap(coordX+1,coordY+1,'X')
                    self.updateMap(coordX-1,coordY+1,'X')
                if(self.dir =="east"):
                    self.updateMap(coordX-1,coordY+1,'X')
                    self.updateMap(coordX-1,coordY-1,'X')
                if(self.dir =="west"):
                    self.updateMap(coordX+1,coordY+1,'X')
                    self.updateMap(coordX+1,coordY-1,'X')

            elif s == "blueLight":
                self.botEnvironment[0] = 1
                self.updateMap(self.player.y,self.player.x,'T')
                self.treasureList.append((self.player.y, self.player.x))

            elif s == "redLight":
                self.botEnvironment[1] = 1
                self.updateMap(self.player.y,self.player.x,'H')
                

            elif s == "greenLight":
                pass

            elif s == "weakLight":
                self.botEnvironment[2] = 1
                self.updateMap(self.player.y,self.player.x,'T')
                #self.treasureList.append((self.player.y, self.player.x))

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

