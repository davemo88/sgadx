"""RWM Player

all distributions initially uniform
each round do
    form Q matrix of subdistributions
    sample prediction, receive loss l
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
# import scipy as sp

STATIONARITY_TOLERANCE = 2.22044604925e-15
PLAYER_D = 10
N_ADS = 10
N_THS = 5

class Player(object):

    def __init__(self, type, moves):

        self.type = type
        self.moves = moves
        self.rwm = SwapBanditRWM(len(moves))

    def get_loss(self, s_type, r_type, signal, action):

        pass

class Sender(Player):

    def get_loss(self, s_type, r_type, signal, action):

        loss = np.dot(s_type, signal) + action

    ## convert to [0,1] loss to be minimized
        return 1 - ((loss + 1)/float(3))

class Receiver(Player):

    def get_loss(self, s_type, r_type, signal, action):

        loss = action * np.dot(r_type, s_type)

        return 1-((loss + 1)/float(2))

class BudSender(Player):

    def get_loss(self, s_type, r_type, signal, action):

        loss = np.dot(s_type, signal) + action

    ## convert to [0,1] loss to be minimized
        return 1 - ((loss + 1)/float(3))

class BudReceiver(Player):

    def get_loss(self, s_type, r_type, signal, action):

        loss = np.dot(r_type, signal) \
        + action * np.dot(r_type, s_type)

    ## convert to [0,1] loss to be minimized
        return (1 - (loss + 2)/4)

class SwapBanditRWM(object):

    def __init__(self, N, eta_c=5):

        self.N = N
        self.t = 1
        self.p = np.ones(self.N) / self.N
        self.Q = np.ones((self.N, self.N)) / self.N
        self.Q_weights = np.ones((self.N, self.N)) / self.N

        self.eta_c = eta_c

    def predict(self):

        return list(np.random.multinomial(1, self.p)).index(1)

    def update_Q_weights(self, move_idx, loss):

        for i in range(self.N):

            g = (self.p[i]*loss*self.Q[i][move_idx])/self.p[move_idx]

            self.Q_weights[i][move_idx] = self.Q_weights[i][move_idx] * \
                        np.exp((-np.sqrt(self.eta_c/float(self.t)))*g)

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

def rwm_ad_sg(s=None,r=None,T=10):

    if not s:
        s_type = random_unit_vector()
        signals = [unit_vector_avg(s_type, 
                                   random_unit_vector())\
                    for _ in range(N_ADS)]
        s = Sender(s_type,signals)

    if not r:
        r_type = random_unit_vector()
        r = Receiver(r_type,range(N_THS))

    print "Similarity: {}".format(np.dot(s_type, r_type))
    print "Ad Similarity: "
    for n in range(N_ADS):
        print "Ad {}: {}".format(n, np.dot(s.moves[n],r.type))

    for t in range(1, T+1):
        signal_idx = s.rwm.predict()
        signal = s.moves[signal_idx]
        th_idx = r.rwm.predict()
## th_idx go from 0 to N_THS-1
## dot products go from -1 to 1
        th = ((2*th_idx)-(N_THS-1))  / float(N_THS-1)
        action = int(np.dot(s.type, r.type)>th)
        s_loss = s.get_loss(s.type, r.type, signal, action)
        r_loss = r.get_loss(s.type, r.type, signal, action)

        s.rwm.update_Q_weights(signal_idx, s_loss)
        s.rwm.update_Q()
        print "p_S: ", s.rwm.p#, s_rwm.p.sum()
        s.rwm.update_p()

        r.rwm.update_Q_weights(th_idx, r_loss)
        r.rwm.update_Q()
        r.rwm.update_p()

        print "===> round {}".format(t)
        print "Signal: {} S_Loss: {}".format(signal_idx, s_loss)
        print "Action: {} ({}) R_Loss: {}".format(action, th, r_loss)
        print "p_S: ", s.rwm.p#, s_rwm.p.sum()
        # print "Q_weights_S: ", s.rwm.Q_weights
        print "p_R: ", r.rwm.p#, r_rwm.p.sum()
        # print "Q_weights_R: ", r.rwm.Q_weights

## sanity check on stationary-ness of p
## seems like code could have numerical stability problems
        # assert np.linalg.norm(s.rwm.p - np.dot(s.rwm.p, s.rwm.Q)) \
        # < STATIONARITY_TOLERANCE


if __name__ == "__main__":

    rwm_ad_sg()



