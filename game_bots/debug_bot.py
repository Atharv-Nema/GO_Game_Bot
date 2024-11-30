from game_implementation.rules_implementation import MoveManager
from game_bots.bot import Bot
class DebugBot(Bot):
    '''This is a bot that implements a simple minimax strategy'''
    def __init__(self, move_manager, my_piece):
        self.previous_states = set()
        self.move_manager: MoveManager = move_manager
        self.my_piece = my_piece

    def receive_result(self, result: str):
        pass

    def board_eval(self, board: str, my_piece: str, other_pass: bool):
        '''
        Returns the board evaluation to be used in minimax. This is just the difference in
        territories between the two players.
        Parameters:
        board (str): The go board
        my_piece (str): The piece to be placed
        other_pass (bool): Whether or not the other player has passed
        Returns:
        The evaluation of the board from the perspective of the player placing my_piece
        '''
        # For now, I will just use the territories count
        territory_str = self.move_manager.create_territory(board)
        ct = 0
        for i in territory_str:
            if i == '-':
                ct += 0
            elif i == my_piece:
                ct += 1
            else:
                ct -= 1
        if ct > 0 and other_pass:
            return 1e9 # Because we can just pass and we win
        return ct

    def minimax(self, board: str, my_piece: str, other_pass: bool, levels_left: int) -> tuple[int, int]:
        '''
        Performs a "levels_left" depth minimax search using board_eval
        Parameters:
        board (str): The go board
        my_piece (str): The piece to be placed
        other_pass (bool): Whether or not the other player has passed
        levels_left (int): The depth left to be explored
        Returns:
        A tuple (move, eval), where move is the best move to make and eval is the evaluation
        '''
        # This is just an extremely stupid and slow brute force minimax. It does not even 
        # store the previous computations
        if levels_left == 0:
            # Ideally, we will never use levels_left = 0 to make a move. I am returning an invalid move
            return (-2, self.board_eval(board, my_piece, other_pass)) # As there is nothing left to do
        else:
            valid_moves = self.move_manager.get_next_moves(board, my_piece)
            # I will start by considering to pass
            if other_pass and self.board_eval(board, my_piece, other_pass) == 1e9:
                return (-1, 1e9)
            opponent_piece = 'o' if my_piece != 'o' else 'x'
            max_move = -1
            curr_max = -self.minimax(board, opponent_piece, True, levels_left - 1)[1] # Evaluation if I pass
            ct = 0
            for move in valid_moves:
                new_board = self.move_manager.make_move(board, move, my_piece)
                if new_board in self.previous_states:
                    continue
                ct += 1
                self.previous_states.add(new_board) # Helps to consider ko in the calculations too
                move_eval = -self.minimax(new_board, opponent_piece, False, levels_left - 1)[1] # I need the evaluation part
                self.previous_states.remove(new_board) # Remove the new board added(This is a bit funky)
                if move_eval > curr_max:
                    curr_max = move_eval
                    max_move = move
        
            return (max_move, curr_max)
        
    def make_move(self, board: str, other_pass: bool) -> int:
        '''Returns the move to make based on the minimax'''
        self.previous_states.add(board)
        information = self.minimax(board, self.my_piece, other_pass, 2)
        move = information[0]
        if(move != -1):
            new_board = self.move_manager.make_move(board, move, self.my_piece)
            self.previous_states.add(new_board)
        return move

