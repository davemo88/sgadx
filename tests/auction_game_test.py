import sys

from sgad import player, game

num_advertisers = 100

num_games = 100

p = player.user()

advertisers = [player.advertiser() for i in range(num_advertisers)]

overall_user_payoff = 0

overall_advertiser_payoffs = [0] * num_advertisers

for game in range(num_games):

    winner, auction_payoffs = signaling_games.auction_game(p, advertisers)

    impression_payoffs = signaling_games.impression_game(advertisers[winner], p)
    
    auction_payoffs[winner] += impression_payoffs[0]

    overall_user_payoff += impression_payoffs[-1]

    overall_advertiser_payoffs = [i+j for i,j in zip(overall_advertiser_payoffs, auction_payoffs)]

##    print "game ", game, " auction winner ", winner, " purchase? ",impression_payoffs[-1]

print "user payoff: ", overall_user_payoff

## print "advertiser payoffs: ", overall_advertiser_payoffs

print "most successful advertiser ", overall_advertiser_payoffs.index(max(overall_advertiser_payoffs)), max(overall_advertiser_payoffs)
