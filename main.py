
from graph import Node,Graph
from random import randint,choice,random
import time,heapq
from math import sqrt,inf,log10
# from graphviz import Graph as GraphViz
from matplotlib import pyplot
import numpy as np
from collections import deque
from matplotlib.collections import LineCollection
# import sys
# from memory_profiler import memory_usage

total_nodes = 100  # Number of node
range_of_nodes = 599    # range of plane (x,y) to choose point from
algos = ('BestFS','UCS','A*','SHCS','SAHC','DFS','BFS','BEAM10','HIBE')     # List of Searches
x = [i+1 for i in range(len(algos))]    # plot-x
runs = 1       # number of time graph will be created and search applied

# find time used by function
def timetaken(callfunc):
    def func(*args, **kwargs):
        starttime = time.time()
        tu = callfunc(*args, **kwargs)
        tt = round(time.time() - starttime,3)
        print("Time: {} seconds\n".format(tt))
        if tu != None:
            y1.append(tu[1])
            y2.append(len(tu[0]))
            tts.append(tt)
        return tu
    return func

# prepare path by traversing the destination to start node of graph
def preparepath(a):
    path = [a.name]
    pathlength = 0
    while a.previous != None:
        path.append(a.previous.name)
        pathlength += sqrt(pow(a.previous.x-a.x,2)+pow(a.previous.y-a.y,2))
        a = a.previous
    path.reverse()
    return path,pathlength

# Best First Search, Uniform Cost Search and A* Search
@timetaken
def Search(start,destination,graph,heuristic,showpath=True):
    # graph.calculateH(destination)
    openlist = [(getattr(start,heuristic)(destination),start)]
    closedlist = np.full(total_nodes,False)
    openlistlookup = np.full(total_nodes,False)
    closedn = 0
    openlistlookup[start.name] = True

    heapq.heapify(openlist)
    while len(openlist) != 0:
        current = heapq.heappop(openlist)
        openlistlookup[current[1].name] = False
        closedlist[current[1].name] = True
        closedn += 1
        if current[1].name == destination.name:
            print("Searched Nodes: {}%".format(closedn*100/graph.v))
            path,pathlength = preparepath(current[1])
            print("Destination Found!\nPathLength:{} \nNodes in Path:{} \nStart Node: {} \nEnd Node: {}".format(pathlength,len(path),start.name,destination.name))
            if showpath:
                print("Path:{}".format(path))
            return path,pathlength
        for a in graph.adjacency_list[current[1].name]:
            if closedlist[a.name] == False and openlistlookup[a.name] == False:
                a.previous = current[1]
                heapq.heappush(openlist,(getattr(a,heuristic)(destination) , a))
                openlistlookup[a.name] = True

    print("Searched Nodes: {}%".format(closedn*100/graph.v))
    print("Destination NOT Found!")
    return ([],inf)

# Hill Climbing, BFS, DFS, BEAM and alternate(Hill Climbing, BEAM)
@timetaken
def CurrentSearch(start,destination,graph,ALGO,showpath=True):
    graph.calculateH(destination)
    openlist = deque([start])
    temp = []
    closedlist = np.full(total_nodes,False)
    closedn = 0
    openlistlookup = np.full(total_nodes,False)
    openlistlookup[start.name] = True
    
    while len(openlist) != 0:
        current = openlist.popleft()
        openlistlookup[current.name] = False
        closedlist[current.name] = True
        closedn += 1

        currlist = []
        if current.name == destination.name:
            print("Searched Nodes: {}%".format(closedn*100/graph.v))
            path,pathlength = preparepath(current)
            print("Destination Found!\nPathLength:{} \nNodes in Path:{} \nStart Node: {} \nEnd Node: {}".format(pathlength,len(path),start.name,destination.name))
            if showpath:
                print("Path:{}".format(path))
            return path,pathlength
        for a in graph.adjacency_list[current.name]:
            if closedlist[a.name] == False and openlistlookup[a.name] == False:
                a.previous = current
                currlist.append(a)
                if len(ALGO) < 4 or (len(ALGO) >= 4 and ALGO[:4] != "BEAM"):
                    openlistlookup[a.name] = True

        if ALGO == "DFS":
            currlist.reverse()
            openlist.extendleft(currlist) 
        elif ALGO == "BFS":
            openlist.extend(currlist)
        elif ALGO == "SHC":
            for node in currlist:
                node.calculateG()
            # currlist.sort(key=lambda node:node.g)
            # currlist.reverse()
            if len(currlist) == 0:
                break
            openlist.extendleft([min(currlist,key=lambda node:node.g)])
        elif ALGO == "SAHC":
            # currlist.sort(key=lambda node:node.h)
            # currlist.reverse()
            if len(currlist) == 0:
                break
            openlist.extendleft([min(currlist,key=lambda node:node.h)])
            # openlist.extendleft(currlist)
        elif ALGO[:8] == "SAHCBEAM":
            if len(ALGO) == 8 or ALGO[8] == "S":
                # currlist.sort(key=lambda node:node.h)
                # currlist.reverse()
                # openlist.extendleft(currlist)
                if len(currlist) == 0:
                    break
                openlist.extendleft([min(currlist,key=lambda node:node.h)])
                ALGO = "SAHCBEAMB"
            elif ALGO[8] == "B":
                if len(openlist) != 0:
                    temp += currlist
                else:
                    temp += currlist
                    temp.sort(key=lambda node:getattr(node,"calculateH")(destination))
                    if(len(temp) >= 3):
                        openlist = deque(temp[:3])
                        for i in range(3):
                            if(len(openlist) < i):
                                break
                            openlistlookup[openlist[i].name] = True
                    else:
                        openlist = deque(temp)
                        for i in range(len(temp)):
                            openlistlookup[openlist[i].name] = True
                    temp = []
                    ALGO = "SAHCBEAMS"
        elif len(ALGO) >= 4 and ALGO[:4] == "BEAM":
            if len(openlist) != 0:
                temp += currlist
            else:
                temp += currlist
                temp.sort(key=lambda node:getattr(node,"calculateH")(destination))
                if(len(ALGO) > 4 and len(temp) >= int(ALGO[4:])):
                    openlist = deque(temp[:int(ALGO[4:])])
                    for i in range(int(ALGO[4:])):
                        if(len(openlist) < i):
                            break
                        openlistlookup[openlist[i].name] = True
                elif(len(ALGO) > 4):
                    openlist = deque(temp)
                    for i in range(len(temp)):
                        openlistlookup[openlist[i].name] = True
                else:
                    openlist = deque(temp[:2])
                    openlistlookup[openlist[0].name] = True
                    openlistlookup[openlist[1].name] = True
                temp = []

    print("Searched Nodes: {}%".format(closedn*100/graph.v))
    print("Destination NOT Found!")
    return ([],inf)

