import matplotlib.pyplot as plt
import random
import math
from Dijkstra import Dijkstra


class Node(object):
    """
    RRT Node
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None  # index


class RRT(object):
    """
    Class for RRT Planning
    """

    def __init__(self, start, goal, obstacle_list, rand_area):
        """
        Setting Parameter
        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:random sampling Area [min,max]
        """
        self.start = Node(start[0], start[1])
        self.end = Node(goal[0], goal[1])
        self.min_rand = rand_area[0]
        self.max_rand = rand_area[1]
        self.N = 1000
        self.obstacleList = obstacle_list
        self.nodeList = [self.start]
        self.path = []

    def RandomSample(self):
        node_x = random.uniform(self.min_rand, self.max_rand)
        node_y = random.uniform(self.min_rand, self.max_rand)
        for (A, B, C) in self.obstacleList:
            S = abs((B[0]-A[0])*(C[1]-A[1])-(C[0]-A[0])*(B[1]-A[1]))/2
            S1 = abs((B[0]-node_x)*(C[1]-node_y)-(C[0]-node_x)*(B[1]-node_y))/2
            S2 = abs((node_x-A[0])*(C[1]-A[1])-(C[0]-A[0])*(node_y-A[1]))/2
            S3 = abs((B[0]-A[0])*(node_y-A[1])-(node_x-A[0])*(B[1]-A[1]))/2
            if (S1+S2+S3 == S):
                return self.RandomSample()

        node = [node_x, node_y]
        return node

    @staticmethod
    def pointOnLine(a, b, c):
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        d2 = dx*dx + dy*dy
        nx = ((c[0]-a[0])*dx + (c[1]-a[1])*dy) / d2
        nx = min(1, max(0, nx))
        return [dx*nx + a[0], dy*nx + a[1]]

    @staticmethod
    def Length(a, b):
        return (a[0] - b[0])**2 + (a[1] - b[1])**2

    def Nearest(self, rnd):
        d_list = [(node.x - rnd[0])**2 + (node.y - rnd[1])
                  ** 2 for node in self.nodeList]
        min_index = d_list.index(min(d_list))
        minNode = self.nodeList[min_index]
        minPoint = []
        minLength = math.inf
        minA = None
        minB = None
        for i in range(len(self.nodeList)):
            if i == len(self.nodeList) - 1:
                break
            a = self.nodeList[i]
            if a.parent != None:
                b = self.nodeList[a.parent]
            else:
                continue
            point = self.pointOnLine([a.x, a.y], [b.x, b.y], rnd)
            L = self.Length(point, rnd)
            if L < minLength:
                minPoint = point
                minLength = L
                minA = i
                minB = a.parent

        if minLength < self.Length([minNode.x, minNode.y], rnd):
            minPoint = Node(minPoint[0], minPoint[1])
            minPoint.parent = minB
            self.nodeList.append(minPoint)
            self.nodeList[minA].parent = self.nodeList.index(self.nodeList[-1])
            return self.nodeList[minA].parent
        else:
            return min_index

    @staticmethod
    def g(a, b, d):
        r = (d[0] - a[0]) * (b[1] - a[1]) - (d[1] - a[1]) * (b[0] - a[0])
        if abs(r) < 0.000000001:
            return 0
        elif r < 0:
            return -1
        else:
            return 1

    def CollisionFree(self, x, y):
        for (a, b, c) in self.obstacleList:
            r1 = (3 != abs(self.g(x, y, a) + self.g(x, y, b) + self.g(x, y, c)))

            r2 = (2 != abs(self.g(a, b, x) + self.g(a, b, y)))
            r3 = (2 != abs(self.g(b, c, x) + self.g(b, c, y)))
            r4 = (2 != abs(self.g(c, a, x) + self.g(c, a, y)))

            if (r1 and (r2 or r3 or r4)):
                return False
        return True

    def Steer(self, a, b):
        lamb = 5
        j = 2
        for i in range(15):
            z_x = (a.x + lamb * b[0])/(1 + lamb)
            z_y = (a.y + lamb * b[1])/(1 + lamb)
            z = [z_x, z_y]
            if self.CollisionFree([a.x, a.y], z):
                return z
            elif lamb <= 1:
                lamb = 1/j
                j += 1
            else:
                lamb = lamb - 1
        return 0

    def Matrix(self):
        matrix = [[0] * len(self.nodeList) for i in range(len(self.nodeList))]
        for i in range(len(self.nodeList)):
            a = self.nodeList[i]
            if a.parent == None:
                continue
            b = self.nodeList[a.parent]
            length = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
            matrix[i][self.nodeList[i].parent] = length
            matrix[self.nodeList[i].parent][i] = length
        return matrix

    def ShortestPath(self):
        if self.path == "Error":
            return "Error"
        m = self.Matrix()
        path = Dijkstra(m, 0, len(self.nodeList)-1)
        if path == 'Error':
            return "Error"
        self.path = path
        return path

    def Planning(self):
        errors = 0
        for i in range(1, self.N):
            Qrand = self.RandomSample()
            min_index = self.Nearest(Qrand)
            Qn = self.nodeList[min_index]
            Qs = self.Steer(Qn, Qrand)
            if Qs == 0:
                continue
            new_node = Node(Qs[0], Qs[1])
            new_node.parent = min_index
            self.nodeList.append(new_node)

        min_index = self.Nearest([self.end.x, self.end.y])
        min_elem = self.nodeList[min_index]
        self.end.parent = min_index
        if self.CollisionFree([self.end.x, self.end.y], [min_elem.x, min_elem.y]):
            self.nodeList.append(self.end)
        else:
            print("error")
            return False


def main(start, goal, rand_area, obstacle_list):
    print("start RRT path planning")

    # Set Initial parameters
    rrt = RRT(start=start, goal=goal, rand_area=rand_area,
              obstacle_list=obstacle_list)
    if rrt.Planning() == False:
        rrt.path = "Error"
    else:
        rrt.path = rrt.ShortestPath()
        print(rrt.path)
        if rrt.path == 'Error':
            print('Пути нет')
    return rrt
