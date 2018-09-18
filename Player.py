import random
import math

class Player:
    def __init__(self, direction):
        self.direction = direction
        self.chessPieceList = []
        # 是否已经胜利
        self.isWin = False
        # 决定胜负的 一步
        self.winStep = None
        self.winChessPieces = None

    def win(self, winStep, winChessPieces):
        self.isWin = True
        self.winStep = winStep
        self.winChessPieces = winChessPieces

    # 添加棋子
    def newChessPiece(self, chessPiece):
        self.chessPieceList.append(chessPiece)

    def updataAllStep(self):
        for item in self.chessPieceList:
            item.updateNextSteps()

    def allLiveChessPieces(self):
        lives = []
        for item in self.chessPieceList:
            if item.live and len(item.nextSteps) > 0:
                lives.append(item)
        return lives

    # 随机获取一个棋子
    def randerOneChessPiece(self):
        allLives = self.allLiveChessPieces()
        index = math.floor(random.random() * len(allLives)) 
        item = allLives[index]
        return item

    # 随机获取一个棋子的 下一步
    def randerNextStep(self, item):
        nextSteps = item.nextSteps
        index = math.floor(random.random() * len(nextSteps))
        nextStep = nextSteps[index]
        return nextStep

    def nextStep(self):
        self.updataAllStep()            
        if self.isWin:
            step = self.winStep
            self.winChessPieces.doNextStep(step)
        else:
            item = self.randerOneChessPiece()
            step = self.randerNextStep(item)

            print(item)
            print(step)

            item.doNextStep(step)




        