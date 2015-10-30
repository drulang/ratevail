import sys
import logging

sys.path.insert(0, '../lib')
from extapi import GooglePlacesAPI
from rvdb import RateVailDb
from rvutil import super_sanitize_str, escape_str


class SearchAndLoadGoogleVenues(object):


    def __init__(self, query, google_venue_types):
        self.google_venue_types = google_venue_types
        self._query = query
        self._apikey = "YourKey"
        self._gapi = GooglePlacesAPI(self._apikey)
        self._db = RateVailDb()

    def run(self):
        print "Searching query: " + str(self._query)

        search_page = self._gapi.search_places(self._query)
        while search_page:
            if search_page['status'] != "OK":
                raise Exception("Search Page response returned status: %s" % search_page['status'])

            self._proc_results(search_page['results'])

            next_token = search_page.get("next_page_token")
            if next_token:
                print "Processing next search page"
                search_page = self._gapi.search_places(self._query, pagetoken=next_token)
            else:
                print "Finished processing all pages"
                break


    def _proc_results(self, results):
        print "Processing Result"
        for result in results:
            detail_page = self._gapi.fetch_place_detail(result['reference'])
            if detail_page['status'] != "OK":
                raise Exception("Detail Page returned bad status")

            #Venue Properties
            venue_name = escape_str(result['name'])
            venue_shortname = super_sanitize_str(result['name'])
            venue_shortname = venue_shortname.replace(" ", "").lower()
            venue_address = result['formatted_address']
            venue_phone = detail_page['result'].get('formatted_phone_number')
            g_venue_types = result['types']
            venue_externalsourceid = result['reference']
            externalrating_uniqid = result['id']
            venue_description = "Description for this venue is coming soon"
            #Rating Val
            if "rating" in result.keys():
                venue_rating = result['rating']
            else:
                venue_rating = 0
            #Price point
            if "price_level" in result.keys():
                venue_pricepoint = result['price_level']
            else:
                venue_pricepoint = 0
            #Convert google venue types to rv venue types
            rv_venue_types = []
            for typ in g_venue_types:
                if typ in self.google_venue_types:
                    rv_venue_types.append(self.google_venue_types[typ])

            rv_venue_types = set(rv_venue_types) #remove duplicates
            if len(rv_venue_types) == 0:
                print "WARNING: This venue doesn't ahve any matching venue types and will be skipped"
                print "WARNING: Skipping venue: " + str(venue_name)
                continue

            #
            # Check if externalsourceid already exists. If it does then just assign types. Have to insert ignore though
            #
            ext_src_rec = self._db.externalrating_uniqid_exists(externalrating_uniqid)
            if len(ext_src_rec) == 1:
                print "External Sourceid exists"
                print "Assigning types"
                for typ in rv_venue_types:
                    self._db.assign_ignore_venue_venuetyp(ext_src_rec[0]['venueid'], typ)
                print "Continuing to next record"
                continue
            elif len(ext_src_rec) > 1:
                raise Exception("Externa Source ID is linked to more than one venue. %s" % str(ext_src_rec))
            else:
                print "External Source id does NOT exist. Creating venue"
                

            #Create Phone Number
            if venue_phone:
                phone_parts = venue_phone.split(" ")
                area_code = phone_parts[0][1:4]
                phone_parts = phone_parts[1].split("-")
                exchange = phone_parts[0]
                subscriberno = phone_parts[1]
                self._db.insert_phone("pri", area_code, exchange, subscriberno, commit=False)
                phoneid = self._db._last_insert_id()
            else:
                phoneid = None
            #Create Address
            # TODO: Find zip properly
            zipcd = "81657"

            addr_parts = venue_address.split(",")
            if len(addr_parts) == 3:
                self._db.insert_addr("PHYS", "", addrline2=None, city=addr_parts[0],
                                     state=addr_parts[1], zipcd=zipcd, commit=False)
            if len(addr_parts) == 4:
                self._db.insert_addr("PHYS", addr_parts[0], addrline2=None, city=addr_parts[1],
                                     state=addr_parts[2], zipcd=zipcd, commit=False)
            elif len(addr_parts) == 5:
                self._db.insert_addr("PHYS", addr_parts[0], addrline2=addr_parts[1], city=addr_parts[2],
                                     state=addr_parts[3], zipcd=zipcd, commit=False)
            addrid = self._db._last_insert_id()

            #Create venue
            resortid = 1
            venueid = self._db.create_venue(resortid, venue_name, venue_shortname, venue_description,
                                            rv_venue_types, pricepointval=venue_pricepoint, phoneid=phoneid,
                                            addrids=[addrid], logoimageid=1)

            #Create External Rating
            self._db.insert_external_rating("GOOGL", venue_externalsourceid, venue_name,
                                            pricepointval=venue_pricepoint,
                                            ratingval=venue_rating,
                                            uniqid=externalrating_uniqid,
                                            commit=False)

            externalratingid = self._db._last_insert_id()
            self._db.assign_venue_external_rating(externalratingid, venueid, commit=True)


if __name__ == "__main__":
    rest_typ = {
        #Restaurants
        "restaurant" : "rstnt",
        "food" : "rstnt",
        "bar" : "bar",
    }
    shopping_typ = {
        "clothing_store" : "clth",
        "home_goods_store" : "hmgds",
        "grocery_or_supermarket" : "grcry",
        "department_store" : "clth",  #TODO: Check this one
        "jewelry_store" : "jwlry",
        "food" : "food",
        "health" : "hlth",
        "store" : "store",
        "hardware_store" : "hdwr",
        "shoe_store" : "clth",
    }

    condo_typ = {
        "real_estate_agency" : "condo",
        "lodging" : "condo",
        "establishment" : "condo",
    }

    hotel_typ = {
        "lodging" : "hotel",
        "establishment" : "hotel",
    }

    spa_typ = {
        "spa" : "spa",
    }

    gym_typ = {
    "establishment" : "gym",
    "gym" : "gym"
    }

    #job = SearchAndLoadGoogleVenues("shopping+in+Vail", shopping_typ)
    #job = SearchAndLoadGoogleVenues("restaurants+in+Vail", rest_typ)
    #job = SearchAndLoadGoogleVenues("condos+in+Vail", condo_typ)
    #job = SearchAndLoadGoogleVenues("hotels+in+Vail", hotel_typ)
    #job = SearchAndLoadGoogleVenues("spa+in+Vail", spa_typ)
    job = SearchAndLoadGoogleVenues("gym+in+Vail", gym_typ)
    

    job.run()
