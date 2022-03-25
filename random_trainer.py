from setuptools import setup
import axelrod as axl
from axelrod import all_strategies
from random import randint
import random
from tqdm import tqdm, trange

from axelrod import tournament

first_time_coop = 0
first_time_defections = 0
switchingAtoB = 0
switchingBtoA = 0

def setup_opponents():
    """generate 20 random indices to select 20 random players listed in 
    all_strategies"""
    players_indices = []
    for i in range(20):
        number = randint(0, len(all_strategies)-35)
        if number in [15, 23, 101, 144]:
            i = i - 1
            continue
        players_indices.append(number)
    players = [axl.all_strategies[i]() for i in players_indices]
    print(players)
    return players

def train():
    """given 20 players, run the tournament to make qlearner learn 
    with variable tournament parameters"""
    players = setup_opponents()
    #players.append(axl.TitForTat())
    for player in tqdm(players):
        match = axl.Match([axl.RiskyQLearner(), player], prob_end = 0.001, p_A = random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]))
        match.play()

def test_match(p_A, first_time_coop, first_time_defections, switchingAtoB, switchingBtoA):
    """test general knowledge player against categories of players,
    eg. static titfortat, dynamic, players inclined to cooperate and
    players inclined to defect"""
    players = [axl.RiskyQLearner(), axl.TitForTat()]
    match = axl.Match(players, prob_end=0.001, p_A = p_A)
    match.play()

    # update statistics
    scores = match.scores()
    if scores[0][0] in [32, 10, 62]:
        # print("COOP")
        first_time_coop += 1
        if scores[1][0] not in [32, 10, 62]:
            # print("SWITCH_CD")
            switchingAtoB += 1
    else:
        # print("DEFCT")
        first_time_defections += 1
        if scores[1][0] in [32, 10, 62]:
            # print("SWITCH_DC")
            switchingBtoA += 1
    return first_time_coop, first_time_defections, switchingAtoB, switchingBtoA
    

def summary(first_time_coop, first_time_defections, switchingAtoB, switchingBtoA):
    """plot cooperation rates in test match over training 
    cycles for different values of p_A to see if who you're 
    trained on heavily impacts results"""
    print("First time coop: " + str(first_time_coop))
    print("First time defections: " + str(first_time_defections))
    print("Switching A to B: " + str(switchingAtoB))
    print("Switching B to A: " + str(switchingBtoA))

def run(first_time_coop, first_time_defections, switchingAtoB, switchingBtoA):
    """run random training simulation about a 1000 times "
    to collect data and plot cooperation rates"""

    #print("length is: " + str(len(all_strategies))+ " and last strat is " + str(all_strategies[len(all_strategies)-35]))
    # for i in trange(15):
    #     train()
    p_vals = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    #p_vals = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    for j in tqdm(p_vals):
        first_time_coop, first_time_defections, switchingAtoB, switchingBtoA = (0, 0, 0, 0)
        for i in range(50):
            first_time_coop, first_time_defections, switchingAtoB, switchingBtoA = test_match(j, first_time_coop, first_time_defections, switchingAtoB, switchingBtoA)
        print("p_A: " + str(j))
        summary(first_time_coop, first_time_defections, switchingAtoB, switchingBtoA)

run(first_time_coop, first_time_defections, switchingAtoB, switchingBtoA)

