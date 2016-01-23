"""

"""

from random import choice

import numpy as np

from sgadx import db, player, distribution, util, my_sim

NUM_CONSUMERS = 100
NUM_ADVERTISERS = 5
NUM_ADS = 5
DIM = 10
ROUNDS = 1000

db.drop_all()
db.create_all()

uniform = distribution.Distribution('uniform')
normal = distribution.Distribution('normal')

## create axis-aligned advertisers
afs = util.normalize(np.array([1,1,0,0,1,0,0,0,0,0]))

## shift the above patern around
advertisers = [my_sim.Advertiser(features=np.array([float(afs[(i+2*j) % DIM]) for i in range(DIM)])) for j in range(NUM_ADVERTISERS)]

for a in advertisers:
# print a.features, type(a.features)
    honest = player.Signal(player=a,features=a.features)
    p1 = player.Signal(player=a,features=util.normalize(a.features + normal.draw_unit_vector(DIM)))
    db.session.add_all([honest, p1])

db.session.add_all(advertisers)

consumers = [my_sim.Consumer(features=distribution.Distribution('normal',\
                                                                loc=normal.sample()).draw_unit_vector(DIM)) for i in range(NUM_CONSUMERS)]
db.session.add_all(consumers)

db.session.commit()

s = my_sim.Adx(ROUNDS, consumers, advertisers);

s.run()