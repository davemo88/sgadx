"""Random Utilities

Function from this class are generic enough that I don't know where else to put them

"""

import random

from sgadx import db, player, sim
from sgadx import sg

def flip(bias=0.5):
    """

    """

    return random.random() < bias    

def get_signal_history(player_id):
    """

    """

    player.Signal.query().join(sg.GameRecord,
                       sg.GameRecord.game_record_id ==\
                       Signal.game_record_id).join(sim.RoundRecord,
                       sim.RoundRecord.game_record_id ==\
                       sg.GameRecord.game_record_id).filter(sg.GameRecord.sender_id==player_id).order_by(sim.RoundRecord.round.asc)

def get_action_history(player_id):

    player.Action.query().join(sg.GameRecord,
                       sg.GameRecord.game_record_id ==\
                       Action.game_record_id).join(sim.RoundRecord,
                       sim.RoundRecord.game_record_id ==\
                       sg.GameRecord.game_record_id).filter(sg.GameRecord.sender_id==player_id).order_by(sim.RoundRecord.round.asc)

