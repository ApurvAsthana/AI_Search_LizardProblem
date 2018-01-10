from collections import deque
import time
import math
import random
import itertools


class Solution:
    nursery = []
    trees = dict()

    def __init__(self, n):
        for i in range(n):
            self.nursery.append([0 for k in range(n)])

    def dfs(self, numOfLiz, n):
        timeOut = time.time()+290
        stack = Stack()
        curr_state = State(n)
        stack.push(curr_state)
        while not stack.isEmpty():
            if time.time()>timeOut:
                return "FAIL"
            curr_state = State(stack.sPop())
            if curr_state.thisLevel == n-1:
                continue
            if not self.trees.__contains__(curr_state.thisLevel+1):
                for i in range(n):
                    new_state = State(curr_state)
                    new_state.thisLevel = curr_state.thisLevel + 1
                    if self.nursery[new_state.thisLevel][i] != 2 and new_state.thisLevel < n and self.isValid(
new_state.positionsOfLizards, new_state.thisLevel,i):
                        new_state.positionsOfLizards.append([new_state.thisLevel, i])
                        if len(new_state.positionsOfLizards) == numOfLiz:
                            return new_state
                        stack.push(new_state)
            else:
                indicesList = [index for index in range(0,n)]
                trees_list = self.trees.get(curr_state.thisLevel+1)
                combin_lists = []
                temp = []
                temp.extend(indicesList[0:trees_list[0]])
                if len(temp) > 0:
                    temp.append(-1)
                    combin_lists.append(temp)
                for j in range(0, len(trees_list) - 1):
                    temp = []
                    temp.extend(indicesList[trees_list[j] + 1:trees_list[j + 1]])

                    if len(temp) > 0:
                        temp.append(-1)
                        combin_lists.append(temp)
                temp = []
                temp.extend(indicesList[trees_list[len(trees_list) - 1] + 1:len(indicesList)])
                if len(temp) > 0:
                    temp.append(-1)
                    combin_lists.append(temp)

                isValidPreCheck = [False for counter in range(0,n)]
                for ctr in range(0,n):
                    isValidPreCheck[ctr] = self.nursery[curr_state.thisLevel+1][ctr]!=2 and self.isValid(curr_state.positionsOfLizards,curr_state.thisLevel+1,ctr)
                for element in itertools.product(*combin_lists):
                    new_state = State(curr_state)
                    new_state.thisLevel = curr_state.thisLevel+1
                    for positionElement in element:
                        if positionElement!=-1 and isValidPreCheck[positionElement]:
                            new_state.positionsOfLizards.append(([new_state.thisLevel,positionElement]))
                        if len(new_state.positionsOfLizards) == numOfLiz:
                            return new_state
                    stack.push(new_state)
        return "FAIL"

    def bfs(self,numOfLiz,n):
        timeout = time.time() + 290
        queue = Q()
        curr_state = State(n)
        queue.enqueue(curr_state)
        while not queue.isEmpty():
            if time.time()>timeout:
                return "FAIL"
            curr_state = State(queue.dequeue())
            if curr_state.thisLevel == n-1:
                continue
            if not self.trees.__contains__(curr_state.thisLevel+1):
                for i in range(n):
                    new_state = State(curr_state)
                    new_state.thisLevel = curr_state.thisLevel + 1
                    if self.nursery[new_state.thisLevel][i] != 2 and new_state.thisLevel < n and self.isValid(
                            new_state.positionsOfLizards, new_state.thisLevel,
                            i):
                        new_state.positionsOfLizards.append([new_state.thisLevel, i])
                        if len(new_state.positionsOfLizards) == numOfLiz:
                            return new_state
                        queue.enqueue(new_state)

            else:
                indicesList = [index for index in range(0,n)]
                trees_list = self.trees.get(curr_state.thisLevel+1)
                combin_lists = []
                temp = []
                temp.extend(indicesList[0:trees_list[0]])
                if len(temp) > 0:
                    temp.append(-1)
                    combin_lists.append(temp)
                for j in range(0, len(trees_list) - 1):
                    temp = []
                    temp.extend(indicesList[trees_list[j] + 1:trees_list[j + 1]])

                    if len(temp) > 0:
                        temp.append(-1)
                        combin_lists.append(temp)
                temp = []
                temp.extend(indicesList[trees_list[len(trees_list) - 1] + 1:len(indicesList)])
                if len(temp) > 0:
                    temp.append(-1)
                    combin_lists.append(temp)

                isValidPreCheck = [False for ctr in range(0,n)]
                for ctr in range(0,n):
                    isValidPreCheck[ctr] = self.nursery[curr_state.thisLevel+1][ctr]!=2 and self.isValid(curr_state.positionsOfLizards,curr_state.thisLevel+1,ctr)
                for element in itertools.product(*combin_lists):
                    new_state = State(curr_state)
                    new_state.thisLevel = curr_state.thisLevel+1
                    for positionElement in element:
                        if positionElement!=-1 and isValidPreCheck[positionElement]:
                            new_state.positionsOfLizards.append(([new_state.thisLevel,positionElement]))
                        if len(new_state.positionsOfLizards) == numOfLiz:
                            return new_state
                    queue.enqueue(new_state)
        return "FAIL"


    def simulatedAnnealing(self):
        current_nursery,curr_placed_lizards = self.generateInitialRandomNursery()
        conflicts_curr_nursery = self.countConlicts(current_nursery,curr_placed_lizards)
        temperature = 35
        cooling_factor = 0.98
        stablizing_factor = 1.08
        curr_stablizer = 5
        timeout = time.time() + 290
        while True:
            if time.time()>timeout:
                return "FAIL"
            temperature = temperature * cooling_factor

            for no_of_runs in range(0,curr_stablizer):
                if conflicts_curr_nursery == 0:
                    return current_nursery
                next_nursery,next_placed_lizards = self.generateNeighbour(current_nursery,curr_placed_lizards)
                conflicts_next_nursery = self.countConlicts(next_nursery,next_placed_lizards)
                delta = conflicts_curr_nursery - conflicts_next_nursery
                try:
                    probability = math.exp(delta / temperature)
                except OverflowError:
                    probability = 0.7
                randomNo = random.random()
                if delta>=0:
                    conflicts_curr_nursery,current_nursery = conflicts_next_nursery,next_nursery
                    curr_placed_lizards = next_placed_lizards
                elif randomNo<probability:
                    conflicts_curr_nursery = conflicts_next_nursery
                    current_nursery = next_nursery
                    curr_placed_lizards = next_placed_lizards
            curr_stablizer = int(curr_stablizer * stablizing_factor)

    def generateInitialRandomNursery(self):
        new_nursery = []
        remLizardsCtr = numOfLizards
        placedLizards = []
        for i in range(0,sizeOfNursery):
            temp = [[]]
            temp[0].extend(self.nursery[i])
            new_nursery.extend(temp)
        while remLizardsCtr>0:
            random_row = random.randint(0,sizeOfNursery-1)
            random_col = random.randint(0,sizeOfNursery-1)
            if new_nursery[random_row][random_col]==2 or new_nursery[random_row][random_col]==1:
                continue
            else:
                new_nursery[random_row][random_col] = 1
                placedLizards.append([random_row,random_col])
                remLizardsCtr = remLizardsCtr - 1
        return new_nursery,placedLizards

    def generateNeighbour(self,input_nursery,placed_lizards):
        new_nursery = []
        for i in range(0,sizeOfNursery):
            temp = [[]]
            temp[0].extend(input_nursery[i])
            new_nursery.extend(temp)
        new_placed_liz = []
        for i in range(0,len(placed_lizards)):
            temp = [[]]
            temp[0].extend(placed_lizards[i])
            new_placed_liz.extend(temp)
        random_liz_index = random.randint(0,len(new_placed_liz)-1)
        new_nursery[new_placed_liz[random_liz_index][0]][new_placed_liz[random_liz_index][1]]=0
        while True:
            random_row = random.randint(0, sizeOfNursery - 1)
            random_col = random.randint(0, sizeOfNursery - 1)
            if new_nursery[random_row][random_col]==2 or new_nursery[random_row][random_col]==1:
                continue
            else:
                new_placed_liz[random_liz_index][0] = random_row
                new_placed_liz[random_liz_index][1] = random_col
                new_nursery[new_placed_liz[random_liz_index][0]][new_placed_liz[random_liz_index][1]] = 1
                break
        return new_nursery,new_placed_liz


    def countConlicts(self,new_nursery,placedLiz):
        countConflicts = 0
        for lizard in placedLiz:
                row = lizard[0]
                column = lizard[1]
                j = row - 1
                while j>=0:
                    if new_nursery[j][column]==1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[j][column]==2:
                        break
                    j = j - 1
                j = row + 1
                while j<sizeOfNursery:
                    if new_nursery[j][column]==1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[j][column]==2:
                        break
                    j = j + 1
                i = row + 1
                j = column + 1
                while i<sizeOfNursery and j<sizeOfNursery:
                    if new_nursery[i][j]==1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[i][j]==2:
                        break
                    i = i + 1
                    j = j + 1
                i = row - 1
                j = column + 1
                while i >= 0 and j < sizeOfNursery:
                    if new_nursery[i][j] == 1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[i][j] == 2:
                        break
                    i = i - 1
                    j = j + 1

                i = row + 1
                j = column - 1
                while i < sizeOfNursery and j >= 0:
                    if new_nursery[i][j] == 1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[i][j] == 2:
                        break
                    i = i + 1
                    j = j - 1

                i = row - 1
                j = column - 1
                while i >= 0 and j >= 0:
                    if new_nursery[i][j] == 1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[i][j] == 2:
                        break
                    i = i - 1
                    j = j - 1

                i = column - 1
                while i >= 0:
                    if new_nursery[row][i] == 1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[row][i] == 2:
                        break
                    i = i - 1

                i = column + 1
                while i < sizeOfNursery:
                    if new_nursery[row][i] == 1:
                        countConflicts = countConflicts + 1
                        break
                    elif new_nursery[row][i] == 2:
                        break
                    i = i + 1

        return countConflicts

    def isValid(self, lizPositions, lvl, index):    #optimize this, use trees dict and#
        if lvl == 0:
            return True
        for lizard in lizPositions:
            if lizard[1]==index:
                isSafe = False
                for i in range(lizard[0]+1,lvl):
                    if self.trees.__contains__(i):
                        if self.trees.get(i).__contains__(index):
                            isSafe = True
                            break

                if not isSafe:
                    return False
            elif (lizard[0]-lizard[1]) == (lvl-index):
                isSafe = False
                for i in range(lizard[0]+1,lvl):
                    if self.trees.__contains__(i):
                        tree_list = self.trees.get(i)
                        for tree in tree_list:
                            if (i-tree) == (lvl-index):
                                isSafe = True
                                break

                if not isSafe:
                    return False
            elif (lizard[0] + lizard[1]) == (lvl + index):
                isSafe = False
                for i in range(lizard[0] + 1, lvl):
                    if self.trees.__contains__(i):
                        tree_list = self.trees.get(i)
                        for tree in tree_list:
                            if (i + tree) == (lvl + index):
                                isSafe = True
                                break
                if not isSafe:
                    return False
        return True

