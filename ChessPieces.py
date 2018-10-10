from enum import Enum
import random

class ChessPiecesType(Enum):
    Wang = '1'
    Ju = '2'
    Ma = '3'
    Pao = '4'
    Xiang ='5'
    Shi = '6'
    Bing = '7'


class ChessPieces:
    def __init__(self, initX, initY, direction, chessPiecesType, checkerboard, player):
        # 默认x，y坐标
        self.initX = initX
        self.initY = direction * initY

        # 当前x，y 坐标
        self.currentX = self.initX
        self.currentY = self.initY

        # 当前的方向 -1 或 1
        self.direction = direction

        # 棋子类型，枚举
        self.chessPiecesType = chessPiecesType

        # 是否存活着
        self.live = True

        # 下一步可以走的 位置
        self.nextSteps = []

        # 棋盘指针
        self.checkerboard = checkerboard
        # 当前的 玩家
        self.player = player

    def name(self):
        swicher = {
            ChessPiecesType.Wang: '王',
            ChessPiecesType.Ju: '车',
            ChessPiecesType.Ma: '马',
            ChessPiecesType.Pao: '炮',
            ChessPiecesType.Xiang: '相',
            ChessPiecesType.Shi: '士',
            ChessPiecesType.Bing: '兵',
        }
        if self.direction > 0:
            return '[{}]'.format(swicher[self.chessPiecesType])
        else:
            return '<{}>'.format(swicher[self.chessPiecesType])
        # return swicher[self.chessPiecesType]

    def pathStr(self):
        return self.pathStrXY(self.currentX, self.currentY)

    def pathStrXY(self, x, y):
        return '{}:{}'.format(int(x), int(y))

    def isInEnemy(self):
        return self.initY * self.direction < 0

    # 可以走的方法
    def stepWays(self):
        return [
            {'x': 0, 'y': 0}
        ]

    # 接下来的走法是否有阻碍
    def isHinderBy(self, baseX, baseY, stepX, stepY):
        # 住要用于 判断 马 和 相 是否被挡住 中间位置
        return False

    # 当前可以 选择的 下一步 位置（一中种走法）
    def updateNextStepsByXY(self, baseX, baseY, stepX, stepY):
        if self.live == False:
            return

        allNextPath = []
        # for aStep in self.stepWays():
        x = stepX
        y = stepY

        nextX = baseX + x
        nextY = baseY + y

        if self.isHinderBy(baseX, baseY, stepX, stepY):
            return allNextPath

        if self.isInScope(nextX, nextY):
            nextPath = {
                'x': nextX,
                'y': nextY
            }
            pathStr = self.pathStrXY(nextX, nextY)

            if self.checkerboard.checkerboardPath.get(pathStr):
                if self.checkerboard.checkerboardPath[pathStr].direction != self.direction:
                    # 杀死 王
                    if self.checkerboard.checkerboardPath[pathStr].chessPiecesType == ChessPiecesType.Wang:
                        return self.updataWinStep(nextPath)
                    allNextPath.append(nextPath)
            else:
                allNextPath.append(nextPath)

        return allNextPath

    # 当前可以 选择的 下一步 位置
    def updateNextSteps(self):
        self.nextSteps = []
        # print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        # print(self.name())
        # print(self.currentX, self.currentY)
        if self.live == False:
            return

        allNextPath = []
        for aStep in self.stepWays():
            x = aStep['x']
            y = aStep['y']
            allP = self.updateNextStepsByXY(self.currentX, self.currentY, x, y)
            if self.player.isWin:
                allNextPath = allP
                break
            else:
                for i in allP:
                    allNextPath.append(i)
        self.nextSteps = allNextPath

    # 获取当前的坐标
    def currentPath(self):
        return {
            'x': self.currentX,
            'y': self.currentY
        }

    # 返回 棋子 存在的范围
    def scope(self):
        return {
            'minX': -8,
            'maxX': 8,
            'minY': -9,
            'maxY': 9
        }

    def isInScope(self, x, y):
        scope = self.scope()
        return x >= scope['minX'] and x <= scope['maxX'] and y >= scope['minY'] and y <= scope['maxY']

    # 走 下一步
    def doNextStep(self, stepPath):
        x = stepPath['x']
        y = stepPath['y']
        oldPathStr = self.pathStr()
        newPathStr = self.pathStrXY(x, y)

        oldItem = self.checkerboard.checkerboardPath.get(newPathStr)
        if oldItem:
            oldItem.live = False

        item = self.checkerboard.checkerboardPath.pop(oldPathStr)
        self.checkerboard.checkerboardPath[newPathStr] = item

        self.currentX = x
        self.currentY = y

    def updataWinStep(self, step):
        # print('-winer')
        # print(self.name())
        # print(step)
        self.player.win(step, self)
        return [step]

# 王
class Wang(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Wang, checkerboard, player)

    def stepWays(self):
        return [
            {'x': 2, 'y': 0},
            {'x': 0, 'y': 2},
            {'x': -2, 'y': 0},
            {'x': 0, 'y': -2}
        ]

    def scope(self):
        if self.direction < 0:
            return {
                'minX': -2,
                'maxX': 2,
                'minY': -9,
                'maxY': -5
            }
        else:
            return {
                'minX': -2,
                'maxX': 2,
                'minY': 5,
                'maxY': 9
            }

