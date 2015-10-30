"""
Loads external ratings for Google and Yelp
"""
import sys
import logging

sys.path.insert(0, '../lib')
from extapi import GooglePlacesAPI
from rvdb import RateVailDb


class GoogleExtRatingsJob(object):

    def __init__(self):
        self._log = logging.getLogger('ldext.google')
        #TODO: Load from config
        self._ext_rating_typcd = "GOOGL"
        self._apikey = "yourapikey"
        self._rvdb = RateVailDb()
        self._gapi = GooglePlacesAPI(self._apikey)

    def purge_comments(self):
        self._log.info("Purging comments")
        cnt = self._rvdb.delete_external_rating_comments_by_type(self._ext_rating_typcd)
        self._log.debug("Purged %s records" % cnt)

    def load_comments(self):
        self._log.info("Loading comments")

        self._log.info("Retrieving external source ids from rvdb")
        ext_src_ids = self._rvdb.get_external_ratings_by_type(self._ext_rating_typcd)
        self._log.info("Retrieved %s external source idse" % len(ext_src_ids))

        for ext_rec in ext_src_ids:
            place_dtl = self._gapi.fetch_place_detail(ext_rec['externalsourceid'])
            if place_dtl['status'] == 'OK':
                #TODO: Need to update externalrating
                if 'reviews' in place_dtl['result']:
                    reviews = place_dtl['result']['reviews']
                    for review in reviews:
                        rating = review['rating']
                        comment = review['text']
                        username = review['author_name']
                        self._log.info("Inserting externalratingid: %s, rating: %s, author_name: %s" %
                                       (ext_rec['externalratingid'], rating, username))
                        if self._rvdb.insert_external_rating_comment(ext_rec['externalratingid'], rating,
                                                                     comment, username) == 1:
                            self._log.info("  -Insert complete")
                        else:
                            self._log.critical("  -Insert failed for externalratingid: %s" %
                                               ext_rec['externalratingid'])
                else:
                    self._log.info("No reviews found for extratingid: %s" % ext_rec['externalratingid'])
            else:
                self._log.critical("Invalid request received")
        return 0

if __name__ == "__main__":
    print "Initiating job"
    j = GoogleExtRatingsJob()
    print "  Initiated."
    print "Starting job"
    print "  running..."
    rc = j.load_comments()
    print "job complete"
    sys.exit(rc)
