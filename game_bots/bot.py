from game_implementation.rules_implementation import MoveManager
from abc import ABC, abstractmethod
class Bot(ABC):
    '''An abstract class that represents a notion of a bot'''
    @abstractmethod
    def __init__(self, move_manager: MoveManager, my_piece: str):
        '''Initializes the bot'''

    @abstractmethod
    def make_move(self, board: str, other_pass: bool) -> int:
        '''Make the move given the board'''
