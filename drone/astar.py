class Pathfinder:
    def __init__(self):
        self.gameMap = []
        self.start = (0, 0)
        self.end = (0, 0)

    def readMap(self, map):
        j = 0
        for line in map:
            self.gameMap.append(line)
            for i in range(41):
                if line[i] == 'I':
                    self.start = (j, i)
                elif line[i] == 'F':
                    self.end = (j, i)
            j += 1

    