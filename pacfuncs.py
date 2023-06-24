from pacstructs import *
from PIL import Image
import heapq
import math

from pprint import pprint

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def init_grid(file):
    bc = Image.open(file)
    pix = bc.load()
    bc.close()

    cols = 19
    rows = 19
    cells = [[GridCell() for j in range(cols)] for i in range(rows)]

    # note in array[][] the first number stands for x val and second number
    # stands for the y value

    for x in range(19):
        for y in range(19):
            cells[x][y].gridloc = [x, y]
            cells[x][y].pixelloc = [x * 32, y * 32]
            if pix[x * 32, y * 32] == BLACK:
                cells[x][y].traversable = True
                cells[x][y].coin = True
    cells[8][9].coin = False
    cells[9][9].coin = False
    cells[10][9].coin = False
    cells[9][8].coin = False
    cells[0][7].coin = False
    cells[1][7].coin = False
    cells[2][7].coin = False
    cells[0][11].coin = False
    cells[1][11].coin = False
    cells[2][11].coin = False
    cells[16][7].coin = False
    cells[17][7].coin = False
    cells[18][7].coin = False
    cells[16][11].coin = False
    cells[17][11].coin = False
    cells[18][11].coin = False

    return cells


def colorTraversable(screen, cells):
    for x in range(19):
        for y in range(19):
            if cells[x][y].traversable == True:
                pygame.draw.rect(screen, RED, [x * 32, y * 32, 32, 32])

def checkCollissions(pacman, GREENGHOST, REDGHOST, ORANGEGHOST):
    if pacman.gridloc == GREENGHOST.gridloc:
        return -1
    if pacman.gridloc == REDGHOST.gridloc:
        return -1
    if pacman.gridloc == ORANGEGHOST.gridloc:
        return -1


def BFS(ghost, pac, cells):
    # All costs for movement from one cell to an adjacent traversable cell is 1.
    # All costs for movement from one cell to an adjacent non-traversable
    #   cell is infinity.
    # Will be using the manhattan distance for heuristics

    inf = float("inf")
    Closed = []
    Open = []
    Open.append(SearchNode(ghost.gridloc))
    # open list now contains the start node

    goalNode = SearchNode(pac.gridloc)
    # goalNode is now a SearchNode object with the correct goal gridlocation field

    while len(Open) > 0:

        distance = 0
        index = 0
        expandingNode = Open[0]
        for i in range(len(Open)):
            if expandingNode.f > Open[i].f:
                expandingNode = Open[i]
                index = i

        Closed.append(Open.pop(index))

        # print(expandingNode.gridloc)
        if expandingNode.gridloc == goalNode.gridloc:
            # then we have found the goal node
            goalNode = expandingNode
            break

        expandingNodeX = expandingNode.gridloc[0]
        expandingNodeY = expandingNode.gridloc[1]

        # compute child node cost and f values

        left = SearchNode([expandingNodeX - 1, expandingNodeY], expandingNode)

        right = SearchNode([expandingNodeX + 1, expandingNodeY], expandingNode)

        up = SearchNode([expandingNodeX, expandingNodeY - 1], expandingNode)

        down = SearchNode([expandingNodeX, expandingNodeY + 1], expandingNode)

        rightbool = True
        leftbool = True
        upbool = True
        downbool = True
        for i in Closed:
            if i.gridloc == left.gridloc:
                leftbool = False
            if i.gridloc == right.gridloc:
                rightbool = False
            if i.gridloc == up.gridloc:
                upbool = False
            if i.gridloc == down.gridloc:
                downbool = False

        if rightbool:
            if cells[right.gridloc[0]][right.gridloc[1]].traversable == False:
                right.g = inf
                right.f = inf
            else:
                right.g = right.parent.g + 1
                right.f = right.g
            Open.append(right)
        if leftbool:
            if cells[left.gridloc[0]][left.gridloc[1]].traversable == False:
                left.g = inf
                left.f = inf
            else:
                left.g = left.parent.g + 1
                left.f = left.g
            Open.append(left)
        if upbool:
            if cells[up.gridloc[0]][up.gridloc[1]].traversable == False:
                up.g = inf
                up.f = inf
            else:
                up.g = up.parent.g + 1
                up.f = up.g
            Open.append(up)
        if downbool:
            if cells[down.gridloc[0]][down.gridloc[1]].traversable == False:
                down.g = inf
                down.f = inf
            else:
                down.g = down.parent.g + 1
                down.f = down.g
            Open.append(down)

    # now goal node should have parent node that is on the path.

    node1 = goalNode
    node2 = goalNode

    while node1.gridloc != ghost.gridloc:
        node2 = node1
        node1 = node1.parent

    return node2.gridloc, len(Closed), len(Closed) + len(Open)


def aStarGhost(ghost, pac, cells):
    inf = float("inf")
    Closed = []
    Open = []
    startNode = SearchNode(ghost.gridloc)
    Open.append(startNode)
    goalNode = SearchNode(pac.gridloc)

    while len(Open) > 0:
        expandingNode = min(Open, key=lambda x: x.f)
        Open.remove(expandingNode)
        Closed.append(expandingNode)

        if expandingNode.gridloc == goalNode.gridloc:
            # then we have found the goal node
            goalNode = expandingNode
            break

        expandingNodeX = expandingNode.gridloc[0]
        expandingNodeY = expandingNode.gridloc[1]

        # generate child nodes
        left = SearchNode([expandingNodeX - 1, expandingNodeY], expandingNode)
        right = SearchNode([expandingNodeX + 1, expandingNodeY], expandingNode)
        up = SearchNode([expandingNodeX, expandingNodeY - 1], expandingNode)
        down = SearchNode([expandingNodeX, expandingNodeY + 1], expandingNode)

        for childNode in [left, right, up, down]:
            # check if the child node is valid and not in the closed list
            if childNode.gridloc[0] < 0 or childNode.gridloc[0] >= len(cells) or \
               childNode.gridloc[1] < 0 or childNode.gridloc[1] >= len(cells[0]) or \
               cells[childNode.gridloc[0]][childNode.gridloc[1]].traversable == False or \
               childNode in Closed:
                continue

            # calculate the cost to reach the child node and the heuristic value
            childNode.g = expandingNode.g + 1
            childNode.h = abs(childNode.gridloc[0] - goalNode.gridloc[0]) + \
                           abs(childNode.gridloc[1] - goalNode.gridloc[1])
            childNode.f = childNode.g + childNode.h

            # check if the child node is already in the open list
            existingNode = next((n for n in Open if n.gridloc == childNode.gridloc), None)
            if existingNode:
                if childNode.g < existingNode.g:
                    # if the new path to the child node is better, update the existing node
                    existingNode.g = childNode.g
                    existingNode.parent = expandingNode
                    existingNode.f = existingNode.g + existingNode.h
            else:
                # add the child node to the open list
                Open.append(childNode)

    # build the path from the start node to the goal node
    path = []
    node = goalNode
    while node != startNode:
        path.append(node.gridloc)
        node = node.parent

    return path[-1], len(Closed), len(Open) + len(Closed)


def subGoalAStar(ghost, pac, cells):
    # All costs for movement from one cell to an adjacent traversable cell is 1.
    # All costs for movement from one cell to an adjacent non-traversable
    #   cell is infinity.
    # Will be using the manhattan distance for heuristics

    #return node2.gridloc, len(Closed), len(Closed) + len(Open)
    return None









