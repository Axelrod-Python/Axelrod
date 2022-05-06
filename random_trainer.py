import collections
import statistics
from setuptools import setup
import axelrod as axl
from axelrod import all_strategies
from random import randint
import random
from tqdm import tqdm, trange
from axelrod._strategy_utils import detect_cycle

from axelrod import tournament

first_time_coop = 0
first_time_defections = 0
switchingCD = 0
switchingDC = 0

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
    #players = [axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random(), axl.Random()]
    #players.append(axl.TitForTat())
    for player in tqdm(players):
        match = axl.Match([axl.RiskyQLearner(), player], prob_end = 0.001, p_A = random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]))
        match.play()

def test_tournament():
    """Make q learner play 20 matches against random strategies and detect sequential equilibria and count wins"""
    players = setup_opponents()
    wins = 0
    scores = []
    opponent_scores = []
    for player in tqdm(players):
        stoch = axl.RiskyQLearner()
        match = axl.Match([stoch, player], prob_end = 0.001, p_A = random.choice([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]))
        match.play()
        scores.append(match.final_score()[0])
        opponent_scores.append(match.final_score()[1])
        if match.final_score()[0] > match.final_score()[1]:
            wins += 1
        
        for j in range(1, 20):
            cycle1 = detect_cycle(player.history[-20:], max_size=j)
            cycle2 = detect_cycle(stoch.history[-20:], max_size=j)
            print(cycle1)
            print(cycle2)
    median = statistics.median(scores)
    rank = 20
    for score in opponent_scores:
        if median >= score:
            rank -= 1
    print("Wins: " + str(wins))
    print("Median Score: " + str(median))
    print("Rank: " + str(rank))

def test_match(p_A, first_time_coop, first_time_defections, switchingCD, switchingDC):
    """test general knowledge player against categories of players for behavioral trait in Kloostermann Paper,
    eg. static titfortat, dynamic, players inclined to cooperate and
    players inclined to defect"""
    players = [axl.RiskyQLearner(), axl.TitForTat()] #TESTING STOCHASTIC Q LEARNER AT THE MOMENT
    match = axl.Match(players, prob_end=0.001, p_A = p_A)
    match.play()

    # update statistics
    scores = match.scores()
    if scores[0][0] in [32, 10, 62]:
        # print("COOP")
        first_time_coop += 1
        if scores[1][0] not in [32, 10, 62]:
            #print("SWITCH_CD")
            switchingCD += 1
    else:
        # print("DEFCT")
        first_time_defections += 1
        if scores[1][0] in [32, 10, 62]:
            #print("SWITCH_DC")
            switchingDC += 1
    return first_time_coop, first_time_defections, switchingCD, switchingDC
    

def summary(first_time_coop, first_time_defections, switchingCD, switchingDC):
    """plot cooperation rates in test match over training 
    cycles for different values of p_A to see if who you're 
    trained on heavily impacts results"""
    print("First time coop: " + str(first_time_coop))
    print("First time defections: " + str(first_time_defections))
    print("Switching A to B: " + str(switchingCD))
    print("Switching B to A: " + str(switchingDC))

def run(first_time_coop, first_time_defections, switchingCD, switchingDC):
    """uncomment out first for loop only and save_state() line in match.py for training
    
    uncomment out p_vals until last line of second for loop only to test for behavioral trait, comment out save_state() line in match.py"""

    # #print("length is: " + str(len(all_strategies))+ " and last strat is " + str(all_strategies[len(all_strategies)-35]))
    # for i in trange(20):
    #     train()
    p_vals = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    p_vals = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    for j in tqdm(p_vals):
        first_time_coop, first_time_defections, switchingCD, switchingDC = (0, 0, 0, 0)
        for i in range(50):
            first_time_coop, first_time_defections, switchingCD, switchingDC = test_match(j, first_time_coop, first_time_defections, switchingCD, switchingDC)
        print("p_A: " + str(j))
        summary(first_time_coop, first_time_defections, switchingCD, switchingDC)

#run(first_time_coop, first_time_defections, switchingCD, switchingDC)

test_tournament()
# import matplotlib.pyplot as plt
# player = axl.RiskyQLearner()
# tf = axl.TransitiveFingerprint(player, number_of_opponents=5)
# data = tf.fingerprint(turns=40, seed=3)
# p = tf.plot()
# plt.savefig("6 - Transitive Fingerprint human traits.png")
# players = [axl.StochasticQLearner(), axl.TitForTat(), axl.LookerUp(), axl.Calculator(), axl.RiskyQLearner()]
# tournament = axl.Tournament(players, prob_end=0.001, p_A=0.9)
# results = tournament.play()
# summary = results.summarise()
# import pprint
# pprint.pprint(summary)
# plot = axl.Plot(results)
# _, ax = plt.subplots()
# p = plot.boxplot(ax=ax)
# plt.savefig("mygraph.png")
# p.show()
# strategy = axl.StochasticQLearner
# probe = axl.TitForTat
# af = axl.AshlockFingerprint(strategy, probe)
# data = af.fingerprint(turns=10, repetitions=2, step=0.05, seed=1)
# p = af.plot()
# plt.savefig("2.png")
