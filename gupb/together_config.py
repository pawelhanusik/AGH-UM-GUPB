from gupb.controller import alpha_gupb
from gupb.controller import ancymon
from gupb.controller import aragorn
from gupb.controller import ares
# from gupb.controller import batman
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

CONFIGURATION = {
    # 'arenas': arena_generator.generate_arenas(50, arena_generator.random_size_generator()),
    # 'arenas': [ 'generated_' + str(i) for i in range(50) ],
    'arenas': [
        'generated_46',
    ],
    
    'controllers': [
        alpha_gupb.AlphaGUPB("AlphaGUPB"), #
        ancymon.AncymonController("Ancymon"), #
        aragorn.AragornController("AragornController"), #
        ares.AresController("Ares"), #
        bob.FSMBot(),
        # batman.BatmanHeuristicsController('Batman'),
        cynamonka.CynamonkaController("Cynamonka"), #
        forrest_gump.ForrestGumpController("Forrest Gump"), #
        # frog.FrogController('Frog'),
        # krombopulos.KrombopulosMichaelController(), #
        maly_konik.MalyKonik("LittlePonny"), #
        mongolek.Mongolek('Mongolek'), #
        pat_i_kot.PatIKotController("Kot i Pat"), #
        # r2d2.RecklessRoamingDancingDruid("R2D2"),
        roger.Roger('1'), #
        random.RandomController("Alice"),
    ],
    
    # 'controllers': [
    #     aragorn.AragornController("AragornController"),
    #     random.RandomController("Alice_0"),
    #     random.RandomController("Alice_1"),
    #     random.RandomController("Alice_2"),
    #     random.RandomController("Alice_3"),
    #     random.RandomController("Alice_4"),
    #     random.RandomController("Alice_5"),
    #     random.RandomController("Alice_6"),
    #     random.RandomController("Alice_7"),
    #     random.RandomController("Alice_8"),
    #     random.RandomController("Alice_9"),
    # ],

    'start_balancing': False,
    'visualise': True,
    'profiling_metrics': ['total', 'avg'],
    'show_sight': False,
    'runs_no': 10,
}
