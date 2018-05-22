from BaseAI import BaseAI
#from random import randint
depthLimit = 5
log = False
applyStateHeuristic = True
applyMoveHeuristic = True
infinity = float('inf')


class PlayerAI(BaseAI):

    def __init__(self):
        self.util = TreeFunctions()

    def getMove(self, grid):
        
        if log: print(" ")
        # ((1)) Apply Heuristics on first move
        selectedMoves = None
        if applyMoveHeuristic:
            if log: print("*** Applying Move Heurisic ***")
            selectedMoves = self.ApplyHeuristics (grid)
        if log: print(">> Ply1 Move Suggested:",selectedMoves," <<")
    
        # ((2)) Create Tree with Utility Values
        rootNode = Node (None, grid, None, 0)
        self.util.addSuccessors (rootNode, selectedMoves, 0)
        if log: print("DecisionTree:")
        if log: self.util.printTree(rootNode)
        
        # ((3)) Get best move with MiniMax & AlphaBeta pruning
        moveNode = self.Decision_AlphaBeta (rootNode)
        if log: print(">> Move sugg with AlphaBeta:", str(moveNode), " <<")
        move = moveNode.getMove()
        return move if move!= None else None

        #move = randint(0, len(moves) - 1)
        #return moves[move] if moves else None

    def ApplyHeuristics (self, grid):
        moves = grid.getAvailableMoves();
        gridCopy = grid.clone()
        if log: print (">> Heu for Moves  :", moves )
        heuTracker = []
        gridFunc = GridFunctions()

        #iterating through all moves for Grid
        for thisMove in moves: 
            gridCopy = grid.clone()
            gridCopy.move(thisMove)
            cntSpaces = 0 
            cnt2n4 = 0
            cnt4s = 0
            highVal = 1
            highCorner = 0
            cntAdjSimVal = 0
            cntMonotonicity = -1
            diffBtwnAdjCell = 0
            cntSmoothness = 0
            cntDistBetwSimVals = 0
            overallHeu = 0
            bonus = 0
            totGridVal = 0

            gridTranspose = gridFunc.GridTranspose(gridCopy.map) 
            gridAndSelfTrsp = [gridCopy.map , gridTranspose]
            # Iterating through each cell for a Grid
            # gridCopy.map enables checking left-right move
            # gridTranspose enables checking up-down move
            for aGrid in gridAndSelfTrsp:
                dist = 0
                lisOfCellVal = []
                for row in aGrid :
                    onCorner = True
                    prevCell = -1
                    monoRowInc = 0
                    monoRowDec = 0
                    for col in row : # iterating a row
                        highVal = max(col, highVal)
                        totGridVal += col
                        if col == 0: cntSpaces += 1
                        if col == 2 or col == 4: cnt2n4 += 1
                        # Checking for adjacent values
                        if onCorner : onCorner = False
                        else:
                            if col == prevCell : cntAdjSimVal += 1 # Adj similar values
                            if col > prevCell : 
                                monoRowInc += 1 # Monotonicity increasing
                                diffBtwnAdjCell += (col - prevCell) # Diff between Adj cell value
                            if col < prevCell : 
                                monoRowDec += 1 # Monotonicity decreasing
                                diffBtwnAdjCell += (prevCell - col) # Diff between Adj cell value
                        # Checking for dist between similar values greater than 4
                        dist +=1
                        if col in lisOfCellVal : 
                            if col > 128 : cntDistBetwSimVals += dist + 2
                            else : cntDistBetwSimVals += dist
                        elif col > 8 : lisOfCellVal.append(col)
                        # update prevCell value for next iteration
                        prevCell = col 
                        cntSmoothness += (diffBtwnAdjCell / highVal)
                    #End Loop for col
                    if monoRowInc > 2 : cntMonotonicity +=1
                    if monoRowDec > 2 : cntMonotonicity +=1
                #End Loop for aGrid
            #End Loop for gridAndSelfTrsp
            
            aFactor = totGridVal/highVal
            
            #Count High Values in Corner
            if highVal < 65: bonus = 1
            elif highVal > 65 and highVal < 129 : bonus = 2
            elif highVal > 129 and highVal < 257: bonus = 3
            elif highVal > 257 and highVal < 513: bonus = 4
            elif highVal > 513 and highVal < 1025: bonus = 3
            else: bonus = 5
            if gridCopy.map[0][0] == highVal : highCorner+= bonus
            if gridCopy.map[0][3] == highVal : highCorner+= bonus
            if gridCopy.map[3][0] == highVal : highCorner+= bonus
            if gridCopy.map[3][3] == highVal : highCorner+= bonus

            # Heuristics 1 : Bonus of 0.25 for each open squares 
            overallHeu = cntSpaces * 1        
            # Heuristic 2: Penalty of 0.3 for occurance of 2 or 4
            overallHeu -= cnt2n4 * 1         
            # Heuristic 3: Bonus of 3 for large values on edge
            overallHeu += highCorner
            # Heuristic 4: Bonus of 2 for adjacent equal values counting number of potential merges 
            overallHeu += cntAdjSimVal * 2
            # Heuristic 5: Monotonicity, Bonus of 1 for each row having tiles either increasing or decreasing 
            overallHeu += cntMonotonicity * 1
            # Heuristic 6: Smoothness, Penalty of ( total value of diff between neighboring tiles / maxTileValue )
            if highVal < 257: overallHeu -= (cntSmoothness / (aFactor*2))
            else : overallHeu -= (cntSmoothness / (aFactor*3))
            # Heuristic 7: Distance between similar values, penalty for lenght of dist
            if highVal < 257: overallHeu -= (cntDistBetwSimVals / (aFactor*2))
            else: overallHeu -= (cntDistBetwSimVals / (aFactor*3))
            # Heuristic x : something to do with avg and median
            # tbd
            heuTracker.append(overallHeu)

            if log:print (">> [%s]heu [ Sps:%s, 2n4:%s, hCorner:%s, adjSim:%s, Mono:%s, Smooth:%s, DistOfSim:%s aFactor:%s, bonus:%s"%(thisMove, cntSpaces,
                -1*cnt2n4, highCorner,cntAdjSimVal,cntMonotonicity,(-1*cntSmoothness)/aFactor, 
                (-1*cntDistBetwSimVals)/ aFactor, aFactor, bonus))
        #End iterating through all moves for Grid

        heuBestMoves = []
        maxHeu = max(heuTracker)
        for index in range (0, len(heuTracker)):
            if heuTracker[index] == maxHeu: heuBestMoves.append(moves[index])
        
        if log: print (">> Final Heu Score:", heuTracker)
        #if log:print (">> Highest Heu:", maxHeu )
        if log:print (">> Best Move with Heu:", heuBestMoves )
        return heuBestMoves 
                
    def Decision_AlphaBeta (self, starting_state):
        self.util.prt("Initiating AlphaBeta.." )
        alpha = -infinity
        beta = infinity
        best_state = None
        
        for state in starting_state.getSuccessors(): # initial maximizer loop
            (aState, utility) = self.Minimize(state, alpha, beta)
            if utility > alpha:
                alpha = utility
                best_state = state
        
        # This is alternate logic and does not work
        #(best_state, utility) = self.Maximize(starting_state, alpha, beta)
        self.util.prt(">> AlphaBeta: Max Utility : " + str(alpha) +
                      " | Best State is Move:" + str(best_state.getMove()))
        return best_state
        
    def Maximize (self, state, alpha, beta):
        #self.util.prt("AlphaBeta-->MAX: Visited Node :: " + 
        #              str(state.getUtility()) + "/" + str(state.getDepth()))
        if state.terminalTest():
            return (None, state.getUtility())
        maxChild = None
        maxUtility = -infinity

        for child in state.getSuccessors():
            (aChild, utility) = self.Minimize(child, alpha, beta)
            if utility > maxUtility:
                maxUtility = utility
                maxChild = child
            if maxUtility >= beta:
                return (maxChild, maxUtility) # break
            if maxUtility > alpha:
                alpha = maxUtility
        return (maxChild, maxUtility)
    

    def Minimize (self, state, alpha, beta):
        #self.util.prt("AlphaBeta-->MIN: Visited Node :: " + 
        #              str(state.getUtility()) + "/" + str(state.getDepth()))
        if state.terminalTest():
            return (None, state.getUtility())
        minChild = None
        minUtility = infinity

        for child in state.getSuccessors():
            (aChild, utility) = self.Maximize(child, alpha, beta)
            if utility < minUtility:
                minUtility = utility
                minChild = child
            if minUtility <= alpha:
                return (minChild, minUtility) # break
            if minUtility < beta:
                beta = minUtility

        return (minChild, minUtility)

