from chess import *

# Test Cases

happy_cases = [('king', (3,7), (3,4)),      # king case 1 - straight
               ('king', (6,1), (1,6)),      # king case 2 - diagonal
               ('king', (3,7), (5,1)),      # king case 3 - diagonal + straight
               ('knight', (3,6), (5,7)),    # knight case 1 - 1 turn
               ('knight', (3,6), (5,3)),    # knight case 2 - 3 turns
               ('knight', (3,1), (3,8)),    # knight case 3 - 5 turns
               ('bishop', (3,2), (5,1)),    # bishop case 1 - unreachable
               ('bishop', (6,1), (1,6)),    # bishop case 2 - 1 turn
               ('bishop', (6,1), (3,8))]    # bishop case 3 - 2 turns

sad_cases= [('pawn', (3,2), (5,1)),      # invalid piece
            ('king', (9,2), (5,1)),      # outside chess board
            ('king', (3,2.0), (5,1)),    # float instead of integer
            ('king', [3,2], [5,1]),      # lists instead of tuple
            ('king', (5,5), (5,5))]      # same start and end positions

for idx, (piece, start, end) in enumerate(happy_cases,1):
    output = chess_min_moves(piece, start, end)
    print("Happy Case {}".format(idx))
    print("Input: {} {} {}".format(piece, start, end))
    print("Output: {}\n".format(output))
         
for idx, (piece, start, end) in enumerate(sad_cases,1):
    output = chess_min_moves(piece, start, end)
    print("Sad Case {}".format(idx))
    print("Input: {} {} {}".format(piece, start, end))
    print("Output: {}\n".format(output))