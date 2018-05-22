# python code for solving 8 puzzle game
# Created by: Vaibhaw Shende
# Created Date: Nov-24-2017
# Updated Date: Mar-22-2018
# File Name: driver.py

import sys
import time
import resource
thisTime = time.time()
useResource = True
verbose = False
depthLimit = 3000
goal_state = [0,1,2,3,4,5,6,7,8]

class Node:
    def __init__ ( self, state, parent, operator, depth, cost):
        self.state = state
        self.parent = parent
        self.operator = operator
        self.depth = depth
        self.cost = cost
        
def dfs_2 (initialState, goalState):
    startTime = time.time()
    if useResource : start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    nodesStack = []
    nodesStack.append( create_node( initialState, None, None, 0, 0 ) )
    thisNode = None
    nodes_expanded = 0
    nodes_explored = []
    max_search_depth = 0
    while (len(nodesStack) > 0):
        thisNode = nodesStack.pop()
        nodes_explored.append (thisNode) 
        if verbose: print (len(nodesStack),"/",len(nodes_explored)," >> ", thisNode.state, thisNode.operator)

        #When GOAL is reached
        if (thisNode.state != None and thisNode.state == goalState):
            running_time = time.time() - startTime
            if useResource : 
                max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, max_ram_usage)
            else: 
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, 0)
        #Add neighbors to Stack
        neighbors, thisDepth = expand_node_revUDLR ( thisNode, nodesStack, nodes_explored )
        nodes_expanded += len (neighbors)
        max_search_depth = max(max_search_depth, thisDepth)
        nodesStack.extend (neighbors)

    return None, None, None, None, None, None, 0 # failure state

def bfs_2 (initialState, goalState):
    startTime = time.time()
    if useResource : start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    nodesQueue = []
    nodesQueue.append( create_node( initialState, None, None, 0, 0 ) )
    thisNode = None
    nodes_expanded = 0
    nodes_explored = []
    max_search_depth = 0
    while (len(nodesQueue) > 0):
        thisNode = nodesQueue.pop(0)
        nodes_explored.append (thisNode) 
        if verbose: print (len(nodesQueue),"/",len(nodes_explored)," >> ", thisNode.state, thisNode.operator)
        #When GOAL is reached
        if (thisNode.state != None and thisNode.state == goalState):
            running_time = time.time() - startTime
            if useResource : 
                max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, max_ram_usage)
            else: 
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, 0)
        #Add neighbors to Queue
        neighbors, thisDepth = expand_node_UDLR( thisNode, nodesQueue, nodes_explored)
        nodes_expanded += len (neighbors)
        max_search_depth = max(max_search_depth, thisDepth)
        nodesQueue.extend (neighbors)
    return None, None, None, None, None, None, 0 # failure state

def ast_2 (initialState, goal_state):
    startTime = time.time()
    if useResource : start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    nodesQueue = []
    nodesQueue.append( create_node( initialState, None, None, 0, 0 ) )
    thisNode = None
    nodes_expanded = 0
    nodes_explored = []
    max_search_depth = 0
    while (len(nodesQueue) > 0):
        thisNode = nodesQueue.pop(0)
        nodes_explored.append (thisNode) 
        if verbose: print (len(nodesQueue),"/",len(nodes_explored)," >> ", thisNode.state, thisNode.operator)
        #When GOAL is reached
        if (thisNode.state != None and thisNode.state == goal_state):
            running_time = time.time() - startTime
            if useResource : 
                max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, max_ram_usage)
            else: 
                return success_state(thisNode, nodes_expanded, max_search_depth, running_time, 0)
        #Add neighbors to Queue
        neighbors, thisDepth = expand_node_leastCost( thisNode, nodesQueue, nodes_explored )
        max_search_depth = max(max_search_depth, thisDepth)
        if neighbors!= None: 
            nodes_expanded += len (neighbors)
            nodesQueue.extend (neighbors)
    return None, None, None, None, None, None, 0 # failure state

def success_state(thisNode, nodes_expanded, max_search_depth, running_time, max_ram_usage):
    path_to_goal = []
    cost_of_path = 0
    search_depth = thisNode.depth
    nodeFromGoalPath = thisNode 
    while nodeFromGoalPath.depth > 0:
        path_to_goal.insert(0, nodeFromGoalPath.operator)
        nodeFromGoalPath = nodeFromGoalPath.parent
        cost_of_path += 1
    return path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, max_ram_usage

