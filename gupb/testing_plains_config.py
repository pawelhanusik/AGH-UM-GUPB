from gupb.controller import alpha_gupb
from gupb.controller import ancymon
from gupb.controller import aragorn
from gupb.controller import ares
from gupb.controller import batman
from gupb.controller import bob
from gupb.controller import cynamonka
from gupb.controller import forrest_gump
from gupb.controller import frog
from gupb.controller import krombopulos
from gupb.controller import maly_konik
from gupb.controller import mongolek
from gupb.controller import pat_i_kot
from gupb.controller import random
from gupb.controller import roger
from gupb.controller import r2d2
from gupb.scripts import arena_generator

aragornController = aragorn.AragornController("AragornController")

controllers_all = [
    alpha_gupb.AlphaGUPB("AlphaGUPB"), #
    ancymon.AncymonController("Ancymon"), #
    ares.AresController("Ares"), #
    bob.FSMBot(),
    batman.BatmanHeuristicsController('Batman'),
    cynamonka.CynamonkaController("Cynamonka"), #
    forrest_gump.ForrestGumpController("Forrest Gump"), #
    # frog.FrogController('Frog'),
    mongolek.Mongolek('Mongolek'), #
    maly_konik.MalyKonik("LittlePonny"), #
    pat_i_kot.PatIKotController("Kot i Pat"), #
    r2d2.RecklessRoamingDancingDruid("R2D2"),
    roger.Roger('1'), #
    random.RandomController("Alice"),
    krombopulos.KrombopulosMichaelController(), #
    
    aragornController,
]

controllers_random = [
    aragornController,
    random.RandomController("Alice_0"),
    random.RandomController("Alice_1"),
    random.RandomController("Alice_2"),
    random.RandomController("Alice_3"),
    random.RandomController("Alice_4"),
    random.RandomController("Alice_5"),
    random.RandomController("Alice_6"),
    random.RandomController("Alice_7"),
    random.RandomController("Alice_8"),
    random.RandomController("Alice_9"),
]

controllers_strongest = [
    aragornController,
    roger.Roger('1'),
    ancymon.AncymonController("Ancymon"),
]


CONFIGURATION = {
    # 'arenas': ['testing_plains',],
    'arenas': [ 'generated_' + str(i) for i in range(250) ],
    # 'arenas': ['generated_1',],
    
    # 'controllers': [ aragornController, ],
    'controllers': controllers_all,
    # 'controllers': controllers_random,
    # 'controllers': controllers_strongest,

    'start_balancing': False,
    'visualise': True,
    'profiling_metrics': ['total', 'avg'],
    
    ### SIGHT
    'show_sight': aragornController,
    ## tiles that were ever seen
    # 'visible_tiles_func': lambda visible_coords: [ coords for coords in aragornController.brain.memory.map.terrain if aragornController.brain.memory.map.terrain[coords].seen ],
    ## debug tiles (for example, pathfinding)
    # 'visible_tiles_func': lambda visible_coords: aragornController.brain.memory.debugCoords if aragornController.brain.memory.debugCoords is not None else visible_coords,
    ## loot tiles
    # 'visible_tiles_func': lambda visible_coords: [ coords for coords in aragornController.brain.memory.map.terrain if aragornController.brain.memory.map.terrain[coords].loot is not None ],
    ## enemies simulation
    # 'visible_tiles_func': lambda visible_coords: [ coords for coords in aragornController.brain.memory.map.enemiesPositionsApproximation.getEnemiesTiles() ],
    
    'runs_no': 10,

    # True - step by step, False - run without stopping, 'Aragorn' - step by step only for Aragorn
    # 'step_mode': 'Aragorn',
    # 'end_if_one_left': False,
    # 'spawn_fog': False,
}
