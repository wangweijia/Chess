from Player import Player
from ChessPieces import *
import copy 

class Checkerboard:
    MaxCount = 2000

    def __init__(self):
        self.player1 = self.initPlayer(1)
        self.player2 = self.initPlayer(-1)

        self.allPlayers = [
            self.player1,
            self.player2
        ]

        self.nextPlayer = 0
        self.checkerboardPath = self.initCheckerboard()
        self.round = 0

    def initPlayer(self, direction):
        aPlayer = Player(direction)
        aPlayer.chessPieceList = self.initChessPieces(direction, aPlayer)
        return aPlayer
        
    def initChessPieces(self, direction, player):
        chessPieces = []

        bings = [
            {'y': 3, 'x': -8},
            {'y': 3, 'x': -4},
            {'y': 3, 'x': 0},
            {'y': 3, 'x': 4},
            {'y': 3, 'x': 8}
        ]

        for path in bings:
            aBing = Bing(path['x'], path['y'], direction, self, player)
            chessPieces.append(aBing)
        
        paos = [
            {'y': 5, 'x': -6},
            {'y': 5, 'x': 6},
        ]

        for path in paos:
            aPao = Pao(path['x'], path['y'], direction, self, player)
            chessPieces.append(aPao)

        jus = [
            {'y': 9, 'x': -8},
            {'y': 9, 'x': 8},
        ]

        for path in jus:
            aJu = Ju(path['x'], path['y'], direction, self, player)
            chessPieces.append(aJu)

        mas = [
            {'y': 9, 'x': -6},
            {'y': 9, 'x': 6},
        ]

        for path in mas:
            aMa = Ma(path['x'], path['y'], direction, self, player)
            chessPieces.append(aMa)

        xiangs = [
            {'y': 9, 'x': -4},
            {'y': 9, 'x': 4},
        ]

        for path in xiangs:
            aXiang = Xiang(path['x'], path['y'], direction, self, player)
            chessPieces.append(aXiang)

        shis = [
            {'y': 9, 'x': -2},
            {'y': 9, 'x': 2},
        ]

        for path in shis:
            aShi = Shi(path['x'], path['y'], direction, self, player)
            chessPieces.append(aShi)

        wangs = [
            {'y': 9, 'x': 0},
        ]

        for path in wangs:
            aWang = Wang(path['x'], path['y'], direction, self, player)
            chessPieces.append(aWang)

        return chessPieces
        
    def initCheckerboard(self):
        path = {}

        players = [
            self.player1,
            self.player2
        ]

        for aPlayer in players:
            for chessPiece in aPlayer.chessPieceList:
                key = chessPiece.pathStr()
                path[key] = chessPiece
        
        return path

    def currentPlayer(self):
        return self.allPlayers[self.nextPlayer%2]

    def turnNextPlayer(self):
        self.nextPlayer += 1

    def turnNextRound(self):
        self.round += 1

    def getNextPlayerPlay(self):
        self.turnNextPlayer()
        
        self.turnNextRound()
        player = self.currentPlayer()

        if self.judgmentOver():
            if self.round > self.MaxCount:
                return 0
            else:
                return player.direction
        else:
            player.randomNextStep()
            return self.getNextPlayerPlay()

        if self.allPlayers[0].isWin or self.allPlayers[1].isWin:
            # print('over')
            # print(player)
            return player.direction
        else:
            if self.round > self.MaxCount:
                return 0
            else:
                player.randomNextStep()
                # return 99
                return self.getNextPlayerPlay()

    def judgmentOver(self):
        if self.allPlayers[0].isWin or self.allPlayers[1].isWin:
            return True
        elif self.round > self.MaxCount:
            return True
        return False

    def currentPlayerPlay(self, item, step):
        self.turnNextRound()
        player = self.currentPlayer()
        player.play(item, step)
        # self.renderView()
        # self.turnNextPlayer()

    def renderView(self): 
        # return
        print('- - - - - - - - - - - - - - - - - - - - -')

        for y in range(-9, 10, 2):
            s = '{0: >2} '.format(y)

            for x in range(-8, 9, 2):
                path = '{}:{}'.format(x, y)
                p = self.checkerboardPath.get(path, False)
                if p:
                    s += p.name()
                else:
                    s += '-+--'
            print(s)
            if y == -1:
                print('   -8- -6- -4- -2---0- +2- +4- +6- +8--')
