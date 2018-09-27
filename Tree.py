class Tree:
    __init__(self):
        pass


class Node:
    __init__(self, parentNode, chessPieces, step):
        # 父类节点
        this.parentNode = parentNode

        # 默认值
        this.value = 0
        # 默认引用数量
        this.count = 0

        # 当前棋子
        this.chessPieces = chessPieces
        # 当前 步骤
        this.step = step

