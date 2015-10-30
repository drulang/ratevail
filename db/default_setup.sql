
/* Setup default values for reference tables */

# External Rating
insert ignore into ratevail.externalratingtyp(externalratingtypcd, name) values ('GOOGL','Google Places API');
insert ignore into ratevail.externalratingtyp(externalratingtypcd, name) values ('YELP','Yelp API');


# Phone Typev
insert ignore into ratevail.phonetyp(phonetypcd, name) values ('pri', 'Primary Phone');
insert ignore into ratevail.phonetyp(phonetypcd, name) values ('sec', 'Secondary Phone');

# Comment Status Type
insert ignore into ratevail.commentstatustyp(commentstatustypcd, name) values ('vld','Valid Comment');
insert ignore into ratevail.commentstatustyp(commentstatustypcd, name) values ('del','Delete Comment');
insert ignore into ratevail.commentstatustyp(commentstatustypcd, name) values ('flg','Flagged Comment');

# Rating Value
insert ignore into ratevail.ratingvalue(ratingval) values (1);
insert ignore into ratevail.ratingvalue(ratingval) values (2);
insert ignore into ratevail.ratingvalue(ratingval) values (3);
insert ignore into ratevail.ratingvalue(ratingval) values (4);
insert ignore into ratevail.ratingvalue(ratingval) values (5);

# Pricepoing
insert ignore into ratevail.pricepoint(pricepointval, name) values (1, '$1-$20');
insert ignore into ratevail.pricepoint(pricepointval, name) values (2, '$20-$30');
insert ignore into ratevail.pricepoint(pricepointval, name) values (3, '$30-$40');
insert ignore into ratevail.pricepoint(pricepointval, name) values (4, '$40-$50');
insert ignore into ratevail.pricepoint(pricepointval, name) values (5, '$60+');

# Feedback Status Type
insert ignore into ratevail.feedbackstatustyp(feedbackstatustypcd, name) values ('new', 'New Feedback Message');
insert ignore into ratevail.feedbackstatustyp(feedbackstatustypcd, name) values ('ack', 'Feedback Message Acknowledged');
insert ignore into ratevail.feedbackstatustyp(feedbackstatustypcd, name) values ('del', 'Feedback Message Deleted');

# Feedback Type
insert ignore into ratevail.feedbacktyp(feedbacktypcd, name) values ('gen', 'General');
insert ignore into ratevail.feedbacktyp(feedbacktypcd, name) values ('adv', 'Advertisement');
insert ignore into ratevail.feedbacktyp(feedbacktypcd, name) values ('bug', 'Bug');
insert ignore into ratevail.feedbacktyp(feedbacktypcd, name) values ('qstn','Question');

# Lift Type
insert ignore into ratevail.lifttyp(lifttypcd, name) values ('gndla', 'Gondola');
insert ignore into ratevail.lifttyp(lifttypcd, name) values ('oplft', 'Open Lift');

# Lift Status Type
insert ignore into ratevail.liftstatustyp(liftstatustypcd, name) values ('opn','Open');
insert ignore into ratevail.liftstatustyp(liftstatustypcd, name) values ('cls','Closed');

# Run Type
insert ignore into ratevail.runtyp(runtypcd, name) values ('grn','Green');
insert ignore into ratevail.runtyp(runtypcd, name) values ('blu','Blue');
insert ignore into ratevail.runtyp(runtypcd, name) values ('blk','Black Diamond');
insert ignore into ratevail.runtyp(runtypcd, name) values ('dblk','Double Black Diamond');

# Address Type
insert ignore into ratevail.addrtyp(addrtypcd, name) values ('PHYS', 'Physical Address');
insert ignore into ratevail.addrtyp(addrtypcd, name) values ('EML', 'Email Address');