# 车
class Ju(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Ju, checkerboard, player)

    def stepWays(self):
        return [
            {'x': 2, 'y': 0},
            {'x': 0, 'y': 2},
            {'x': -2, 'y': 0},
            {'x': 0, 'y': -2}
        ]

    def updateNextStepsByXY(self, baseX, baseY, stepX, stepY):
        if self.live == False:
            return

        allNextPath = []

        nextX = baseX + stepX
        nextY = baseY + stepY

        if self.isInScope(nextX, nextY):
            nextPath = {
                'x': nextX,
                'y': nextY
            }
            pathStr = self.pathStrXY(nextX, nextY)

            if self.checkerboard.checkerboardPath.get(pathStr):
                if self.checkerboard.checkerboardPath[pathStr].direction != self.direction:
                    # 杀死 王
                    if self.checkerboard.checkerboardPath[pathStr].chessPiecesType == ChessPiecesType.Wang:
                        return self.updataWinStep(nextPath)
                    allNextPath.append(nextPath)
            else:
                allNextPath.append(nextPath)
                andNextPath = self.updateNextStepsByXY(nextX, nextY, stepX, stepY)
                for p in andNextPath:
                    allNextPath.append(p)
   
        return allNextPath

# 马
class Ma(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Ma, checkerboard, player)

    # 接下来的走法是否有阻碍
    def isHinderBy(self, baseX, baseY, stepX, stepY):
        absStepX = abs(stepX)
        absStepY = abs(stepY)

        nextX = baseX
        nextY = baseY

        if absStepX > absStepY:
            nextX += stepX / 2
        else:
            nextY += stepY / 2

        pathStr = self.pathStrXY(nextX, nextY)
        # print(pathStr)
        if self.checkerboard.checkerboardPath.get(pathStr):
            return True
        else:
            return False

    def stepWays(self):
        return [
            {'x': 2, 'y': 4},
            {'x': 2, 'y': -4},
            {'x': -2, 'y': 4},
            {'x': -2, 'y': -4},
            {'x': 4, 'y': 2},
            {'x': 4, 'y': -2},
            {'x': -4, 'y': 2},
            {'x': -4, 'y': -2},
        ]

# 炮
class Pao(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Pao, checkerboard, player)

    def stepWays(self):
        return [
            {'x': 2, 'y': 0},
            {'x': 0, 'y': 2},
            {'x': -2, 'y': 0},
            {'x': 0, 'y': -2}
        ]

    def updateNextStepsByXY(self, baseX, baseY, stepX, stepY):
        if self.live == False:
            return

        allNextPath = []

        nextX = baseX + stepX
        nextY = baseY + stepY

        if self.isInScope(nextX, nextY):
            nextPath = {
                'x': nextX,
                'y': nextY
            }
            pathStr = self.pathStrXY(nextX, nextY)

            if self.checkerboard.checkerboardPath.get(pathStr):
                nextXx = nextX + stepX
                nextYy = nextY + stepY
                while True:
                    if self.isInScope(nextXx, nextYy):
                        np = self.pathStrXY(nextXx, nextYy)
                        if self.checkerboard.checkerboardPath.get(np):
                            p = self.checkerboard.checkerboardPath[np]
                            if p.direction != self.direction:
                                # 杀死 王
                                if p.chessPiecesType == ChessPiecesType.Wang:
                                    return self.updataWinStep({'x': nextXx, 'y': nextYy})
                                allNextPath.append({
                                    'x': nextXx,
                                    'y': nextYy
                                })
                            break
                    else:
                        break
                    
                    nextXx = nextXx + stepX
                    nextYy = nextYy + stepY
            else:
                allNextPath.append(nextPath)
                andNextPath = self.updateNextStepsByXY(nextX, nextY, stepX, stepY)
                for p in andNextPath:
                    allNextPath.append(p)
   
        return allNextPath

# 相
class Xiang(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Xiang, checkerboard, player)

    def stepWays(self):
        return [
            {'x': 4, 'y': 4},
            {'x': 4, 'y': -4},
            {'x': -4, 'y': 4},
            {'x': -4, 'y': -4},
        ]
    
    def scope(self):
        if self.direction > 0:
            return {
                'minX': -8,
                'maxX': 8,
                'minY': 1,
                'maxY': 9
            }
        else:
            return {
                'minX': -8,
                'maxX': 8,
                'minY': -9,
                'maxY': -1
            }

        # 接下来的走法是否有阻碍
    def isHinderBy(self, baseX, baseY, stepX, stepY):
        nextX = baseX
        nextY = baseY

        nextX += stepX / 2
        nextY += stepY / 2

        pathStr = self.pathStrXY(nextX, nextY)
        if self.checkerboard.checkerboardPath.get(pathStr):
            return True
        else:
            return False

# 士
class Shi(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Shi, checkerboard, player)

    def stepWays(self):
        return [
            {'x': 2, 'y': 2},
            {'x': 2, 'y': -2},
            {'x': -2, 'y': 2},
            {'x': -2, 'y': -2},
        ]
    
    def scope(self):
        if self.direction < 0:
            return {
                'minX': -2,
                'maxX': 2,
                'minY': -9,
                'maxY': -5
            }
        else:
            return {
                'minX': -2,
                'maxX': 2,
                'minY': 5,
                'maxY': 9
            }

# 兵
class Bing(ChessPieces):
    def __init__(self, initX, initY, direction, checkerboard, player):
        super().__init__(initX, initY, direction, ChessPiecesType.Bing, checkerboard, player)

    def stepWays(self):
        if self.isInEnemy():
            return [
                {'x': 0, 'y': -2 * self.direction},
                {'x': 2, 'y': 0},
                {'x': -2, 'y': 0},
            ]
        else:
            return [
                {'x': 0, 'y': -2 * self.direction},
            ]