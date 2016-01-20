"""

"""

from random import choice

import numpy as np
from sklearn.preprocessing import normalize

from sgadx import db, player, distribution, my_sim

NUM_CONSUMERS = 100
NUM_ADVERTISERS = 5
NUM_ADS = 5
DIMENSION = 10
ROUNDS = 100

uniform = distribution.Distribution('uniform')
normal = distribution.Distribution('normal')

db.drop_all()
db.create_all()

## create axis-aligned advertisers
afs = normalize(np.array([1,1,0,0,1,0,0,0,0,0]).reshape(-1,1),axis=0)

## shift the above patern around
advertisers = [my_sim.Advertiser(features=[afs[(i+2*j) % DIMENSION] for i in range(len(afs))]) for j in range(NUM_ADVERTISERS)]

for a in advertisers:
    print a.features
    honest = player.Signal(player=a,features=a.features)
## want to do an intertial rotation
## generate random 
    # perturbed = [normalize(a.features + ]
    db.session.add_all(moves)

db.session.add_all(advertisers)

s = my_sim.Adx(consumers, advertisers);

s.run()