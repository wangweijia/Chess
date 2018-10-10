from Checkerboard import *
from Tree import *

def main():
    checkerboard = Checkerboard()
    rootTree = RootNode()
    rootTree.initCheckerboard(checkerboard)
    while not rootTree.checkerboard.judgmentOver():
        for target_list in range(100):
            rootTree.simulation()
        rootTree = rootTree.uct().parseRootNode()

    print('finsh')
    rootTree.checkerboard.renderView()


if __name__ == '__main__':
  main()