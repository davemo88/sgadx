"""

"""

from app import db

from numpy import array

import sqlalchemy

class Ad(db.Model):
    __table_name__ = 'ad'

    id = db.Column(db.Integer, primary_key = True)
    advertiser = db.relationship('Advertiser')
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    _ad_features = db.relationship('AdFeature')

    def __init__(self, advertiser):

        self.advertiser = advertiser

        self.ad_features = self.advertiser.get_perturbed_features()

        super(Ad, self).__init__()

        self._ad_features = [AdFeature(ad_id=self.id, value=val) for val in self.ad_features]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.ad_features = array([af.value for af in self._ad_features])

class AdFeature(db.Model):
    __table_name__ = 'ad_feature'

    id = db.Column(db.Integer, primary_key = True)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'))
    value = db.Column(db.DECIMAL(10,9))