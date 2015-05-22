from app import db, feature, player, distribution, game, sim


NUM_CONSUMERS = 100
NUM_ADVERTISERS = 5
NUM_FEATURES = 10
NUM_ADS = 5
CLICK_THRESHOLD = .9
CONVERSION_THRESHOLD = .99
NUM_ITERATIONS = 100

distribution.Distribution.query.delete()
d = distribution.Distribution('uniform')
db.session.add(d)

consumers = [player.Consumer(d, NUM_FEATURES, CLICK_THRESHOLD, CONVERSION_THRESHOLD) for i in range(NUM_CONSUMERS)]
advertisers = [player.Advertiser(d, NUM_FEATURES, NUM_ADS) for i in range(NUM_ADVERTISERS)]

db.session.add_all(consumers)
db.session.add_all(advertisers)

db.session.commit()

s = sim.AdExchange(consumers, advertisers);

s.run(NUM_ITERATIONS)