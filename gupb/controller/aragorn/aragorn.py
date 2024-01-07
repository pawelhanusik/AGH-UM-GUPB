from collections import defaultdict
import inspect

from gupb import controller
from gupb.model import arenas, coordinates, weapons
from gupb.model import characters

from gupb.controller.aragorn.brain import Brain
from gupb.controller.aragorn import name
from gupb.controller.aragorn.constants import SPOOF_NAME


class AragornController(controller.Controller):
    def __init__(self, first_name :str):
        self.first_name = first_name
        self.brain = Brain()
        self.scores = defaultdict(lambda: 0)
        self.round = 1
    
    def decide(self, knowledge: characters.ChampionKnowledge) -> characters.Action:
        return self.brain.decide(knowledge)

    def praise(self, score: int) -> None:
        self.scores[score] += 1
        print("Aragorn all scores after round")

        scoresOrdered = dict(sorted(self.scores.items(), key=lambda item: item[0], reverse=True))

        for score, count in scoresOrdered.items():
            print(f"{score}: {count}")
        print('-' * 5)

        self.round += 1

    def reset(self, game_no: int, arena_description: arenas.ArenaDescription) -> None:
        self.brain.reset(arena_description)
    
    @property
    def name(self) -> str:
        if SPOOF_NAME:
            callerName = inspect.stack()[1].function

            if callerName == 'pick_action':
                return name.get_current_name()

        return name.OUR_BOT_NAME

    @property
    def preferred_tabard(self) -> characters.Tabard:
        return characters.Tabard.ARAGORN
