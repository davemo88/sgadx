"""

"""

from app import db, feature

from numpy import array

import sqlalchemy

class Ad(db.Model):
    __table_name__ = 'ad'

    id = db.Column(db.Integer, primary_key = True)
    advertiser = db.relationship('Advertiser')
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertiser.id'))
    _ad_features = db.relationship('AdFeature', order_by=sqlalchemy.asc('position'))

    def __init__(self, advertiser):

        super(Ad, self).__init__()

        self.advertiser = advertiser

        self.ad_features = self.advertiser.get_perturbed_features()

        self._ad_features = [feature.AdFeature(ad_id=self.id, position=i, value=self.ad_features[i]) for i in range(len(self.ad_features))]

    @sqlalchemy.orm.reconstructor
    def init_on_load(self):

        self.ad_features = array([af.value for af in self._ad_features])