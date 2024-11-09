from game_bots.bot import Bot
from game_implementation.rules_implementation import MoveManager
class GameRunner:
    '''A class that simulates a go game between two bots'''
    def __init__(self, bot_x: type[Bot], bot_o: Bot, move_manager: MoveManager):
        '''Initializes the game runner'''
        self.bot_x: Bot = bot_x(move_manager, 'x')
        self.bot_o: Bot = bot_o(move_manager, 'o')
        self.piece_to_move: str = 'x'
        self.move_manager: MoveManager = move_manager
        self.board = move_manager.get_empty_board()

    def start_game(self) -> str:
        '''Returns the piece that won the game'''
        has_passed = False
        states_achieved = set() # For detecting ko's
        while(True):
            bot_to_play: Bot = self.bot_x if self.piece_to_move == 'x' else self.bot_o
            move_played: int = bot_to_play.make_move(self.board, has_passed)
            if move_played == -1:
                if has_passed:
                    # Game is over
                    # Counting the territory
                    territory_str = self.move_manager.create_territory(self.board)
                    ct = 0
                    for i in territory_str:
                        if i == 'x':
                            ct += 1
                        elif i == 'o':
                            ct -= 1
                    if ct == 0:
                        self.bot_x.receive_result("Draw")
                        self.bot_o.receive_result("Draw")
                        return '-'
                    elif ct > 0:
                        self.bot_x.receive_result("You won")
                        self.bot_o.receive_result("You lost")
                        return 'x'
                    else:
                        self.bot_x.receive_result("You lost")
                        self.bot_o.receive_result("You won")
                        return 'o'
                    
                else:
                    has_passed = True
                    self.piece_to_move = 'o' if self.piece_to_move == 'x' else 'x'
                    continue
            
            has_passed = False
            # I don't really have a good way to handle ko currently(I will have to think of something)
            # For now, if ko occures, just abort the game
            new_board = self.move_manager.make_move(self.board, move_played, self.piece_to_move)
            if new_board in states_achieved:
                raise ValueError(f"Invalid move by {self.piece_to_move} because of ko")
            
            states_achieved.add(new_board)
            
            self.board = new_board
            self.piece_to_move = 'o' if self.piece_to_move == 'x' else 'x'