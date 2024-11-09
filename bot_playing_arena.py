from game_implementation.game_play_manager import GameRunner
from game_bots.human_bot import HumanBot
from game_bots.minimax_bot import MinimaxBot
from game_implementation.rules_implementation import MoveManager

move_manager = MoveManager(9)
game_runner = GameRunner(HumanBot, MinimaxBot, move_manager)
game_runner.start_game()