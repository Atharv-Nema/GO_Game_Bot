def make_move(board, index, color):
    board_list = list(board)
    board_list[index] = color
    return ''.join(board_list)