"""

"""

from app import db

class Feature(db.Model):
    __table_name__ = 'feature'

    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    value = db.Column(db.DECIMAL(10,9))