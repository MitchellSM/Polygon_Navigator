"""

@date: February 7-2018
@author: Mitchell Sulz-Martin


**NOTE: Please read README.txt before testing your own polygons**

"""
from math import sqrt
from numpy import fabs
from queue import PriorityQueue 
from time import time

"""Testing set #1"""
Start = (1, 1)
Goal = (14, 9)
test_polygons = [ [(3, 1), (8, 1), (8, 3), (3, 3)],
                  [(5, 5), (7, 8), (5, 9)],
                  [(0, 5), (2, 4), (3, 6), (2, 8), (1, 7)],
                  [(9, 3), (12, 1), (10, 5)],
                  [(13, 2), (15, 3), (15, 6), (13, 6)],
                  [(11, 9), (12, 7), (14, 8), (13, 10)]]

"""Testing set #2"""
Start2 = (3, 16)
Goal2 = (14, 2)
test_polygons2 = [  [(4, 11), (8, 9), (5, 14)],
                    [(8, 14), (13, 17), (12, 20), (8, 19)],
                    [(8, 7), (11, 10), (9, 12)],
                    [(12, 3), (16, 5), (14, 8), (10, 8)]]



class Polygon:
    """Definition of a polygon"""
    def __init__(self, test_vertices=[]):
        #vertices are counterclockwise, starting from the smallest x coord
        self._vertices = test_vertices

class Node:
    """General node definition"""
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent

class ASNode(Node):
    """A node for A* search"""
    def __init__(self, point, parent, g=0, h=0):
        self.point = point
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

class PQNode(Node):
    """A node for priority queue based searching"""
    def __init__(self, point, parent, dis):
        self.point = point
        self.parent = parent
        self.g = dis
    
    def __lt__(self, other):
        return self.g < other.g

class StateSpace:
    """State space as defined in the question"""
    def __init__(self):
        self.polygons = []
        self.goal = None
        self.start = None

    def test_state_space(self, test_polygons, start, goal):
        """Sets up a predetermined state space""" 
        self.start = start
        self.goal = goal
        for i in test_polygons:
            self.polygons.append(Polygon(i))
        self.polygons.append(Polygon([goal]))   #add goal as a polygon
        return

    def intersection_check(self, p1, p2, poly):
        """checks if two points intersect a polygon"""
        outer = lambda v, u: (v[0]*u[1] - v[1]*u[0]) #outer product 
        d = [(p2[0]-p1[0]), (p2[1]-p1[1])] #direction of line p1p2
        iEnter, iExit, epsilon = 0, 1, 0.0000000001
        poly.append(poly[0])            #Creates a cyclic polygon
        
        for i in range(0, len(poly)-1):
            edge = [(poly[i+1][0]-poly[i][0]), (poly[i+1][1]-poly[i][1])] 
            norm = outer(edge, [(p1[0]-poly[i][0]), (p1[1]-poly[i][1])])
            D = -outer(edge, d)  
            if fabs(D) == 0:            #line p1p2 are parallel to polygon
                del poly[-1]
                return False
            elif fabs(D) < epsilon:     #line p1p2 are almost parallel to polygon
                if norm < 0:            #line p1p2 exceed this polygon
                    del poly[-1]
                    return False
                else:
                    continue            #prevent divide by 0
            intersect = norm/D
            if D < 0:
                if intersect > iEnter:
                    iEnter = intersect  #new maximum enter depth
            else:
                if intersect < iExit:
                    iExit = intersect   #new minimum exit depth
        del poly[-1]                    #remove cyclic vertex
        return True if iEnter < iExit else False

    def get_reachable_vertices(self, viewable_polygons, current):
        """Gets all of the reachable vertices from the current state"""
        reachable_vertices = []
        for i in viewable_polygons:
            for j in i._vertices:
                if not self.intersection_check(current, j, i._vertices):
                    reachable = True
                    for k in viewable_polygons:
                        if self.intersection_check(current, j, k._vertices):
                            reachable = False
                            break
                    if reachable and j != current and j[0] > current[0]:
                        reachable_vertices.append(j)
        return reachable_vertices

    def find_shortest_path_GreedyBFS(self):
        """Find the shortest path using Greedy Best-First Search"""
        PQ = PriorityQueue()
        euc_dis = lambda v, u: sqrt((v[0]-u[0])**2 + (v[1]-u[1])**2)
        PQ.put(PQNode(self.start, None, 0))
        while not PQ.empty():
            n = PQ.get()
            if n.point == self.goal:
                return n
            reachable = self.get_reachable_vertices(self.polygons, n.point)
            for i in reachable:
                PQ.put(PQNode(i, n, euc_dis(i, n.point)))
        return False

    def find_shortest_path_A_star(self):
        """Find the shortest path using A* Search"""
        euc_dis = lambda v, u: sqrt((v[0]-u[0])**2 + (v[1]-u[1])**2)
        fringe = []
        explored = []
        fringe.append(ASNode(self.start, None))
        
        while len(fringe)-1 >= 0:
            n = min(fringe, key=lambda x:x.f)
            fringe.remove(n)
            if n.point == self.goal:
                return n
            successors = self.get_reachable_vertices(self.polygons, n.point)
            for i in successors:
                suc = ASNode(i, n, 
                              n.g + euc_dis(i, n.point), 
                              euc_dis(i, self.goal))
                for j in fringe:            #successor is already in fringe
                    if j.point == suc.point:
                        if j.f < suc.f:
                            continue
                for k in explored:          #successor has been explored
                    if k.point == suc.point:
                        if k.f < suc.f:
                            continue
                fringe.append(suc)
            explored.append(n)
        return False

    def generate_path(self, sln, path):
        """Print the path of the solution from goal to start"""
        path.insert(0, sln.point)
        if sln.parent is not None:
            self.generate_path(sln.parent, path)
        else:
            print(end=' - ')
            for i in range(0, len(path)-1):
                print(path[i], end=' -> ')
            print(path[-1])
        return 

#testing set #1:
S = StateSpace()
S.test_state_space(test_polygons, Start, Goal)
a_star_path = []
gbfs_path = []
print("Test polygons set 1:")
print("Start", S.start, "->", S.goal, "Goal\n")

time1 = time()
gBFS_SLN = S.find_shortest_path_GreedyBFS()
time2 = time()
print("Greedy BFS took:", round(time2-time1, 3),"seconds. With the solution:")
S.generate_path(gBFS_SLN, gbfs_path)

time3 = time()
a_star_SLN = S.find_shortest_path_A_star()
time4 = time()
print("\nA* Search took:", round(time4-time3, 3),"seconds. With the solution:")
S.generate_path(a_star_SLN, a_star_path)

#testing set #2:
S2 = StateSpace()
S2.test_state_space(test_polygons2, Start2, Goal2)
a_star_path = []
gbfs_path = []

print("\n\nTest polygons set 2:")
print("Start", S2.start, "->", S2.goal, "Goal\n")

time5 = time()
gBFS_SLN = S2.find_shortest_path_GreedyBFS()
time6 = time()
print("Greedy BFS took:", round(time6-time5, 3),"seconds. With the solution:")
S2.generate_path(gBFS_SLN, gbfs_path)

time7 = time()
a_star_SLN = S2.find_shortest_path_A_star()
time8 = time()
print("\nA* Search took:", round(time8-time7, 3),"seconds. With the solution:")
S2.generate_path(a_star_SLN, a_star_path)