def expand_node_UDLR( node, nodes,nodes_explored):
    expanded_nodes = []
    childNodeDepth = node.depth + 1
    if childNodeDepth > depthLimit : 
        print ("depthLimit reached")
        return expanded_nodes, childNodeDepth # Limits depth of search
    # Adding nodes in order of U D L R
    expanded_nodes.append( create_node( UP( node.state ),   node, "Up", childNodeDepth,0 ) )
    if(expanded_nodes[0].state != None) : expanded_nodes[0] = checkDuplicate_2 (expanded_nodes[0],nodes,nodes_explored)
    expanded_nodes.append( create_node( DOWN( node.state ), node, "Down", childNodeDepth,0  ) )
    if(expanded_nodes[1].state != None) : expanded_nodes[1] = checkDuplicate_2 (expanded_nodes[1],nodes,nodes_explored)
    expanded_nodes.append( create_node( LEFT( node.state ), node, "Left", childNodeDepth,0  ) )
    if(expanded_nodes[2].state != None) : expanded_nodes[2] = checkDuplicate_2 (expanded_nodes[2],nodes,nodes_explored)
    expanded_nodes.append( create_node( RIGHT( node.state), node, "Right", childNodeDepth,0  ) )
    if(expanded_nodes[3].state != None) : expanded_nodes[3] = checkDuplicate_2 (expanded_nodes[3],nodes,nodes_explored)
    expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
    return expanded_nodes, childNodeDepth 

def expand_node_revUDLR( node, nodes, nodesExplored):
    expanded_nodes = []
    childNodeDepth = node.depth + 1
    if childNodeDepth > depthLimit : return expanded_nodes, childNodeDepth # Limits depth of search
    # Adding nodes in reverse order of U D L R
    expanded_nodes.append( create_node( RIGHT( node.state ),   node, "Right", childNodeDepth, 0 ) )
    if(expanded_nodes[0].state != None) : expanded_nodes[0] = checkDuplicate_2 (expanded_nodes[0],nodes, nodesExplored)
    expanded_nodes.append( create_node( LEFT( node.state ), node, "Left", childNodeDepth, 0 ) )
    if(expanded_nodes[1].state != None) : expanded_nodes[1] = checkDuplicate_2 (expanded_nodes[1],nodes, nodesExplored)
    expanded_nodes.append( create_node( DOWN( node.state ), node, "Down", childNodeDepth, 0 ) )
    if(expanded_nodes[2].state != None) : expanded_nodes[2] = checkDuplicate_2 (expanded_nodes[2],nodes, nodesExplored)
    expanded_nodes.append( create_node( UP( node.state), node, "Up", childNodeDepth, 0 ) )
    if(expanded_nodes[3].state != None) : expanded_nodes[3] = checkDuplicate_2 (expanded_nodes[3],nodes, nodesExplored)
    expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
    return expanded_nodes, childNodeDepth 

def expand_node_leastCost( node, nodes, nodesExplored):

    childNodeDepth = node.depth + 1
    if childNodeDepth > depthLimit : return expanded_nodes, childNodeDepth # Limits depth of search
    best_nodes = []
    bestMoves =[]
    bestStates = []
    leastMoveCost = 999

    #UP move analysis
    thisState = UP( node.state )
    if thisState != None and isNotDuplicate (thisState, nodes,nodesExplored):
        moveCost = astarHeuristic (thisState, goal_state) 
        if moveCost == leastMoveCost : # In case of another node with same heuristic value
            bestMoves.append ("Up") 
            bestStates.append(thisState)
        elif moveCost < leastMoveCost :            
            leastMoveCost = moveCost
            bestMoves = [] 
            bestStates = []
            bestMoves.append ("Up") 
            bestStates.append(thisState)
    #Down move analysis
    thisState = DOWN( node.state )
    if thisState != None and isNotDuplicate (thisState, nodes,nodesExplored): 
        moveCost = astarHeuristic (thisState, goal_state) 
        if moveCost == leastMoveCost : # In case of another node with same heuristic value
            bestMoves.append ("Down") 
            bestStates.append(thisState)
        elif moveCost < leastMoveCost :            
            leastMoveCost = moveCost
            bestMoves = [] 
            bestStates = []
            bestMoves.append ("Down") 
            bestStates.append(thisState)

    #Left move analysis
    thisState = LEFT( node.state )
    if thisState != None and isNotDuplicate (thisState, nodes,nodesExplored): 
        moveCost = astarHeuristic (thisState, goal_state) 
        if moveCost == leastMoveCost : # In case of another node with same heuristic value
            bestMoves.append ("Left") 
            bestStates.append(thisState)
        elif moveCost < leastMoveCost :            
            leastMoveCost = moveCost
            bestMoves = [] 
            bestStates = []
            bestMoves.append ("Left") 
            bestStates.append(thisState)

    #Right move analysis
    thisState = RIGHT( node.state )
    if thisState != None and isNotDuplicate (thisState, nodes,nodesExplored): 
        moveCost = astarHeuristic (thisState, goal_state) 
        if moveCost == leastMoveCost : # In case of another node with same heuristic value
            bestMoves.append ("Right") 
            bestStates.append(thisState)
        elif moveCost < leastMoveCost :            
            leastMoveCost = moveCost
            bestMoves = [] 
            bestStates = []
            bestMoves.append ("Right") 
            bestStates.append(thisState)

    #return best Node
    if len(bestMoves) == 0 : return  None, childNodeDepth
    else:
        for i in range (len(bestStates)):
            best_nodes.append( create_node( bestStates[i], node, bestMoves[i], childNodeDepth, 0 ) )
            #if(best_nodes[i].state != None) : 
            best_nodes[i] = checkDuplicate_2 (best_nodes[i],nodes, nodesExplored)
        best_nodes = [node for node in best_nodes if node.state != None] #list comprehension!
        return best_nodes, childNodeDepth

