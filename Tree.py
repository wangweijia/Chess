import copy
import random
import math


class RootNode:
    def __init__(self):
        # # 默认值
        # self.value = 0

        # 进行uct计算的次数
        self.visits = 0

        self.childen = []

    def initCheckerboard(self, checkerboard):
        self.checkerboard = copy.deepcopy(checkerboard)
        self.initNodes()

    def initNodes(self):
        player = self.checkerboard.currentPlayer()
        player.updataAllStep()
        allLiveChessPieces = player.allLiveChessPieces()

        childen = []

        for acp in allLiveChessPieces:
            for step in acp.nextSteps:
                aNode = Node(self, acp, step)
                childen.append(aNode)

        self.childen = childen

    def uct(self):
        self.visits += 1
        uctItems = []
        maxValue = 0
        # float("inf")
        for child in self.childen:
            if child.count == 0:
                if maxValue < float("inf"):
                    uctItems = [child]
                    maxValue = float("inf")
                else:
                    uctItems.append(child)
            else:
                # c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))
                v = child.value / child.count + math.sqrt(2 * math.log(self.visits) / child.count)
                # print('v ', v)
                if v > maxValue:
                    uctItems = [child]
                    maxValue = v
                elif v == maxValue:
                    uctItems.append(child)

        index = math.floor(random.random() * len(uctItems))
        return uctItems[index]

    def simulation(self):
        tempNode = self.uct()
        tempCheckerboard = copy.deepcopy(self.checkerboard)

        pathStr = tempNode.chessPieces.pathStr()
        chessPieces = tempCheckerboard.checkerboardPath[pathStr]
        tempCheckerboard.currentPlayerPlay(chessPieces, tempNode.step)

        res = tempCheckerboard.getNextPlayerPlay()
        # print(res, self.checkerboard.currentPlayer().direction)

        if res == 0:
            tempNode.accumulation(5)
        elif res == self.checkerboard.currentPlayer().direction:
            tempNode.accumulation(10)
        else:
            tempNode.accumulation(0)


class Node:
    def __init__(self, parentNode, chessPieces, step):
        # 父类节点
        self.parentNode = parentNode

        # 当前棋子
        self.chessPieces = chessPieces
        # 当前 步骤
        self.step = step
        # 默认值
        self.value = 0
        # 默认引用数量
        self.count = 0

    def parseRootNode(self):
        rootNode = RootNode()

        # 父类棋盘 走当前 node 走下一步
        checkerboard = self.parentNode.checkerboard
        player = checkerboard.currentPlayer()
        player.play(self.chessPieces, self.step)

        checkerboard.turnNextRound()
        checkerboard.turnNextPlayer()

        print('\n')
        print(self.chessPieces.name(), self.step)
        checkerboard.renderView()

        rootNode.initCheckerboard(checkerboard)

        return rootNode

    def accumulation(self, value):
        self.value += value
        self.count += 1

        # print('accumulation: ', self.value, self.count)
