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
    # botCompass N(0), S(1), E(2), W(3), NE(4), SE(5), SW(6), NW(7)
    botCompass = [0,0,0,0,0,0,0,0]

    # botEnvironment Item1, Item2, Item3, Enemy
    botEnvironment = [0,0,0,0]

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

    def UpdateBotCompass(self,command):
        print(self.botCompass[7],self.botCompass[0],self.botCompass[4])
        print(self.botCompass[3],"*",self.botCompass[2])
        print(self.botCompass[6],self.botCompass[1],self.botCompass[5])

        oldState = self.botCompass
        if(command == 'right'):
            self.botCompass[0] = oldState[2] # East becomes north
            self.botCompass[1] = oldState[3] # West becomes south
            self.botCompass[2] = oldState[1] # South becomes East
            self.botCompass[3] = oldState[0] # North becomes west
            self.botCompass[4] = oldState[5] # NE becomes SE 
            self.botCompass[5] = oldState[6] # SE becomes SW
            self.botCompass[6] = oldState[7] # SW becomes NW
            self.botCompass[7] = oldState[4] # NW becomes NE

        if(command == 'left'):
            self.botCompass[0] = oldState[3] # East becomes north
            self.botCompass[1] = oldState[2] # West becomes south
            self.botCompass[2] = oldState[0] # South becomes East
            self.botCompass[3] = oldState[1] # North becomes west
            self.botCompass[4] = oldState[7] # NE becomes NW 
            self.botCompass[5] = oldState[4] # SE becomes NE
            self.botCompass[6] = oldState[5] # SW becomes SE
            self.botCompass[7] = oldState[6] # NW becomes SW
        if(command == 're'):
            self.botCompass[0] = oldState[0]
            self.botCompass[1:4] = [0,0,0,0]

            self.botCompass[4] = oldState[2]
            self.botCompass[7] = oldState[3]
            if(self.nearDanger):
                self.botCompass[4] = -1
                self.botCompass[7] = -1
        if(command == 'front'):
            self.botCompass[0] = 0
            self.botCompass[1] = 0 # 
            self.botCompass[2] = oldState[4] # NE becomes E
            self.botCompass[3] = oldState[7] # NW becomes W
            self.botCompass[4] = 0 #
            self.botCompass[5] = oldState[2] # E becomes SE
            self.botCompass[6] = oldState[3] # W becomes SW
            self.botCompass[7] = 0 # 

        

    def StateAction(self):

        action = 2
        if(self.botEnvironment[3] == 1): # Enemy in line
            action = 3
            self.botEnvironment[3] = 0
        elif(self.botEnvironment[0] == 1 or self.botEnvironment[2] == 1): # Treasure
            if(self.triedToPickUpTreasure):
                print("Vou tentar pegar alguma coisa com 4")
                action = 4
            else:
                action = 5
                print("Vou tentar pegar alguma coisa com 5")
                self.triedToPickUpTreasure = True

        elif(self.botCompass[1] == 1 and self.energy < 100): # Power
            self.botEnvironment[1] = 0
            action = 6
        elif(self.botCompass[0] == 1): # Blocked
            if(self.botCompass[2] == 0): # Right free
                action = 0
            elif(self.botCompass[3] == 0): # Left free
                action = 1
            elif(self.botCompass[1] == 0): # Back free
                action = 7


        print("Mandando a action ", action)

        if(action!=5):
            self.triedToPickUpTreasure = False
            self.botEnvironment[0] = 0

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
                self.botCompass[0] = 1

            if s == 'shooting':
                self.botCompass[0] = 1
                # pass
            
            elif s == "steps":
                self.botCompass[0] = 1
                # pass
            
            elif s == "breeze":
                # pass
                if(-1 in self.botCompass[1:]):
                    self.botCompass[0] = 0
                    self.nearDanger = False
                else:
                    self.botCompass[0] = 1
                    self.botCompass[2] = 1
                    self.botCompass[3] = 1
                    self.nearDanger = True


            elif s == "flash":
                if(-1 in self.botCompass[1:]):
                    self.botCompass[0] = 0
                    self.nearDanger = False
                else:
                    self.botCompass[0] = 1
                    self.botCompass[2] = 1
                    self.botCompass[3] = 1
                    self.nearDanger = True
                # pass

            elif s == "blueLight":
                self.botEnvironment[0] = 1
                # pass

            elif s == "redLight":
                self.botEnvironment[1] = 1
                # pass

            elif s == "greenLight":
                pass

            elif s == "weakLight":
                self.botEnvironment[2] = 1
                # pass
            elif "enemy#" in s:
                self.botEnvironment[3] = 1



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
            print("Shooting")
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