def minAll(l):
    minimum = min(l)
    return [i for i, v in enumerate(l) if v == minimum]

@timetaken
def showplots():
    global points
    global edges
    plt = pyplot
    plt.figure(1)
    plt.subplot(3,1,1)
    ppl = plt.bar(x,np.log10(y1),align='center')
    [ppl[my1].set_color('g') for my1 in minAll(y1)]
    plt.ylabel("log10(Pathlength)")
    plt.xticks(x,algos)

    plt.subplot(3,1,3)
    tpl = plt.bar(x,tts,align='center')
    [tpl[my1].set_color('g') for my1 in minAll(tts)]
    plt.ylabel("time")
    plt.xticks(x,algos)
    
    plt.subplot(3,1,2)
    npl = plt.bar(x,np.log10(y2),align='center')
    [npl[my1].set_color('g') for my1 in minAll(y2)]
    plt.ylabel("log10(No. of Nodes)")
    plt.xticks(x,algos)
    plt.show()
    # plt.savefig('result/image'+str(rth+1)+".png")

    # plt.figure(2)
    # points = np.array(points)
    # edges = np.array(edges)
    # ax = points[:,0].flatten()
    # ay = points[:,1].flatten()
    # plt.plot(ax[edges.T], ay[edges.T], linestyle='-', color='y',
    #     markerfacecolor='red', marker='o') 
    # plt.show()


if __name__=="__main__":
    for r in range(runs):
        # sys.stdout=open("result/result"+str(r+1)+".txt","w")

        y1 = []     # plot-y of pathlength 
        y2 = []     # plot-y of number of nodes in path
        tts = []    # plot-y of times
        totaltime = 0   # totaltime for runing one run with each search
        # points = []     # list of points
        edges = []      # list of edges with (point1,point2)
        start_time = time.time()
        
        graph = Graph()
        # graphv = GraphViz(format='png')

        # choosing x and y in x-y plane and add to graph as a node
        for i in range(total_nodes):
            tx,ty = random()*range_of_nodes,random()*range_of_nodes
            graph.addNode(Node(tx,ty,i))
            # points.append([tx,ty])
            # graphv.node(str(i))
        graph.initAdjList()
        edges = graph.addRandomEdges(int(1.5*total_nodes),None)
        
        start = choice(graph.nodes)
        destination = choice(graph.nodes)
        while start == destination:
            destination = choice(graph.nodes)

        print("Time For preparing Graph: {} seconds\n".format(round(time.time() - start_time,3)))


        # best first search
        print("===============Best First Search================")
        Search(start,destination,graph,"calculateH",False)
        # uniform cost search
        print("===============Uniform Cost Search================")
        Search(start,destination,graph,"calculateG",False)
        # A * Algorithm
        print("===============A* Algorithm Search================")
        Search(start,destination,graph,"calculateF",False)
        # simple hill climbing search 
        print("===============Simple Hill Climbing Search================")
        CurrentSearch(start,destination,graph,"SHC",False)
        # steepest ascent hill climbing search 
        print("===============Steepest Ascent Hill Climbing Search================")
        CurrentSearch(start,destination,graph,"SAHC",False)
        # Depth First Search
        print("===============Depth First Search================")
        CurrentSearch(start,destination,graph,"DFS",False)
        # Bredth First Search
        print("===============Bredth First Search================")
        CurrentSearch(start,destination,graph,"BFS",False)
        # Beam Search with width 10
        print("===============Beam Search================")
        CurrentSearch(start,destination,graph,"BEAM10",False)
        # SAHC and BEAM mix
        print("===============Hill Climbing and Beam Search================")
        CurrentSearch(start,destination,graph,"SAHCBEAM",False)
        
        showplots()
        # graph.showGraph(edges)

        # graphv.node(str(start.name),label="start")
        # graphv.node(str(destination.name),label="end")
        # graphv.render(view=True)
        print(graph.v,graph.e,"Total time:{}".format(time.time()-start_time))
        # sys.stdout.close()