# Image Type
insert ignore into ratevail.imagetyp(imagetypcd, name) values ('vntyp', 'Website Venue Type Image');
insert ignore into ratevail.imagetyp(imagetypcd, name) values ('venue', 'Website Venue Image');
insert ignore into ratevail.imagetyp(imagetypcd, name) values ('glyph', 'Glyphicon');

# Venue Type
#   - Setup image for venue typ
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (1, 'vntyp', 'Image Coming Soon', 'nophoto.jpg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (2, 'vntyp', 'Bar Venues', 'venue_bar.jpeg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (3, 'vntyp', 'Condo Venues', 'venue_condo.jpeg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (4, 'vntyp', 'Entertainment Venues', 'venue_entertainment.jpeg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (5, 'vntyp', 'Hotel Venues', 'venue_hotel.jpg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (6, 'vntyp', 'Restaurant Venues', 'venue_restaurant.jpeg');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (7, 'vntyp', 'Shopping Venues', 'venue_shopping.jpeg');
#Glyphicons
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (8, 'glyph', 'Glyphicon House', 'glyphicon-home');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (9, 'glyph', 'Glyphicon Cutlery', 'glyphicon-cutlery');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (10, 'glyph', 'Glyphicon Headphones', 'glyphicon-headphones');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (11, 'glyph', 'Glyphicon Shopping Cart', 'glyphicon-shopping-cart');
insert ignore into ratevail.image(imageid, imagetypcd, title, location) values (12, 'glyph', 'Glyphicon Martining Glass', 'glyphicon-glass');
#   - Setup venue types
#Top Level
insert ignore into ratevail.venuetyp(venuetypcd, imageid, iconimageid, name, displayname) values ('acmdn', 5, 8, 'accomodations', 'Accomodations');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('hotel', 'acmdn', 4, 'hotel', 'Hotel');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('condo', 'acmdn', 2, 'condo', 'Condo');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('reltr', 'acmdn', 2, 'realtor', 'Realtor');

#Top Level
insert ignore into ratevail.venuetyp(venuetypcd, imageid, iconimageid, name, displayname) values ('ntlfe', 2, 12, 'nightlife', 'Night Life');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('bar', 'ntlfe', 1, 'bar', 'Bar');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('club', 'ntlfe', 1, 'club',  'Club');

#Top Level
insert ignore into ratevail.venuetyp(venuetypcd, imageid, iconimageid, name, displayname) values ('dning', 6, 9, 'dining', 'Dining');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('rstnt', 'dning', 1, 'restaurant',  'Restaurant');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('amrc', 'dning', 1, 'american',  'American');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('orntl', 'dning', 1, 'oriental',  'Oriental');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('itnl', 'dning', 1, 'italian',  'Italian');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('erpn', 'dning', 1, 'erpn',  'Europen');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('bfest', 'dning', 1, 'breakfast',  'Breakfast');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('cafe', 'dning', 1, 'cafe',  'Cafe');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('pzza', 'dning', 1, 'pizza',  'Pizza');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('dssrt', 'dning', 1, 'dessertery',  'Dessertery');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('mexcn', 'dning', 1, 'mexican',  'Mexican');

# Top Level 
insert ignore into ratevail.venuetyp(venuetypcd, imageid, iconimageid, name, displayname) values ('store', 7, 11, 'store', 'Stores');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('sport', 'store', 6, 'sports', 'Sports Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('spa', 'store', 6, 'spas', 'Spas');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('gnrl', 'store', 6, 'general', 'General Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('mve', 'store', 6, 'movie', 'Movie Theater');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('hlth', 'store', 6, 'health', 'Health Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('clth', 'store', 6, 'clothing', 'Clothing Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('hmgds', 'store', 6, 'homegoods', 'Home Goods Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('grcry', 'store', 6, 'grocery', 'Grocery/Supermarket Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('jwlry', 'store', 6, 'jewelry', 'Jewelry Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('food', 'store', 6, 'food', 'Food Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('hdwr', 'store', 6, 'hdwr', 'Hardware Store');
  insert ignore into ratevail.venuetyp(venuetypcd, parentvenuetypcd, imageid, name, displayname) values ('svnr', 'store', 6, 'souvenir', 'Souvenir Store');

# Create Vail
insert ignore into ratevail.resort(resortid, name, slogan) values (1, "Vail", "Like nothing on earh.");


# Create Venus

# Default image for a bar if they don't have a logo
# Garfinkels
insert ignore into ratevail.phone(phoneid, phonetypcd, areacode, exchange, subscriberno, createdate) values (1, 'pri', '336', '123', '2342', NOW());
insert ignore into ratevail.venue(venueid, resortid, logoimageid, name, shortname, slogan, phoneid, hours, pricepointval, description) 
  values (1, 1, 1, 'Garfinkels', 'garfsvail', 'A fantastic time had by all', 1, '8:00 AM- 10:00AM', 3, 'Welcome to Garfinkel\'s restaurant and bar, located in the Lionshead section of Vail, CO. Enjoy great apre ski entertainment on our large sunny deck, wonderful dining and drink specials and nothing short of a fantastic time had by all at Vail, Colorado\'s favorite local bar.');
#Type
insert ignore into ratevail.venue_has_venuetyp(venueid, venuetypcd) values (1, 'bar');
insert ignore into ratevail.venue_has_venuetyp(venueid, venuetypcd) values (1, 'rstnt');
#Address
insert ignore into ratevail.addr(addrid, addrtypcd, addrline1, addrline2, city, state, zip)
  values (1, 'PHYS', '123 Pandas','On Coke line 2', 'Vail', 'CO', '12345');
insert ignore into ratevail.venue_has_addr(venueid, addrid) values (1, 1);

# Shakedown Bar
insert ignore into ratevail.phone(phoneid, phonetypcd, areacode, exchange, subscriberno, createdate) values (2, 'pri', '336', '123', '2342', NOW());
insert ignore into ratevail.venue(venueid, resortid, logoimageid, name, shortname, slogan, phoneid, hours, pricepointval, description)
  values (2, 1, 1, 'Shakedown', 'shakedownbar', 'Vail\'s Best Live Music Joint!', 2, '1:00AM - 10:00AM', 2, 'Located at the top of Bridge St., in the heart of Vail Village just east of the fountain, Shakedown Bar is a hot spot for Vail nightlife and apres ski. This 190 person capacity live music venue and bar is dedicated to delivering a musical experience that you wont soon forget!');
#Type
insert ignore into ratevail.venue_has_venuetyp(venueid, venuetypcd) values (2, 'bar');
#Address
insert ignore into ratevail.addr(addrid, addrtypcd, addrline1, addrline2, city, state, zip)
  values (2, 'PHYS', '123 Pandas','On Coke line 2', 'Vail', 'CO', '12345');
insert ignore into ratevail.venue_has_addr(venueid, addrid) values (2, 2);

# Ski SHop
insert ignore into ratevail.phone(phoneid, phonetypcd, areacode, exchange, subscriberno, createdate) values (3, 'pri', '336', '123', '2342', NOW());
insert ignore into ratevail.venue(venueid, resortid, logoimageid, name, shortname, slogan, phoneid, hours, pricepointval, description)
  values (3, 1, 1, 'SkiShop', 'skishop', 'Come get your skis!', 3, '1:00AM - 10:00AM', 2, 'Come get your skis, snowboards and apparelt and this awesome sauce shop!');
#Type
insert ignore into ratevail.venue_has_venuetyp(venueid, venuetypcd) values (3, 'sport');
insert ignore into ratevail.venue_has_venuetyp(venueid, venuetypcd) values (3, 'clth');
#Address
insert ignore into ratevail.addr(addrid, addrtypcd, addrline1, city, state, zip)
  values (3, 'PHYS', '123 Pandas', 'Vail', 'CO', '12345');
insert ignore into ratevail.venue_has_addr(venueid, addrid) values (3, 3);

