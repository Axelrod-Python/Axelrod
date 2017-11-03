from axelrod.action import Action
from random import random,choice
from axelrod.strategies.meta import MetaPlayer
import re

C, D = Action.C, Action.D

class MemoryDecay(MetaPlayer):
    """
    A player utilizes the Tit for Tat stretegy for the first (default) 15 turns,
    at the same time memorizing the opponent's decisions. After the 15 turns have
    passed, the player calculates a 'net cooperation score' (NCS) for his opponent,
    weighing decisions to Cooperate as (default) 1, and to Defect as (default)
    -2. If the opponent's NCS is below 0, the player Defects; otherwise,
    he Cooperates.

    The player's memories of his opponent's decisions have a random chance to be
    altered (i.e., a C decision becomes D or vice versa; default probability
    is 0.03) or deleted (default probability is 0.1).

    Name: Memory Decay
    """
    name = 'Memory Decay'
    classifier = {
        'memory_depth' : float('inf'),
        'long_run_time' : False,
        'stochastic' : True,
        'makes_use_of' : set(),
        'inspects_source' : False,
        'manipulates_source' : False,
        'manipulates_state' : False
    }

    def __init__(self, p_memory_delete: float = 0.1, p_memory_alter: float = 0.03,
                 loss_value: float = -2, gain_value: float = 1,
                 memory: list = None, start_strategy: str = '^Tit For Tat$',
                 start_strategy_duration: int = 15):
        super().__init__()
        self.p_memory_delete = p_memory_delete
        self.p_memory_alter = p_memory_alter
        self.loss_value = loss_value
        self.gain_value = gain_value
        self.memory = [] if memory == None else memory
        self.start_strategy_duration = start_strategy_duration

        self.strategy_search = start_strategy
        strats_list = [str(strategy) for strategy in self.team]
        found_strats_match = [re.match(self.strategy_search, x) for strategy in strats_list]
        found_strats_str = [found.group(0) if found is not None else None
                            for found in found_strats]
        found_strats = [[i, strategy] for i, strategy in enumerate(found_strats_str)
                        if strategy is not None]
        if len(found_strats) > 1:
            pass #de napravi nešto

    def gain_loss_tr(self):
        self.gloss_values = [*map(lambda x: self.loss_value if x == D else
                                         self.gain_value, self.memory)]

    def mem_alter(self):
        alter = choice(range(0, len(self.memory)))
        self.memory[alter] = self.memory[alter].flip()

    def mem_delete(self):
        self.memory.pop(choice(range(0, len(self.memory))))

    def strategy(self, opponent: Player) -> Action:
        try:
            self.memory.append(opponent.history[-1])
        except IndexError:
            pass
        if len(self.history) < self.start_strategy_duration:
            return self.strategies[self.start_strategy].strategy(opponent)
        else:
            if random() <= self.p_memory_alter:
                self.mem_alter()
            if random() <= self.p_memory_delete:
                self.mem_delete()
            self.gain_loss_tr()
            if sum(self.gloss_values) < 0:
                return D
            else:
                return C