class GridFunctions:

    #def __init__(self):
        
    def GridTranspose (self, gridAsList):
        #if log: print("input Grid: ", gridAsList)
        ret_grid_row1 = []
        ret_grid_row2 = []
        ret_grid_row3 = []
        ret_grid_row4 = []

        for grid_row in gridAsList:
            ret_grid_row1.append(grid_row [0])
            ret_grid_row2.append(grid_row [1])
            ret_grid_row3.append(grid_row [2])
            ret_grid_row4.append(grid_row [3])
            #newGridPointer +=1
        tranGrid = [ret_grid_row1, ret_grid_row2, ret_grid_row3, ret_grid_row4 ]
        #if log: print("tranGrid : ", tranGrid )
        return tranGrid 
    
    def evalGrid(self, grid):
        # Heuristic for State
        if log: print (">> evaluating grid: ", grid.map)
        numSpaces = len(grid.getAvailableCells()) 
        faceAdjtoSpace = 0
        otherFaces = 0
        numMoves = len(grid.getAvailableMoves()) 
        numAlignedVal = 0
        for row in grid.map:
            #print ("row :",row)
            onCorner = True
            prevCell = -1
            for thisCell in row :
                if onCorner: 
                    prevCell = thisCell 
                    onCorner = False
                else:
                    if thisCell == prevCell : 
                        numAlignedVal +=1 # Number of aligned values 
                    if thisCell > 0 and prevCell == 0: 
                        faceAdjtoSpace += 1 # Sum of faces adjacent to a space
                    else: 
                        otherFaces += 1 # Sum of other faces
                #print ("thisCell :",thisCell )
                                
        evalu = 128  
        evalu += ( numSpaces * 128)
        evalu += ( numMoves * 256) 
        if faceAdjtoSpace > 0 : 
            evalu += (4096 / faceAdjtoSpace )
        if otherFaces > 0 : 
            evalu += (otherFaces * 4)
        evalu += (numAlignedVal * 2)
        
        if log: print (">> evaluation=",evalu,
               " (%s, %s, %s, %s, %s )"%(numSpaces, numMoves, 
                 faceAdjtoSpace, otherFaces, numAlignedVal), " <<") 
        return evalu

    def getGridAsList (self, grid) :
        print ("grid map", grid.map)
        return None
        
