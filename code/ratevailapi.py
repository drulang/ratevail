import json

from flask import request
from flask.views import MethodView
from flask import session

import lib.rvdb
from lib.rvlog import apilog

db = lib.rvdb.RateVailDb()

class VenueAPI(MethodView):

    def get(self, venueid):
        if 'loggedin' not in session:
            return json.dumps({"status":"ERR","errmsg":"Must be logged in to access"})

        if venueid:
            venue_profile = db.get_venue_profile(venueid=venueid)
            return json.dumps(venue_profile)
        else:
            return json.dumps(db.get_venues())

    def put(self, venueid):
        if 'loggedin' not in session:
            return json.dumps({"status":"ERR","errmsg":"Must be logged in to access"})

        description = unicode(request.form.get("description",None))
        imgname = request.form.get("imgname",None)
        imgtitle = request.form.get("imgtitle",None) 
        venuetypes = request.form.get("venuetypes",None)
        hours = unicode(request.form.get("hours",None))

        #xor imgloc/imgtitle
        if bool(imgname) != bool(imgtitle):
            return json.dumps({"status":"ERR",
                               "errmsg":"If imgname/imgtitle must be either passed together or not at all"})
        elif imgname:
            img = (imgtitle, "venues/" + imgname)
        else:
            img = None

        if venuetypes:
            venuetypes = venuetypes.split(",")

        try:
            db.update_venue(venueid,
                            description=description.replace("'","\\'"),
                            img=img,
                            venue_types=venuetypes,
                            hours=hours)
        except Exception as e:
            return json.dumps({"status":"ERR","errmsg":str(e)})

        return json.dumps({"status":"OK"})

class VenueTypeAPI(MethodView):

    def get(self):
        if 'loggedin' not in session:
            return json.dumps({"status":"ERR","errmsg":"Must be logged in to access"})

        return json.dumps(db.venue_types)