def astarHeuristic (currState, goalState):
    if currState == None: return -1
    manhattanDist = 0
    # Reference matrix with distance values wrt to Goal State
    distanceMatrix = [[0,1,2,1,2,3,2,3,4],
                      [1,0,1,2,1,2,3,2,3],
                      [2,1,0,3,2,1,4,3,2],
                      [1,2,3,0,1,2,1,2,3],
                      [2,1,2,1,0,1,2,1,2],
                      [3,2,1,2,1,0,3,2,1],
                      [2,3,4,1,2,3,0,1,2],
                      [3,2,3,2,1,2,1,0,1],
                      [4,3,2,3,2,1,2,1,0]]
    
    for i in range(len(currState)-1):
        cellVal = currState[i]
        manhattanDist += distanceMatrix[cellVal][i]
    return manhattanDist

def checkDuplicate_2(node, nodes, nodesExplored):
    # check if nodes exists in stack or queue
    for i in range ((len(nodes)-1)):
        if node.state == nodes[i].state : 
            return create_node( None, None, None,0,0)
    # check for node in already explored nodes
    for i in range ((len(nodesExplored)-1)):
        if node.state == nodesExplored[i].state : 
            return create_node( None, None, None,0,0)
    return node

def isNotDuplicate (thisState, nodes, nodesExplored):
    if len(thisState) == 0 or thisState == None: return False
    # check is nodes exists in stack or queue
    for i in range ((len(nodes)-1)):
        if thisState == nodes[i].state : 
            return False
    # check for already explored nodes
    for i in range ((len(nodesExplored)-1)):
        if thisState == nodesExplored[i].state : 
            return False
    return True
    
def create_node( state, parent, operator, depth, cost ):
	return Node( state, parent, operator, depth, cost )


def main ():

    method = sys.argv[1]
    starting_state = listFromStr(sys.argv[2])

    if (method == "bfs"): #print("============BFS solution============")
        path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem = bfs_2(starting_state,goal_state)
        if verbose: print_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, delta_mem)
        if (path_to_goal != None): write_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem)
        else : print ("No solution found")
    elif (method == "dfs"): #print("============DFS solution============")
        path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem = dfs_2(starting_state,goal_state)
        if verbose: print_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, delta_mem)
        if (path_to_goal != None): write_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem)
        else : print ("No solution found")
    elif (method == "ast"): #print("============DFS solution============")
        path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem = ast_2(starting_state,goal_state)
        if verbose: print_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, delta_mem)
        if (path_to_goal != None): write_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem)
        else : print ("No solution found")
    else:
        print("======Method Not Selected========")
	    
def UP( state ): # Moves tile up .
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 1, 2]:
		temp = new_state[index - 3]
		new_state[index - 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None # Cannot move

def DOWN( state ): # Moves tile down.
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [6, 7, 8]:
		temp = new_state[index + 3]
		new_state[index + 3] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None # Cannot move

def LEFT( state ): # Moves tile left.
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [0, 3, 6]:
		temp = new_state[index - 1]
		new_state[index - 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None  # Cannot move

def RIGHT( state ): # Moves tile right.
	new_state = state[:]
	index = new_state.index( 0 )
	if index not in [2, 5, 8]:
		temp = new_state[index + 1]
		new_state[index + 1] = new_state[index]
		new_state[index] = temp
		return new_state
	else:
		return None  # Cannot move

def print_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, delta_mem ):
    print("path_to_goal: ",path_to_goal)
    print("cost_of_path: ",cost_of_path)
    print("nodes_expanded: ",nodes_expanded) 
    print("search_depth: ", search_depth) 
    print("max_search_depth: ", max_search_depth) 
    print("running_time: ",(time.time()-thisTime))
    print("max_ram_usage: ",delta_mem)
	
def write_solution(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth, running_time, delta_mem ):
    file = open("output.txt","w")
    file.writelines("path_to_goal: %s\n" % path_to_goal)
    file.writelines("cost_of_path: %s\n" % cost_of_path)
    file.writelines("nodes_expanded: %s\n" % nodes_expanded) 
    file.writelines("search_depth: %s\n" % search_depth) 
    file.writelines("max_search_depth: %s\n" % max_search_depth) 
    file.writelines("running_time: %s\n" % running_time)
    file.writelines("max_ram_usage: %s" % delta_mem)
    file.close()

def listFromStr(str):
	list = []
	for element in str.split(","):
	    list.append(int(element))
	return list
		
main()