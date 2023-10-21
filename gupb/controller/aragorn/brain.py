from gupb.model import arenas, coordinates, weapons
from gupb.model import characters

from gupb.controller.aragorn.memory import Memory
from gupb.controller.aragorn.actions import *



class Brain:
    def __init__(self):
        self.memory = Memory()
        self.actions = {
            'spin': SpinAction(),
            'go_to': GoToAction(),
            'random': RandomAction()
        }

    def decide(self, knowledge: characters.ChampionKnowledge) -> characters.Action:
        self.memory.update(knowledge)

        mapCenter = self.memory.map.passableCenter

        actions = []

        if mapCenter is not None:
            goToAction = self.actions['go_to']
            goToAction.setDestination(mapCenter)
            actions.append(goToAction)

        spinAction = self.actions['spin']
        actions.append(spinAction)
        
        for action in actions:
            ret = action.perform(self.memory)
            
            if ret is not None and ret is not characters.Action.DO_NOTHING:
                return ret
        
        return characters.Action.TURN_RIGHT
    
    def reset(self, arena_description: arenas.ArenaDescription) -> None:
        self.memory.reset(arena_description)
