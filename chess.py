import numpy as np
import operator
import os, argparse


# tuple operations utils

def add_tuple(t1, t2):
    return tuple(np.add(t1, t2))

def subtract_tuple(t1, t2):
    return tuple(np.subtract(t1, t2))

def divide_tuple(t1, t2):
    return tuple(np.floor_divide(t1, t2))

def abs_tuple(t):
    return tuple(map(lambda x: abs(x), t))

def string_to_tuple(s):
    return (int(s[0]), int(s[1]))



def king_solve(start, end):
    
    # find x- and y- axis difference between start and end
    delta = subtract_tuple(end, start)
    delta_abs = abs_tuple(delta)

    path = [start]
    
    # get diagonal move (for 1 turn) then move till start and end share an axis
    if 0 not in delta:
        diag_move = divide_tuple(delta, delta_abs)
    while 0 not in delta:
        path.append(add_tuple(path[-1],diag_move))
        delta = subtract_tuple(delta, diag_move)

    # get straight-line move (for 1 turn) then move till start == end
    if sum(delta) != 0:
        divisor = max(abs_tuple(delta))
        straight_move = divide_tuple(delta, (divisor, divisor))
    while sum(delta) != 0:
        path.append(add_tuple(path[-1],straight_move))
        delta = subtract_tuple(delta, straight_move)
    
    return max(delta_abs), path



def knight_solve(start, end):
    
    knight_moves =[(1,2), (2,1), (-1,2), (2,-1),
                   (1,-2), (-2,1), (-1,-2), (-2,-1)]
    
    visited_nodes, unvisited_nodes = [], []
    
    # visiting node stores current node position, the shortest distance and last position
    visiting_node = (start, 0, False)
    
    # implement Djikstra's Algorithm of an unweighted graph
    while visiting_node[0] != end:
        visited_nodes.append(visiting_node)
        for move in knight_moves:
            next_node_pos = add_tuple(visiting_node[0], move)
            
            # check if next node is out of board
            if max(next_node_pos)>8 or min(next_node_pos)<1:
                pass
            
            # check if next node is already in visited node
            if next_node_pos in [node[0] for node in visited_nodes]:
                pass
            
            else:
                new_node = (next_node_pos,
                            visiting_node[1]+1,
                            visiting_node[0])
                unvisited_nodes.append(new_node)
                
        visiting_node = unvisited_nodes.pop(0)

    # trace shortest path backwards from goal
    path = [visiting_node[0]]
    path_node = visiting_node
    
    while path_node[2] != False:
        path.append(path_node[2])
        for node in visited_nodes:
            if node[0] == path_node[2]:
                path_node = node
    
    path.reverse()
    
    return visiting_node[1], path



def bishop_solve(start, end):
    
    # check if start and end are on different colour (i.e. black and white)
    diff_color = abs((sum(start)%2)-(sum(end)%2))
    if diff_color == 1:
        return "NA", "NA. Goal position is unreachable."
    
    # if start and end are same color, goal is reachable
    elif diff_color == 0:
        delta = subtract_tuple(end, start)

        # 1 move needed if start and end share a diagonal
        if abs(delta[0]) == abs(delta[1]):
            return 1, [start, end]
        
        # 2 moves needed if don't share a diagonal - find intersection of start and end diagonals 
        else:
            
            bishop_directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
            
            # get positions of squares in diagonals of start and end
            start_diags, end_diags = [], []
            for direction in bishop_directions:
                start_next, end_next = start, end
                
                while max(start_next)<=8 and min(start_next)>=1:
                    start_diags.append(start_next)
                    start_next = add_tuple(start_next, direction)
                    
                while max(end_next)<=8 and min(end_next)>=1:
                    end_diags.append(end_next)
                    end_next = add_tuple(end_next, direction)
            
            intersections = list(set(start_diags).intersection(end_diags))
            
            return 2, [start, intersections[0], end]

        
        
# input 1       :  chess piece as a string ('king' or 'knight' or 'bishop')
# inputs 2, 3   :  start and end positions as a pair of tuple (x,y) on an 8x8 positive x-y coordiates
# outputs 1, 2  :  minimum number of turns as an integer and shortest path as a list of tuples

def chess_min_moves(piece, start, end):
    
    # catch special cases and errors
    if (type(piece), type(start), type(end)) != (str, tuple, tuple):
        return "Error: Wrong input format. Please input: string, tuple, tuple."
    
    if sum([type(i) == int for i in start])+sum([type(i) == int for i in end]) != 4:
        return "Error: Start and end positions need to be tuples of two integers."
    
    if max(start)>8 or max(end)>8 or min(start)<1 or min(end)<1:
        return "Error: Start and end positions should be within 8x8 chess board."
    
    if start == end:
        return "0 turn needed. Start and end are the same."
    
    # lowercase unstandardized strings such as "King" or "KnIgHt"
    piece = piece.lower()
    
    if piece== "king":
        (min_turns, path) = king_solve(start, end)
    elif piece == "knight":
        (min_turns, path) = knight_solve(start, end)
    elif piece == "bishop":
        (min_turns, path) = bishop_solve(start, end)
    else:
        return "Error: Chess piece not recognized. Enter 'King' or 'Knight' or 'Bishop'."
    
    return "{} needs {} turns using path: {}".format(piece, min_turns, path)
    

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("piece", type=str, help="String containing 'king' or 'knight' or 'bishop'.")
    parser.add_argument("start", type=str, help="String containing xy values of start point, eg. 12 for (1,2).")
    parser.add_argument("end", type=str, help="String containing xy values of end point, eg. 68 for (6,8).")
    args = parser.parse_args()
    
    start = string_to_tuple(args.start)
    end = string_to_tuple(args.end)
    
    print(chess_min_moves(args.piece, start, end))
