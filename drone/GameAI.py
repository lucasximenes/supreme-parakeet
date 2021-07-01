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



    botState = [0,0,0,0,0,0]

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

    def UpdateBotState(self,command):

        oldState = self.botState
        if(command == 'right'):
            self.botState[0] = oldState[2]
            self.botState[1] = oldState[3]
            self.botState[2] = oldState[1]
            self.botState[3] = oldState[0]
        if(command == 'left'):
            self.botState[0] = oldState[3]
            self.botState[1] = oldState[2]
            self.botState[2] = oldState[0]
            self.botState[3] = oldState[1]
        if(command == 're'):
            self.botState[0] = oldState[0]
            self.botState[1] = 0
            self.botState[2] = 0
            self.botState[3] = 0
        if(command == 'front'):
            self.botState = [0,0,0,0,0,0]
        print(self.botState)

    def StateAction(self):

        action = 2
        if(self.botState[5] == 1): # Enemy in line
            action = 3
        elif(self.botState[4] == 1): # Item
            self.botState[4] = 0
            action = 4
        elif(self.botState[4] == 2): # Item
            self.botState[4] = 0
            action = 6
        elif(self.botState[0] == 1): # Blocked
            if(self.botState[2] == 0): # Right free
                action = 0
            elif(self.botState[3] == 0): # Left free
                action = 1
            elif(self.botState[1] == 0): # Back free
                action = 7


        self.botState[5] = 0 # reset enemy in line
        print("Mandando a action ", action)

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

            if s == 'blocked':
                self.botState[0] = 1

            if s == 'shooting':
                self.botState[0] = 1
                # pass
            
            elif s == "steps":
                self.botState[5] = 1
                # pass
            
            elif s == "breeze":
                # pass
                self.botState[0] = 1


            elif s == "flash":
                self.botState[0] = 1
                # pass

            elif s == "blueLight":
                self.botState[4] = 1
                # pass

            elif s == "redLight":
                self.botState[4] = 2
                # pass

            elif s == "greenLight":
                self.botState[4] = 3
                # pass

            elif s == "weakLight":
                self.botState[4] = 4
                # pass
            elif "enemy#" in s:
                self.botState[5] = 1



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
            self.UpdateBotState('right')
            return "virar_direita"
        elif n == 1:
            self.UpdateBotState('left')
            return "virar_esquerda"
        elif n == 2:
            self.UpdateBotState('front')
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
            self.UpdateBotState('re')
            return "andar_re"

        return ""

