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
import json, time

STATIONARITY_TOLERANCE = 2.22044604925e-15
PLAYER_D = 10
N_ADS = 10
N_THS = 5
T = 100


class Expert:

    def __init__(self, **kwargs):

        self.kwargs = kwargs

    def __call__(self, **kwargs) -> int:
        """ return the index of a move in player.moves

        """

        return 0

class MoveExpert:

    def __init__(self, move_idx:int):

        Expert.__init__(self)
        self.move_idx = move_idx

    def __call__(self, **kwargs) -> int:

        return self.move_idx

class ThresholdExpert:

    def __init__(self, threshold:float):

        Expert.__init__(self)
        self.threshold = threshold

    def __call__(self, signal, type, **kwargs) -> int:

#        print(signal,type)

        return int(np.dot(signal, type) > self.threshold)

class DmpExpert:

    def __init__(self, accuracy:float):

        Expert.__init__(self)
        self.accuracy = accuracy

    def __call__(self, ads, receiver_type,**kwargs):

        rv = random_unit_vector()

        guess = (1 - self.accuracy) * rv + self.accuracy * receiver_type

        vals = [np.dot(guess,ad) for ad in ads]

        return vals.index(max(vals))

class Player:

    def __init__(self, type, moves:List=[], experts:List[Expert]=[]):

        self.type = type
        self.moves = moves
        self.experts = [MoveExpert(i) for i in range(len(self.moves))] if not experts else experts 
        self.exp3 = SwapBanditEXP3(len(self.experts))
        self.min_gain = float(0)
        self.max_gain = float(1)

    def get_gain(self, s_type, r_type, signal, action, scale=False) -> float:

        return float(0) 

    def scale_gain(self, gain:float) -> float:

        return (gain - self.min_gain)/(self.max_gain - self.min_gain)

class Sender(Player):

    def __init__(self, type, moves, experts=[]):
        Player.__init__(self, type, moves, experts)
        self.min_gain = float(-1)
        self.max_gain = float(1)

    def get_gain(self, s_type, r_type, signal, action, scale=False):

        gain = np.dot(s_type, signal) + action

        return gain if not scale else self.scale_gain(gain)

class Receiver(Player):

    def __init__(self, type, moves=[0,1], experts=[]):
        Player.__init__(self, type, moves, experts)
        self.min_gain = float(-1)
        self.max_gain = float(2) 

    def get_gain(self, s_type, r_type, signal, action, scale=False):

        gain = action * np.dot(r_type, s_type)

        return gain if not scale else self.scale_gain(gain) 


class SwapBanditEXP3(object):

    def __init__(self, N:int):

        self.N = N
        self.t = 1
        self.p = np.ones(self.N) / self.N
        self.Q = np.ones((self.N, self.N)) / self.N
        self.Q_weights = np.ones((self.N, self.N))

    def get_eta(self):
        return np.sqrt(8*np.log(self.N)/float(self.t))

    def get_expert_idx(self):

        expert = np.random.multinomial(1, self.p)

     #   print(expert)

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

def setup_sender(): 

    type = random_unit_vector()
    moves = [unit_vector_avg(type, random_unit_vector()) for _ in range(N_ADS)]
    experts = [MoveExpert(i) for i in range(len(moves))] + \
            [DmpExpert(accuracy=0), DmpExpert(accuracy=1)]
    return Sender(type, moves=moves, experts=experts)

def setup_receiver():

    type = random_unit_vector()
    experts = [ThresholdExpert(float(2*i-N_THS+1)/float(N_THS-1)) for i in range(N_THS)]
    return Receiver(type, experts=experts)

def write_summary_json(s, r, sim_id):

    summary = {
            'player_d': PLAYER_D,
            'n_ads': N_ADS,
            'n_ths': N_THS,
            'T': T,
            'player_sim': np.dot(s.type, r.type),
            's_ad_sim': [np.dot(s.type,ad) for ad in s.moves],
            'r_ad_sim': [np.dot(r.type,ad) for ad in s.moves],
            's_p_T': s.exp3.p.tolist(),
            'r_p_T': r.exp3.p.tolist()
            } 
    with open('sim_sum_{}.json'.format(sim_id), 'w') as jsonf:
        json.dump(summary, jsonf)

def write_rec_json(sim_rec, sim_id):
    with open('sim_rec_{}.json'.format(sim_id), 'w') as jsonf:
        json.dump(sim_rec, jsonf)

def exp3_ad_sg(T=T):

    s = setup_sender()
    r = setup_receiver()

##    print("Similarity: {}".format(np.dot(s.type, r.type)))
##    print("Ad Similarity: ")
##    for n in range(N_ADS):
##        print("Ad {}: {}".format(n, np.dot(s.moves[n],r.type)))
    sim_rec = []

    for t in range(1, T+1):
        s_expert_idx = s.exp3.get_expert_idx()
        s_move_idx = s.experts[s_expert_idx](ads=s.moves,receiver_type=r.type)
        signal = s.moves[s_move_idx]
        r_expert_idx = r.exp3.get_expert_idx()
        th = r.experts[r_expert_idx].threshold
        r_move_idx = r.experts[r_expert_idx](signal, r.type)
        action = r.moves[r_move_idx]
        
        s_gain = s.get_gain(s.type, r.type, signal, action)
        r_gain = r.get_gain(s.type, r.type, signal, action)

        s.exp3.update_Q_weights(s_expert_idx, s_gain)
        s.exp3.update_Q()
#        print("p_S: ", s.exp3.p, s.exp3.p.sum())
        s.exp3.update_p()

        r.exp3.update_Q_weights(r_expert_idx, r_gain)
        r.exp3.update_Q()
        r.exp3.update_p()

        rec = {
                't':t,
                's_expert_idx':s_expert_idx,
                'r_expert_idx':r_expert_idx,
                'th':th,
                'signal':signal.tolist(),
                'action':action,
                's_ad_sim':np.dot(signal,s.type),
                'r_ad_sim':np.dot(signal,r.type),
                's_p_t':s.exp3.p.tolist(),
                'r_p_t':r.exp3.p.tolist(),
                's_gain':s_gain,
                'r_gain':r_gain,
                } 

        sim_rec.append(rec)

##        print("===> round {}".format(t))
##        print("Expert: {} ({}) Signal: {} S_Gain: {}".format(s_expert_idx, type(s.experts[s_expert_idx]).__name__, s_move_idx, s_gain))
##        print("Expert: {} (th={}) Action: {} R_Gain: {}".format(r_expert_idx, th, r_move_idx, r_gain))
##        print("p_S: ", s.exp3.p)#, s_exp3.p.sum()
##        # print "Q_weights_S: ", s.exp3.Q_weights
##        print("p_R: ", r.exp3.p)#, r_exp3.p.sum()
        # print "Q_weights_R: ", r.exp3.Q_weights

## sanity check on stationary-ness of p
        # assert np.linalg.norm(s.exp3.p - np.dot(s.exp3.p, s.exp3.Q)) \
        # < STATIONARITY_TOLERANC
    sim_id = int(round(time.time())) 
    write_summary_json(s,r,sim_id)
    write_rec_json(sim_rec,sim_id)


if __name__ == "__main__":

    exp3_ad_sg()

