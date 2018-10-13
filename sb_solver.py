
dataInput = """
AAGGGGJJJ
AAGGGHJJJ
ABGGGHJJJ
BBBGGHHJJ
BBBGGHHHJ
CCFFEEEEE
CCCFFEEEE
CCCCCCEED
CCCCDDDDD
"""

dataInput1 = """
AAAABBCDDD
AAABBECCDD
AABBEEECCD
ABBEEEEECC
FBKKEEEEEH
FFKKKEEEHH
FFFKKKEHHH
GFFFKKHHHI
GGFFFHHHII
GGGFHHHIII
"""

dataInput2 = """
FFGGG.III.
AFGGG.III.
AFGGG.....
AFFGH.....
AFFGH....E
AFFGHH...E
AFFGHH..EE
ABBCCCDDEE
ABBCCCDDEE
ABBCCCDDEE
"""

import datetime
def logExecutionTime(func):
    def wrapped(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        koniec = datetime.datetime.now()
        print("Execution time")
        print(koniec-start)
        return result
    return wrapped

class StarBattle(object):
    def __init__(self, inputData, starNum):
        self.dicInput = {}
        x, y = 0, 0
        for i in inputData.strip():
            if i == "\n":
                self.maxX = x
                x = 0
                y += 1
            else:
                temp = self.dicInput.get(i, [])
                temp.extend([[x, y]])
                self.dicInput[i] = temp[:]
                x = x+1
        self.maxY = y + 1
        self.starNum = starNum
        self.blockList = list(self.dicInput.keys())
        self.blockElmCount = [len(self.dicInput.get(x)) for x in self.blockList]
        self.verticalCount = [0]*self.maxX
        self.horizontalCount = [0]*self.maxY
        self.resultGrid = [[0] * (self.maxX) for i in range(self.maxY)]
        #self.actCombination = [[x, 0] for x in self.blockList*self.starNum]
        #Sorted list
        self.actCombination = [[x, 0] for x in sorted(self.blockList*self.starNum)]
        self.actProgres = 0
        self.addRemoveQue = []

    def showResult(self):
        for n in self.resultGrid:
            print(n)
        return self.resultGrid

    def actualProgressPossible(self):
        temp = self.dicInput[(self.actCombination[self.actProgres][0])][self.actCombination[self.actProgres][1]]

        if self.resultGrid[temp[1]][temp[0]] != 0:
            #print("field ocupied")
            return False
        if self.verticalCount[temp[0]] == self.starNum:
            #print("field vertical count")
            return False
        if self.horizontalCount[temp[1]] == self.starNum:
            #print("horizontal vertical count")
            return False

        x = (0, -1, +1)
        y = (0, -1, +1)
        cellsAround = [(temp[0]+a, temp[1]+b) for a in x for b in y]
        for cc in cellsAround:
            if not (cc[0] == temp[0] and cc[1] == temp[1]):
                if 0 <= cc[0] < self.maxX and 0 <= cc[1] < self.maxY:
                    if self.resultGrid[cc[1]][cc[0]] == 1:
                        #print("have neigbour")
                        return False

        return True

    def putActualProgress(self):
        temp = self.dicInput[(self.actCombination[self.actProgres][0])][self.actCombination[self.actProgres][1]]
        self.resultGrid[temp[1]][temp[0]] = 1
        self.verticalCount[temp[0]] += 1
        self.horizontalCount[temp[1]] += 1
        self.addRemoveQue.append([temp[1], temp[0]])

    def removeActualProgress(self):
        self.resultGrid[self.addRemoveQue[-1][0]][self.addRemoveQue[-1][1]] = 0
        self.verticalCount[self.addRemoveQue[-1][1]] -= 1
        self.horizontalCount[self.addRemoveQue[-1][0]] -= 1
        self.addRemoveQue.pop()

    @logExecutionTime
    def solve(self):
        while True:
            if self.actualProgressPossible():
                self.putActualProgress()
                if self.actProgres == len(self.actCombination)-1:
                    print("Solution:")
                    self.showResult()
                    break
                else:
                    self.actProgres += 1
            else:
                while True:
                    if self.actCombination[self.actProgres][1] < self.blockElmCount[self.blockList.index(self.actCombination[self.actProgres][0])]-1:
                        self.actCombination[self.actProgres][1] += 1
                        break
                    else:
                        self.removeActualProgress()
                        self.actCombination[self.actProgres][1] = 0
                        self.actProgres -= 1


sb = StarBattle(dataInput, 2)
sb.solve()

sb = StarBattle(dataInput1, 2)
sb.solve()

sb = StarBattle(dataInput2, 2)
sb.solve()
