"""EXP3 Player

all distributions initially uniform
each round do
    form Q matrix of subdistributions
    sample prediction, receive gain l
    get stationary distribution of matrix Q
    find stationary distribution p of matrix Q (using eigenvectors)
    distribute l among subalgorithms according to p
    update subdistributions (exponential weighted average)

signaling game setup
all distributions initially uniform
each round do
    get Q_S
    sample \sigma
    get Q_R
    sample \alpha
    get \mu_S, \mu_R
    get stationary distributions p_S, p_R
    of matrices Q_S, Q_R (eigenvectors)
    distribute \mu_S and \mu_R according to p_S and p_S 
    update Q_S and Q_R

"""

import numpy as np
#import typing
from typing import List
# import scipy as sp

STATIONARITY_TOLERANCE = 2.22044604925e-15
PLAYER_D = 10
N_ADS = 10
N_THS = 5

class Expert:

    def __init__(self, player:Player, **kwargs):

        self.player = player

    def __call__(**kwargs) -> int:
        """ return the index of a move in player.moves

        """

        return 0

class MoveExpert:

    def __init__(self, player:Player, move_idx:int):

        Expert.__init__(self, player)
        self.move_idx = move_idx

    def __call__() -> int:

        return self.move_idx

class ThresholdExpert:

    def __init__(self, player:Player, threshold:float):

        Expert.__init__(self, player)
        self.threshold = threshold

    def __call__(signal):

        return np.dot(signal, player.type) > self.threshold

class Player:

    def __init__(self, type, moves:List=[], experts:List[Expert]=[], min_gain:float=float(0), max_gain:float=float(1)):

        self.type = type
        self.moves = moves
        self.experts = [MoveExpert(i) for i in range(len(self.moves))] if not experts else experts 
        self.exp3 = SwapBanditEXP3(len(self.experts))
        self.min_gain = min_gain
        self.max_gain = max_gain

    def get_gain(self, s_type, r_type, signal, action, scale=False) -> float:

        return float(0) 

    def scale_gain(self, gain:float) -> float:

        return (gain - self.min_gain)/(self.max_gain - self.min_gain)

class Sender(Player):

    def get_gain(self, s_type, r_type, signal, action, scale=False):

        gain = np.dot(s_type, signal) + action

        return gain if not scale else self.scale_gain(gain)

class Receiver(Player):

    def get_gain(self, s_type, r_type, signal, action, scale=False):

        gain = action * np.dot(r_type, s_type)

        return gain if not scale else self.scale_gain(gain) 

class SwapBanditEXP3(object):

    def __init__(self, N:int):

        self.N = N
        self.t = 1
        self.p = np.ones(self.N) / self.N
        self.Q = np.ones((self.N, self.N)) / self.N
        self.Q_weights = np.ones((self.N, self.N))# / self.N

    def get_eta(self):
        return np.sqrt(8*np.log(self.N)/float(self.t))

    def get_expert_idx(self):

        expert = np.random.multinomial(1, self.p)

        print(expert)

        return list(expert).index(1)

    def update_Q_weights(self, expert_idx:int, gain:float):

        for i in range(self.N):

            g = (self.p[i]*gain*self.Q[i][expert_idx])/self.p[expert_idx]

            self.Q_weights[i][expert_idx] = self.Q_weights[i][expert_idx] * \
                        np.exp(self.get_eta()*g)

        self.t += 1

    def update_Q(self): 

        for i in range(self.N):

            self.Q[i] = self.Q_weights[i] / self.Q_weights[i].sum()

    def update_p(self):

        # print "update_p"
        u,v = np.linalg.eig(self.Q.T)
## get the first (only?) eigenvector with eigenvalue 1
## 1e-8 is some precision tolerance
        p = np.array(v[:,np.where(np.abs(u-1.) < 1e-8)[0][0]].flat)
## discard complex components (?)
        p = p.astype(np.float)
        self.p = p / p.sum()

def random_unit_vector(dimension=PLAYER_D):

    v = np.array([np.random.normal() for _ in range(dimension)])
    return v / np.linalg.norm(v)

def unit_vector_avg(u,v):

    return (u + v) / np.linalg.norm(u + v)

def exp3_ad_sg(s=None,r=None,T=100):

    if not s:
        s_type = random_unit_vector()
        signals = [unit_vector_avg(s_type, 
                                   random_unit_vector())\
                    for _ in range(N_ADS)]
        s = Sender(s_type,signals)

    if not r:
        r_type = random_unit_vector()
        r = Receiver(r_type, ths)

    print("Similarity: {}".format(np.dot(s_type, r_type)))
    print("Ad Similarity: ")
    for n in range(N_ADS):
        print("Ad {}: {}".format(n, np.dot(s.moves[n],r.type)))

    for t in range(1, T+1):
        s_expert_idx = s.exp3.predict()
        signal = s.experts[signal_idx]()
        r_expert_idx = r.exp3.predict()
        
## th_idx go from 0 to N_THS-1
## dot products go from -1 to 1
        th = ((2*th_idx)-(N_THS-1))  / float(N_THS-1)
        action = int(np.dot(s.type, r.type)>th)
        s_gain = s.get_gain(s.type, r.type, signal, action)
        r_gain = r.get_gain(s.type, r.type, signal, action)

        s.exp3.update_Q_weights(signal_idx, s_gain)
        s.exp3.update_Q()
        print("p_S: ", s.exp3.p, s_exp3.p.sum())
        s.exp3.update_p()

        r.exp3.update_Q_weights(th_idx, r_gain)
        r.exp3.update_Q()
        r.exp3.update_p()

        print("===> round {}".format(t))
        print("Signal: {} S_Loss: {}".format(signal_idx, s_gain))
        print("Action: {} ({}) R_Loss: {}".format(action, th, r_gain))
        print("p_S: ", s.exp3.p)#, s_exp3.p.sum()
        # print "Q_weights_S: ", s.exp3.Q_weights
        print("p_R: ", r.exp3.p)#, r_exp3.p.sum()
        # print "Q_weights_R: ", r.exp3.Q_weights

## sanity check on stationary-ness of p
        # assert np.linalg.norm(s.exp3.p - np.dot(s.exp3.p, s.exp3.Q)) \
        # < STATIONARITY_TOLERANCE


if __name__ == "__main__":

    exp3_ad_sg()