class TreeFunctions:
    
    def addSuccessors (self, parentNode, ply1Moves=None, parentDepth=1):
        #print (">> add successors called [%d]"%parentDepth)
        treeUtil = TreeFunctions()
        gridUtil = GridFunctions()
        thisDepth = parentDepth +1
        aNode = None
        
        if ply1Moves == None:
            avblMoves = parentNode.getGrid().getAvailableMoves()
        else:
            avblMoves = ply1Moves 
        #print (">> avblMoves ",avblMoves )
        for mv in avblMoves:
            gridCopy = parentNode.getGrid().clone()
            gridCopy.move(mv)
            if (thisDepth < (depthLimit-1)):
                #aNode = Node (mv, gridCopy, gridCopy.getMaxTile(), thisDepth)
                aNode = Node (mv, gridCopy, None, thisDepth)
                parentNode.addChild(aNode)
                treeUtil.addSuccessors (aNode,[mv],thisDepth)
            else:
                # Add Terminal Nodes
                if applyStateHeuristic : 
                    # Adding Evaluation function to Terminal node
                    if log: print("*** Applying State Heurisic ***")
                    aNode = Node (mv, None, gridUtil.evalGrid(gridCopy), thisDepth)
                else:
                    # Adding grid value to Terminal node
                    aNode = Node (mv, None,   gridCopy.getMaxTile(), thisDepth)
                
                parentNode.addChild(aNode)

    
    def printTree (self, node, depth=0):
        treeUtil = TreeFunctions()
        if (node != None ): 
            print (self.getInitChars(depth), node,
                   "(",node.getSuccessorCnt(),")",
                   "[",node.getUtility(),"/",node.getDepth(),"]",
                   ) # print Node with depth
        if node.getSuccessors() == None: 
            return
        elif len(node.getSuccessors()) > 0 :
            for childNode in node.getSuccessors() :
                treeUtil.printTree(childNode,(depth+1))
        else: return

    def getInitChars (self, depth):
        retStr = ">"
        if depth > 0 : 
            barCnt = depth - 1
            while barCnt >= 0 :
                retStr += " | "
                barCnt -= 1
            retStr += " +-"
        return retStr

    def prt(self, logMesg):
        if log: print (logMesg)
            
    def printGrid (self, thisGrid):
        print("|%d | %d | %d | %d|"%(thisGrid.map[0][0],thisGrid.map[0][1],thisGrid.map[0][2],thisGrid.map[0][3]))
        print("|%d | %d | %d | %d|"%(thisGrid.map[1][0],thisGrid.map[1][1],thisGrid.map[1][2],thisGrid.map[1][3]))
        print("|%d | %d | %d | %d|"%(thisGrid.map[2][0],thisGrid.map[2][1],thisGrid.map[2][2],thisGrid.map[2][3]))
        print("|%d | %d | %d | %d|"%(thisGrid.map[3][0],thisGrid.map[3][1],thisGrid.map[3][2],thisGrid.map[3][3]))

class Node:
    def __init__(self, move=5, grid=None, value=0, depth=0):
        self.move = move
        self.grid = grid
        self.value = value
        self.depth = depth
        self.children = []
        
    def __repr__(self):
        name = str(self.move)
        return name
    
    def getGrid (self):
        return self.grid

    def getUtility (self):
        return self.value

    def addChild(self, childNode):
        self.children.append(childNode)
    
    def getChild(self, index): 
        return self.children [index]

    def removeChild(self, index): 
        lenth =len(self.children) 
        if lenth != 0 and index < lenth: 
            self.children.pop(index)
            return True
        else: 
            return False 

    def getSuccessorCnt(self): 
        return len(self.children) 

    def getSuccessors(self):
        if len(self.children) == 0: return None
        return self.children

    def getDepth(self): 
        return self.depth 

    def getMove(self): 
        return self.move
    
    def printIt (self):
        printValue = "move:" + str(self.move) + " / value:" + str(self.value) + " / depth:" + str(self.depth)
        return printValue

    def terminalTest(self):
        if self.grid == None : return True
        else : return False
