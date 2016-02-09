"""

"""

from itertools import chain
from random import choice

import numpy as np

from sgadx import db, player, distribution, my_sim

NUM_CONSUMERS = 10
NUM_ADVERTISERS = 5
# NUM_ADS = 5
DIM = 10
ROUNDS = 1000

db.drop_all()
db.create_all()

uniform = distribution.Distribution('uniform')
normal = distribution.Distribution('normal')

def unit_vector_average(*unit_vectors):

    return sum(unit_vectors)/np.linalg.norm(sum(unit_vectors))

# def test_honest_sim():

# ## create axis-aligned advertisers
#     afs = unit_vector_average(np.array([1,1,0,0,1,0,0,0,0,0]))

# ## shift the above patern around
#     advertisers = [my_sim.Advertiser(features=np.array([float(afs[(i+2*j) % DIM]) for i in range(DIM)])) for j in range(NUM_ADVERTISERS)]

#     for a in advertisers:
# ## give each advertiser a perturbed version of their features as a signal
#         p1 = player.Signal(player=a,features=unit_vector_average(a.features + normal.draw_unit_vector(DIM)),desc='Perturbed')
#         db.session.add(p1)

#     # db.session.add_all(advertisers)

#     consumers = [my_sim.Consumer(features=distribution.Distribution('normal',\
#                                                                     loc=normal.sample()).draw_unit_vector(DIM)) for i in range(NUM_CONSUMERS)]

#     # db.session.add_all(consumers)

#     # db.session.commit()

#     s = my_sim.Adx(ROUNDS, consumers, advertisers);

#     records = s.run()

#     db.session.add_all(records.keys())
#     db.session.add_all(chain.from_iterable([records[k] for k in records]))
#     db.session.add(s)
#     db.session.commit()

def test_dishonest_sim():

## create axis-aligned advertisers
    afs = unit_vector_average(np.array([1,1,0,0,1,0,0,0,0,0]))

## promoters instead of advertisers
    advertisers = [my_sim.Promoter(features=np.array([float(afs[(i+2*j) % DIM]) for i in range(DIM)])) for j in range(NUM_ADVERTISERS)]

    for a in advertisers:
## give each advertiser a perturbed version of their features as a signal
        p1 = player.Signal(player=a,features=-a.features,desc='Opposite')
        db.session.add(p1)

    # db.session.add_all(advertisers)

    consumers = [my_sim.Consumer(features=distribution.Distribution('normal',\
                                                                    loc=normal.sample()).draw_unit_vector(DIM)) for i in range(NUM_CONSUMERS)]

    # db.session.add_all(consumers)

    # db.session.commit()

    s = my_sim.Adx(ROUNDS, consumers, advertisers);

    records = s.run()

    db.session.add_all(records.keys())
    db.session.add_all(chain.from_iterable([records[k] for k in records]))
    db.session.add(s)
    db.session.commit()