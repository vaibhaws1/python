# python code for solving SUDOKU
# Created by: Vaibhaw Shende
# Created Date: Dec-01-2017
# Updated Date: Apr-21-2017

import sys
from copy import deepcopy

# Variables
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
def cross(A, B):
    return [a+b for a in A for b in B]
squares  = cross(rows, cols)

def main ():
    solutions =[]
    if len(sys.argv)==2: # Solve for single puzzle
        # This section executes with following
        # $ python driver.py <sudoku board>
        solutions.append(solve_sudoku_board(sys.argv[1]))
    else: # Solve for multiple puzzles by reading from file
        # This section executes with following
        # $ python driver.py <input file name> SOLVE_MULTIPLE_SUDOKUs
        given_sudoku_boards = read_file(sys.argv[1])
        for given_sudoku_board in given_sudoku_boards :
            solutions.append(solve_sudoku_board(given_sudoku_board))
    write_to_file ("output.txt",solutions)

def solve_sudoku_board(given_sudoku_board):
    csp = csp_class(given_sudoku_board)
    # check first with AC3
    arc_consistency_check = AC3(csp)
    solved = arc_consistency_check and isComplete_ac3(csp)
    if solved:
        sudoku_board_soln = get_solution_string(csp.values)
        print("Solved board with AC3")
        return (sudoku_board_soln+" AC3")
    else : # if AC3 fails
        solution = Backtracking_Search(csp)
        if solution != "failure":
            sudoku_board_soln = get_solution_string(solution)
            print("Solved board with BTS")
            return (sudoku_board_soln+" BTS")
        else:
            print("No Solution Found for board")
    
def get_solution_string(values_dict):
    soln_str = ""
    for sq in squares:
        soln_str += values_dict [sq]
    return soln_str
    
def AC3(csp):
    que = []
    for arc in csp.constraints:
        que.append(arc)
    while len(que) > 0:
        (Xi, Xj) = que.pop(0)
        if Revise(csp, Xi, Xj):
            if len(csp.values[Xi]) == 0:
                return False
            for Xk in (csp.peers[Xi] - set(Xj)):
                que.append((Xk, Xi))
    return True 

def Revise(csp, Xi, Xj):
	revised = False
	values = set(csp.values[Xi])
	for x in values:
		if not isconsistent_AC3(csp, x, Xi, Xj):
			csp.values[Xi] = csp.values[Xi].replace(x, '')
			revised = True 
	return revised 

def isconsistent_AC3(csp, x, Xi, Xj):
	for y in csp.values[Xj]:
		if Xj in csp.peers[Xi] and y!=x:
			return True
	return False
        
def isComplete_ac3(csp):
    for variable in squares:
        if len(csp.values[variable])>1:
            return False
    return True

def Backtracking_Search(csp):
	#return Backtrack({}, csp)
    return Backtrack_with_inference({}, csp)

# Backtracking search - Is lot slower
def Backtrack(assignment, csp):
    if isComplete_bts(assignment):
        return assignment
    var = Select_Unassigned_Variables(assignment, csp)
    for value in csp.values[var]:
        if isConsistent_bts(var, value, assignment, csp):
            assignment[var] = value
            result = Backtrack(assignment, csp)
            if result!="failure":
                return result
            del assignment[var]
    return "failure"

# Backtracking w/ inference
def Backtrack_with_inference(assignment, csp):
    if isComplete_bts(assignment):
        return assignment
    var = Select_Unassigned_Variables(assignment, csp)
    domain = deepcopy(csp.values)
    for value in csp.values[var]:
        if isConsistent_bts(var, value, assignment, csp):
            assignment[var] = value
            inf = {}
            inf = Infer(assignment, inf, csp, var, value)
            if inf != "failure":
                result = Backtrack_with_inference(assignment, csp)
                if result!="failure":
                    return result
            del assignment[var]
            csp.values.update(domain)
    return "failure"

def Infer(assignment, inferences, csp, var, value):
	inferences[var] = value
	for neighbor in csp.peers[var]:
		if neighbor not in assignment and value in csp.values[neighbor]:
			if len(csp.values[neighbor])==1:
				return "failure"
			remaining = csp.values[neighbor] = csp.values[neighbor].replace(value, "")
			if len(remaining)==1:
				flag = Infer(assignment, inferences, csp, neighbor, remaining)
				if flag=="failure":
					return "failure"
	return inferences

def isComplete_bts(assignment):
	return set(assignment.keys())==set(squares)

def Select_Unassigned_Variables(assignment, csp):
	unassigned_variables = dict((squares, len(csp.values[squares])) for squares in csp.values 
                             if squares not in assignment.keys())
	mrv = min(unassigned_variables, key=unassigned_variables.get)
	return mrv

def Order_Domain_Values(var, assignment, csp):
	return csp.values[var]

def isConsistent_bts(var, value, assignment, csp):
	for neighbor in csp.peers[var]:
		if neighbor in assignment.keys() and assignment[neighbor]==value:
			return False
	return True

def forward_check(csp, assignment, var, value):
	csp.values[var] = value
	for neighbor in csp.peers[var]:
		csp.values[neighbor] = csp.values[neighbor].replace(value, '')

class csp_class:
    def __init__ (self, board):
        self.variables = squares
        self.values = self.initValues(board)
        self.unitlist = [['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1'],
                         ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                         ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3'],
                         ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4'],
                         ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'],
                         ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'I6'],
                         ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7'],
                         ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8'],
                         ['A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9'],
                         ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
                         ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                         ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                         ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
                         ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
                         ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
                         ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
                         ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
                         ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9'],
                         ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
                         ['A4', 'A5', 'A6', 'B4', 'B5', 'B6', 'C4', 'C5', 'C6'],
                         ['A7', 'A8', 'A9', 'B7', 'B8', 'B9', 'C7', 'C8', 'C9'],
                         ['D1', 'D2', 'D3', 'E1', 'E2', 'E3', 'F1', 'F2', 'F3'],
                         ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6'],
                         ['D7', 'D8', 'D9', 'E7', 'E8', 'E9', 'F7', 'F8', 'F9'],
                         ['G1', 'G2', 'G3', 'H1', 'H2', 'H3', 'I1', 'I2', 'I3'],
                         ['G4', 'G5', 'G6', 'H4', 'H5', 'H6', 'I4', 'I5', 'I6'],
                         ['G7', 'G8', 'G9', 'H7', 'H8', 'H9', 'I7', 'I8', 'I9']]
        
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)
        self.constraints = {(variable, peer) for variable in self.variables for peer in self.peers[variable]}

    def initValues(self, board):
        i = 0
        values = dict()
        for sq in self.variables:
            if board[i]!='0':
                values[sq] = board[i]
            else:
                values[sq] = digits
            i += 1
        return values
    
def read_file (fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content]

def write_to_file (filename, aList):
    file = open(filename,"w")
    for line in aList:
        lineToWrite = line + "\n"
        file.writelines(lineToWrite )
    file.close()

main()