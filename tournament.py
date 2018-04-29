#given a matrix of pairwise beliefs about who will win, lose between teams
#generate a distribution over outcomes of the tournament.

import numpy as np
from itertools import product, combinations, permutations
import heapq
import random

random.seed(1010101)

def rr_outcomes(n):
    '''Get all possible outcomes of a round robin tournament with n teams.
    Result will be an nxn matrix where outcome(i,j) = i beats j.
    Diagonals will be 0.'''
    num_games = (n*(n-1))/2
    outcomes = []
    for result in product([0,1], repeat=num_games):
        #result is 1-0 vector representing wins, losses for a set of games
        new_outcome = np.zeros((n,n))
        new_outcome[np.triu_indices(n, k=1)] = result
        new_outcome[np.tril_indices(n, k=-1)] = (1-new_outcome.T)[np.tril_indices(n, k=-1)]
        outcomes.append(new_outcome)
    return outcomes

def to_wl_ids(outcome, ids):
    '''Where outcome is an nxn 1-0 matrix for the outcome of a game,
    and ids is a list of n player ids, return two lists in the form winners,
    losers. Use this to index the probability array.'''
    loser_mat, winner_mat = np.meshgrid(group, group)
    return (winner_mat[outcome==1], loser_mat[outcome==1])

#teams will be identified by row #s
#this should be a 32x32 matrix of win-loss probs
#winloss[a,b] = P(a beats b)
wl = np.random.rand(32*32).reshape((32,32))
wl = np.triu(wl,1)
wl += np.tril(1-wl.T, -1)

#group stage
#assign team ids to groups
groups = []
for start_id in range(0,32,4):
    groups.append(np.asarray(range(start_id, start_id+4)))
#group results is nxn where group_result[i,j] -> i winner, j runner up
group_results = np.zeros((32,32))

#for each outcome of each group, calculate probability of win-loss record
for i, group in enumerate(groups):
    for o in rr_outcomes(len(group)):
        #compute scenario probability
        prob_index = to_wl_ids(o, group)
        o_prob = np.prod(wl[prob_index])
        #compute winner(s). Break ties randomly
        wins = np.sum(o, axis=1)
        winners = np.where(wins==np.max(wins))[0]
        winner = np.random.choice(winners)
        #repeat with runner up
        wins[winner] = -1
        runners = np.where(wins == np.max(wins))[0]
        runner_up = np.random.choice(runners)
        #get ids for these teams
        winner_id = group[winner]
        runner_id = group[runner_up]
        #add probability to scenario matrix
        group_results[winner_id, runner_id] += o_prob

#now we have a lookup table for any (winner, runner-up) combination

##################################################################
# Strategy 1: generate group-marginal beliefs about initial bracket
##################################################################

"""Brackets will have the following format:
mx2xn
where n = number of teams, m=number of games at this level of the bracket,
and the teams in col1 play the teams in col2.
bracket[i,j,k] is the probability of team k occupying slot i,j
"""
#generate belief about initial bracket
#for inital bracket, col1 is winners and col2 is runners-up
initial_bracket = np.zeros((8,2,32))
for i, group in enumerate(groups):
    for winner, runner in combinations(group, 2):
        prob = group_results[winner, runner]
        initial_bracket[i,0,winner] += prob
        initial_bracket[i,1,runner] += prob
#reorder so that the appropriate teams play each other
#see get_wl.py for how groups should initially be ordered
#0 is group A, 1 is group B etc.
winners_order = [0,2,4,6,1,3,5,7]
runners_order = [1,3,5,7,0,2,4,6]
initial_bracket[:,0,:] = initial_bracket[winners_order, 0, :]
initial_bracket[:,1,:] = initial_bracket[runners_order, 1, :]

#recursively compute beliefs about next level of bracket
#format: winner of groups 0-1 plays winner of 2-3, winner of 3-4 plays 4-5, etc
def next_level(bracket):
    m, _, n = bracket.shape
    new_bracket = np.zeros((m/2, 2, n))
    for g, p1, p2 in np.ndindex((m,n,n)):
        #odds vs evens
        ngi = g % 2
        game_prob = bracket[g, 0, p1] * bracket[g, 1, p2]
        new_bracket[g/2, ngi, p1] += wl[p1,p2] * game_prob
        new_bracket[g/2, ngi, p2] += wl[p2,p1] * game_prob
    #TODO: normalize at each level? Or just at the end?
    new_bracket = new_bracket / np.sum(new_bracket, axis=-1)[:,:, np.newaxis]
    return new_bracket

b = initial_bracket
while b.shape[0] > 1:
    b = next_level(b)

#compute beliefs about winner
winner_probs = np.zeros(32)
for p1, p2 in np.ndindex((32,32)):
    game_prob = b[0, 0, p1] * b[0,1,p2]
    winner_probs[p1] += game_prob * wl[p1,p2]
    winner_probs[p2] += game_prob * wl[p2,p1]
#normalize
winner_probs = winner_probs/np.sum(winner_probs)
for i in range(32):
    print i, winner_probs[i]





#################################################################
# Strategy 2: Sample from distribution of starting brackets
#################################################################
# #generate a sample of starting brackets
# class BracketSample:
#     def __init__(self, s):
#         self.sample_size = s
#         self.h = []
#         self.id = 0 #meaningless number to avoid exceptions with heap alg
#
#     def push(self, prob, bracket):
#         heapq.heappush(self.h, (prob, self.id, bracket))
#         self.id += 1
#         if len(self.h) > self.sample_size:
#             heapq.heappop(self.h)
#
#     def get_data(self):
#         return [(prob, bracket) for prob,id,bracket in self.h]
#
# group_pairs = [list(permutations(g,2)) for g in groups] #list of all winner, runner-up pairs for each group
# #starting brackets are combinations of these
# probsum=0 #for normalization
# sample_size=10000
# walk_length=1000000
# sample = BracketSample(sample_size)
# #we are going to get a large sample of brackets, keeping the most probable
# for i in xrange(walk_length):
#     bracket = np.zeros((len(groups), 2), int)
#     for g, outcomes in enumerate(group_pairs):
#         bracket[g] = random.choice(outcomes)
#     prob = np.prod(group_results[bracket[:,0], bracket[:,1]])
#     probsum += prob
#     sample.push(prob, bracket)
# print probsum
# print sum(s[0] for s in sample.h)
