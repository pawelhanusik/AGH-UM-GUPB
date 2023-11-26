from gupb.model import arenas, characters, coordinates, weapons, consumables

from gupb.controller.aragorn.memory import Memory
from gupb.controller.aragorn.actions import *
from gupb.controller.aragorn import utils
from gupb.controller.aragorn.constants import DEBUG, INFINITY, OUR_BOT_NAME
from gupb.model.profiling import profile

import time

class Brain:
    def __init__(self):
        self.memory = Memory()
        self.persistentActions = {}

        self.__initPersistentActions()
        self.wholeTime = 0
    
    def __initPersistentActions(self):
        self.persistentActions = {
            'explore': ExploreAction(),
        }

    def prepareActions(self, knowledge: characters.ChampionKnowledge) -> characters.Action:
        self.memory.update(knowledge)

        # ------------------------------------------
        
        dangerousTilesDict = self.memory.map.getDangerousTilesWithDangerSourcePos(self.memory.tick, 7)

        # ------------------------------------------

        # PREVENT IDLE PENALTY

        if self.memory.willGetIdlePenalty():
            # TODO: allow to decide action, afterwards, if pos will no change - force spin
            spinAction = SpinAction()
            spinAction.setSpin(characters.Action.TURN_LEFT)
            yield spinAction, "Spinning to prevent idle penalty"
        
        # ------------------------------------------

        # PICKING UP POTION

        [closestPotionDistance, closestPotionCoords] = self.memory.getDistanceToClosestPotion()

        if closestPotionDistance is not None and closestPotionDistance < 5:
            goToPotionAction = GoToAction()
            goToPotionAction.setDestination(closestPotionCoords)
            yield goToPotionAction, "Picking nearby potion"

        # ------------------------------------------
        
        # ATTACKING

        oponentInRange = self.memory.getClosestOponentInRange()

        if (
            oponentInRange is not None
            and (
                self.memory.position not in dangerousTilesDict.keys()
                # or (
                    # oponentInRange.health <= self.memory.health
                    # and oponentInRange.health <= consumables.POTION_RESTORED_HP
                # )
            )
        ):
            attackAction = AttackAction()
            yield attackAction, "Attacking, since got oponent in range"

        # ------------------------------------------

        # DEFENDING FROM ATTACKS

        if self.memory.position in dangerousTilesDict:
            takeToOnesLegsAction = TakeToOnesLegsAction()
            takeToOnesLegsAction.setDangerSourcePos(dangerousTilesDict[self.memory.position])
            yield takeToOnesLegsAction, "Defending from attack"
        
        # ------------------------------------------
        
        # PICKING UP WEAPON

        [closestWeaponDistance, closestWeaponCoords] = self.memory.getDistanceToClosestWeapon()

        if closestWeaponDistance is not None and closestWeaponDistance < 15:
            goToWeaponAction = GoToAction()
            goToWeaponAction.setDestination(closestWeaponCoords)
            yield goToWeaponAction, "Picking nearby weapon"
        
        # ------------------------------------------

        # MIST FORCED MOVEMENT

        [menhirPos, prob] = self.memory.map.menhirCalculator.approximateMenhirPos(self.memory.tick)

        if menhirPos is not None and (self.memory.map.mist_radius < 7 or utils.coordinatesDistance(self.memory.position, menhirPos) > self.memory.map.mist_radius / 2):
            goToAroundAction = GoToAroundAction()
            goToAroundAction.setDestination(menhirPos)
            yield goToAroundAction, "Going closer to menhir"
        
        # ------------------------------------------
        
        # Go to closest enemy
        attackClosestEnemyAction = AttackClosestEnemyAction()
        yield attackClosestEnemyAction, "Going closer to enemy"
        
        # ------------------------------------------

        # ROTATE TO SEE MORE

        seeMoreAction = SeeMoreAction()
        yield seeMoreAction, "Rotating to see more"

        # ------------------------------------------

        # EXPLORE THE MAP

        exploreAction = self.persistentActions['explore']
        yield exploreAction, "Exploring action"

        # ------------------------------------------

        # NOTHING TO DO - JUST SPIN

        spinAction = SpinAction()
        yield spinAction, "No action found, spinning"

        # ==========================================

    @profile
    def decide(self, knowledge: characters.ChampionKnowledge) -> characters.Action:
        actionIndexPerformed = 0

        for action, dbg_ac_msg in self.prepareActions(knowledge):
            startTime = time.time()
            ret = action.perform(self.memory)
            endTime = time.time()
            self.wholeTime += endTime - startTime
            
            if ret is not None and ret is not characters.Action.DO_NOTHING:
                if DEBUG: print("[ARAGORN|BRAIN]", action.__class__.__name__, dbg_ac_msg)
                self.onDecisionReturning(ret)
                
                return ret
            
            # if ret is None:
            #     if DEBUG: print("[ARAGORN|BRAIN]", "TRIED TO PERFORM ACTION BUT FAILED!", action.__class__.__name__, dbg_ac_msg)
            
            actionIndexPerformed += 1
        
        if DEBUG: print("[ARAGORN|BRAIN] None of actions returned anything, spinning")
        self.onDecisionReturning(characters.Action.TURN_RIGHT)
        
        return characters.Action.TURN_RIGHT
    
    def reset(self, arena_description: arenas.ArenaDescription) -> None:
        self.memory.reset(arena_description)
        pathfinding.invalidate_PF_cache()

        self.__initPersistentActions()
    
    def onDecisionReturning(self, action: characters.Action):
        if action in [
            characters.Action.TURN_LEFT,
            characters.Action.TURN_RIGHT,
            characters.Action.STEP_FORWARD,
        ]:
            self.memory.resetIdle()
        
        self.memory.addLastAction(action)
