from axelrod.action import Action
from random import random,choice
from axelrod.player import Player
from axelrod.strategies.meta import MetaPlayer

C, D = Action.C, Action.D

class MemoryDecay(MetaPlayer):
    """
    A player utilizes the (default) Tit for Tat stretegy for the first (default) 15 turns,
    at the same time memorizing the opponent's decisions. After the 15 turns have
    passed, the player calculates a 'net cooperation score' (NCS) for his opponent,
    weighing decisions to Cooperate as (default) 1, and to Defect as (default)
    -2. If the opponent's NCS is below 0, the player Defects; otherwise,
    he Cooperates.

    The player's memories of his opponent's decisions have a random chance to be
    altered (i.e., a C decision becomes D or vice versa; default probability
    is 0.03) or deleted (default probability is 0.1).

    It's necessary to specify EXACT name of the starting strategy if changing
    the default. Possible strategies can be accessed with the .team attribute.

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
                 memory: list = None, start_strategy: str = 'Tit For Tat',
                 start_strategy_duration: int = 15, team=None):
        super().__init__()
        self.p_memory_delete = p_memory_delete
        self.p_memory_alter = p_memory_alter
        self.loss_value = loss_value
        self.gain_value = gain_value
        self.memory = [] if memory == None else memory
        self.start_strategy_duration = start_strategy_duration

        # searches for the specified start_strategy
        self.strategy_search = start_strategy
        strats_list = [str(strategy) for strategy in self.team]
        if self.strategy_search != 'Tit For Tat':
            try:
                self.strat_ind = strats_list.index(self.strategy_search)
                self.start_strategy = self.team[self.strat_ind]
            except:
                print('Strategy not found. Starting strategy set to Tit For Tat.')
                self.strat_ind = strats_list.index('Tit For Tat')
                self.start_strategy = self.team[self.strat_ind]
        else:
            self.strat_ind = strats_list.index('Tit For Tat')
            self.start_strategy = self.team[self.strat_ind]

    # translates the actions (D and C) to numeric values (loss_value and
    # gain_value)
    def gain_loss_tr(self):
        self.gloss_values = [*map(lambda x: self.loss_value if x == D else
                                         self.gain_value, self.memory)]

    # alters memory entry, i.e. puts C if there's a D and vice versa
    def mem_alter(self):
        alter = choice(range(0, len(self.memory)))
        self.memory[alter] = self.memory[alter].flip()

    # deletes memory entry
    def mem_delete(self):
        self.memory.pop(choice(range(0, len(self.memory))))

    def strategy(self, opponent):
        try:
            self.memory.append(opponent.history[-1])
        except IndexError:
            pass
        if len(self.history) < self.start_strategy_duration:
            play = self.start_strategy.strategy(opponent)
            #self.history.append(play)
            self.start_strategy.history.append(play)
            return play
        else:
            if random() <= self.p_memory_alter:
                self.mem_alter()
            if random() <= self.p_memory_delete:
                self.mem_delete()
            self.gain_loss_tr()
            if sum(self.gloss_values) < 0:
                #self.history.append(D)
                return D
            else:
                #self.history.append(C)
                return C

    # plays (default) TFT for first 15 turns before switching to the NCS
#    def meta_strategy(self, opponent):
#        if len(self.history) < self.start_strategy_duration:
#            return self.start_strategy.strategy(opponent)
#        else:
#            if random() <= self.p_memory_alter:
#                self.mem_alter()
#            if random() <= self.p_memory_delete:
#                self.mem_delete()
#            self.gain_loss_tr()
#            if sum(self.gloss_values) < 0:
#                return D
#            else:
#                return C

#    def strategy(self, opponent: Player) -> Action:
#        MetaPlayer.strategy(opponent)
#        try:
#            self.memory.append(opponent.history[-1])
#        except IndexError:
#            pass
#        if len(self.history) < self.start_strategy_duration:
#            return self.team[self.strat_ind].strategy(opponent)
#        else:
#            if random() <= self.p_memory_alter:
#                self.mem_alter()
#            if random() <= self.p_memory_delete:
#                self.mem_delete()
#            self.gain_loss_tr()
#            if sum(self.gloss_values) < 0:
#                return D
#            else:
#                return C