class State:
    positionsOfLizards = []
    thisLevel = -1

    def __init__(self, n):
        if(isinstance(n,int)):
            self.positionsOfLizards = []
            self.thisLevel = -1
        elif(isinstance(n,State)):
            self.positionsOfLizards = []
            self.positionsOfLizards.extend(n.positionsOfLizards)
            self.thisLevel = n.thisLevel


class Stack:
    data = deque()

    def __init__(self):
        self.data = deque()

    def push(self, item):
        self.data.append(item)

    def sPop(self):
        return self.data.pop()

    def isEmpty(self):
        if (len(self.data) > 0):
            return False
        else:
            return True

    def sPeek(self):
        if self.isEmpty():
            return -1
        else:
            return State(self.data[len(self.data)-1]).thisLevel

class Q:
    dataInQ = deque()

    def __init__(self):
        self.dataInQ = deque()

    def enqueue(self,item):
        self.dataInQ.append(item)

    def dequeue(self):
        return self.dataInQ.popleft()

    def isEmpty(self):
        if len(self.dataInQ)>0:
            return False
        else:
            return True

    def sPeek(self):
        if self.isEmpty():
            return -1
        else:
            return State(self.dataInQ[len(self.dataInQ)-1]).thisLevel

    def dequeueAtFront(self):
        return self.dataInQ.pop()


