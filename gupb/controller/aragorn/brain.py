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

        mapSize = self.memory.map.size
        mapCenter = coordinates.Coords(mapSize[0] / 2, mapSize[1] / 2)

        actionToPerform = self.actions['go_to']
        actionToPerform.setDestination(mapCenter)
        
        return actionToPerform.perform(self.memory)
    
    def reset(self, arena_description: arenas.ArenaDescription) -> None:
        self.memory.reset(arena_description)
