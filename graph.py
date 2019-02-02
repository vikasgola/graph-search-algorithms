from random import choice
import pygame

class Node:
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.g = 0
        self.h = 0
        self.f = 0
        self.previous = None
    
    def calculateH(self,destination):
        self.h = pow(self.x-destination.x,2)+pow(self.y-destination.y,2)
        return self.h

    def calculateG(self,destination=None):
        if self.previous == None:
            return 0
        self.g = self.previous.g + pow(self.x-self.previous.x,2)+pow(self.y-self.previous.y,2)
        return self.g
    
    def calculateF(self,destination):
        self.f = self.calculateG(destination) + self.calculateH(destination)
        return self.f

class Graph():
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}
        self.v = 0
        self.e = 0

    def showGraph(self,edges):
        pygame.init()
        screen = pygame.display.set_mode((600, 600))
        done = False
        clock = pygame.time.Clock()
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            screen.fill((200, 200, 200))
            for n in self.nodes.values():
                pygame.draw.circle(screen,(0, 100, 255),(int(n.x),int(n.y)),10)
            for e in edges:
                pygame.draw.line(screen,(200, 100, 0),(int(e[0].x),int(e[0].y)),(int(e[1].x),int(e[1].y)),4)
            pygame.display.flip()
            clock.tick(60)

    def addNode(self,node):
        self.nodes[node.name] = node
        self.v += 1

    def initAdjList(self):
        self.adjacency_list = {}
        for name in self.nodes.keys():
            self.adjacency_list[name] = []

    def calculateH(self,destination):
        for node in list(self.nodes.values()):
            node.calculateH(destination)


    def addRandomEdges(self,n,graphv):
        tedges = []
        temp1 = list(self.nodes.values())
        temp2 = [temp1[0]]
        for i in range(n):
            if len(temp1) <= i:
                s1 = choice(range(len(temp1)))
            else:
                s1 = i
            s2 = choice(range(len(temp2)))
            if s1 != s2 :
                tedges.append([temp1[s1], temp2[s2]])
                self.addEdge(temp1[s1], temp2[s2])
                temp2.append(temp1[s1])
                # graphv.edge(str(s1.name),str(s2.name))
        return tedges

    def addAllEdges(self):
        for i in range(self.v):
            for j in range(i+1,self.v):
                self.adjacency_list[self.nodes[j].name].append(self.nodes[i])
                self.adjacency_list[self.nodes[i].name].append(self.nodes[j])
                self.e += 1

    def addEdge(self,node1,node2):
        if node1 not in self.adjacency_list[node2.name] and node2 not in self.adjacency_list[node1.name]:
            self.adjacency_list[node1.name].append(node2)
            self.adjacency_list[node2.name].append(node1)
            self.e += 1

    def clearCache(self):
        for i in range(self.v):
            self.nodes[i].previous = None
            self.nodes[i].g = 0
            self.nodes[i].h = 0
            self.nodes[i].f = 0