count_trees = 0
f_in = open('input.txt', 'r')
startTime = time.time()
method = f_in.readline()
sizeOfNursery = int(f_in.readline())
numOfLizards = int(f_in.readline())
S = Solution(sizeOfNursery)
for ctr in range(sizeOfNursery):
    line_str = f_in.readline()
    for str_index in range(len(line_str)):
        if line_str[str_index] == "2":
            S.nursery[ctr][str_index] = 2
            count_trees = count_trees + 1
            if S.trees.__contains__(ctr):
                S.trees.get(ctr).append(str_index)
            else:
                temp = []
                temp.append(str_index)
                S.trees[ctr] = temp
f_out = open('output.txt', 'w')
if numOfLizards > (sizeOfNursery+count_trees):
    f_out.write("FAIL")
    # print("FAIL1")
elif method.__contains__("DFS"):
    answer = S.dfs(numOfLizards, sizeOfNursery)
    if answer=="FAIL":
        # print("FAIL")
        f_out.write("FAIL")
    else:
        f_out.write("OK\n")
        # print("OK")
        resultState = State(answer)
        for index in range(len(resultState.positionsOfLizards)):
            S.nursery[resultState.positionsOfLizards[index][0]][resultState.positionsOfLizards[index][1]] = 1
        resultStr = ""
        for i in range(sizeOfNursery):
            for j in range(sizeOfNursery):
                resultStr = resultStr + str(S.nursery[i][j])
            resultStr = resultStr + '\n'
        # print(resultStr)
        f_out.write(resultStr)
elif method.__contains__("BFS"):
    answer = S.bfs(numOfLizards, sizeOfNursery)
    if answer=="FAIL":
        # print("FAIL")
        f_out.write("FAIL")
    else:
        f_out.write("OK\n")
        # print("OK")
        resultState = State(answer)
        for index in range(len(resultState.positionsOfLizards)):
            S.nursery[resultState.positionsOfLizards[index][0]][resultState.positionsOfLizards[index][1]] = 1
        resultStr = ""
        for i in range(sizeOfNursery):
            for j in range(sizeOfNursery):
                resultStr = resultStr + str(S.nursery[i][j])
            resultStr = resultStr + '\n'
        # print(resultStr)
        f_out.write(resultStr)
elif method.__contains__("SA"):
    answer = S.simulatedAnnealing()
    if answer=="FAIL":
        # print("FAIL")
        f_out.write("FAIL")
    else:
        f_out.write("OK\n")
        # print("OK")
        resultStr = ""
        for i in range(sizeOfNursery):
            for j in range(sizeOfNursery):
                resultStr = resultStr + str(answer[i][j])
            resultStr = resultStr + '\n'
        # print(resultStr)
        f_out.write(resultStr)
print(time.time() - startTime)
f_in.close()
f_out.close()