import sys
import json
from Queue import Queue

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import redirect

from lib.rvlog import applog
import lib.rvdb as rvdb
import lib.rvconf as rvconf
from lib.rvutil import sanitize_str, super_sanitize_str, escape_str
from ratevailapi import VenueAPI, VenueTypeAPI
from lib.rvtweet import RvAutoTweet

applog.info("Starting RateVail Web Application");
appconf = rvconf.RvConf()
db =  rvdb.RateVailDb()

#Setup Application
app = Flask(__name__)
app.secret_key = 'R0ZF98jzzzz/5yX R~XHH!jmN]LWX/,?RT' 

#Setup API
venue_view = VenueAPI.as_view('venue_api')
app.add_url_rule('/v1/venue',defaults={"venueid":None},
                 view_func=venue_view, methods=['GET'])
app.add_url_rule('/v1/venue/<int:venueid>',
                 view_func=venue_view, methods=['GET','PUT'])
venuetyp_view = VenueTypeAPI.as_view('venuetyp_api')
app.add_url_rule('/v1/venuetyp',
                 view_func=venuetyp_view,
                 methods=['GET'])

#Setup AutoTweet
tweetQueue = Queue()
rvTweet = RvAutoTweet(tweetQueue)
if appconf.autotweet:
    applog.info("Starting RateVail AutoTweet")
    rvTweet.start()     
else:
    applog.debug("Not starting RateVail AutoTweet. Config disabled")


def gen_main_menu():
    #Move this to different module
    top_level_items = db.top_level_venue_types

    for item in top_level_items:
        item['subitems'] = []

        for venue_typ in db.venue_types:
            if venue_typ['parentvenuetypcd'] == item['venuetypcd']:
                item['subitems'].append(venue_typ)
    return top_level_items

main_menu = gen_main_menu()

@app.context_processor
def inject_main_menu():
    return dict(main_menu=main_menu)

@app.route('/')
def index():
    rand_comments=db.get_random_comments(6)
    for comment in rand_comments:
        #Calculate full/empty stars
        comment['num_full_stars'] = range(comment['ratingval'])
        comment['num_empty_stars'] = range(5-comment['ratingval'])
        if len(comment['text']) > 250:
            comment['text'] = comment['text'][0:247] + "... "
            comment['readMoreLink'] = "/venue/" + comment['venueshortname']

    return render_template("index.html", rand_comments=rand_comments)

@app.route('/venues')
@app.route('/venues/<venue_type_name>')
def venues(venue_type_name=None):
    venue_type_name=super_sanitize_str(venue_type_name)
    def group_by(grp, grp_nbr=4):
        #Build groups of 4 for template
        group = []
        curr_grp = []

        for venue in grp:
            if len(curr_grp) != grp_nbr:
                curr_grp.append(venue)
            else:
                group.append(curr_grp)
                curr_grp = [venue]

        if len(curr_grp) > 0:
            group.append(curr_grp)
        
        return group

    #Verify valid venue type, if not return empty. If valid then vall get_venues
    for venue_type in db.venue_types:
        if venue_type['name'].lower() == unicode(venue_type_name).lower():
            active_venue_type=venue_type
            venues = db.get_venues(venuetypcd=venue_type['venuetypcd'])

            for venue in venues:
                #Calculate full/empty stars
                if venue['avguserrating']:
                    num_full_stars = int(round(venue['avguserrating']))
                    num_empty_stars = 5 - num_full_stars
                else:
                    num_full_stars = 0
                    num_empty_stars = 5

                venue['full_stars'] = range(num_full_stars)
                venue['empty_stars'] = range(num_empty_stars)
                if venue['pricepointval']:
                    venue['pricepoint'] = range(venue['pricepointval'])
                else:
                    venue['pricepoint'] = []

            #Calculate sub items
            venue_sub_items = None
            for item in main_menu:
                if item['venuetypcd'] == venue_type['parentvenuetypcd'] or (venue_type['venuetypcd'] in db.top_level_venue_typcd):
                    venue_sub_items = item['subitems']

            return render_template("venues.html",
                                   active_venue_type=active_venue_type,
                                   venue_sub_items=venue_sub_items,
                                   venues=venues)
    return render_template("venues.html",
                            grouped_venue_types=group_by(db.top_level_venue_types))

@app.route('/venue/<venue_shortname>', methods=['GET','POST'])  #TODO: Need to change this to /venue/<resort>/<venue_shortname>
def venue(venue_shortname=None):
    venue_shortname = super_sanitize_str(venue_shortname)
    applog.debug("Venue short name: %s" % venue_shortname)
    venue_profile = db.get_venue_profile(venue_shortname=venue_shortname) 
    if not venue_profile:
        return render_template("error.html",
                               errmsg="Unable to find that venue.")

    if venue_profile['pricepointval']:
        venue_profile['pricepoint'] = range(venue_profile['pricepointval'])
    else:
        venue_profile['pricepoint'] = []

    #TODO: Seems like there is a better way to draw stars
    if venue_profile['avguserrating']:
        num_full_stars = int(round(venue_profile['avguserrating']))
        num_empty_stars = 5 - num_full_stars
    else:
        num_full_stars = 0
        num_empty_stars = 5

    venue_profile['full_stars'] = range(num_full_stars)
    venue_profile['empty_stars'] = range(num_empty_stars)

    #Venue Comments
    user_likes = request.cookies.get("likes", "{}")
    user_likes = json.loads(user_likes)

    venue_comments = db.get_top_user_comments_for_venue(venue_profile['venueid'])
    for comment in venue_comments:
        num_full_stars = comment['ratingval']
        num_empty_stars = 5 - num_full_stars
        comment['full_stars'] = range(num_full_stars)
        comment['empty_stars'] = range(num_empty_stars)
        comment['createdate'] = comment['createdate'].strftime("%m/%d/%Y")
        if comment['userfname'] == None:
            comment['userfname'] = "Anonymous"

        cid = unicode(comment['commentid'])
        if cid in user_likes:
            if user_likes[cid] == "U":
                comment['userliked'] = True
            else:
                comment['userdisliked'] = True

    #Venue External Ratings
    google_venue_profile = None
    google_venue_comments = None

    try:
        google_venue_profile = db.get_external_rating_for_venue(venue_profile['venueid'], 'GOOGL')
        num_full_stars = google_venue_profile['ratingval']
        num_empty_stars = 5 - num_full_stars
        google_venue_profile['full_stars'] = range(num_full_stars)
        google_venue_profile['empty_stars'] = range(num_empty_stars)
    except Exception as e:
        applog.critical("Unable to retrieve google venue profile for venueid: %s" % venue_profile['venueid'])
        applog.critical(str(e))
    
    if google_venue_profile:
        try: 
            google_venue_comments = db.get_external_rating_comments(google_venue_profile['externalratingid'])
            for comment in google_venue_comments:
                full_stars = comment['ratingval']
                empty_stars = 5 - full_stars
                comment['full_stars'] = range(full_stars)
                comment['empty_stars'] = range(empty_stars)
        except Exception as e:
            applog.critical("Unable to retireve google comments for external rating id: %s" %
                            str(google_venue_profile['externalratingid']))

    if request.cookies.get("user-rated-%s" % venue_profile['venueid']) == "true":
        return render_template("venue.html",
                               venue_profile=venue_profile,
                               venue_comments=venue_comments,
                               google_venue_profile=google_venue_profile,
                               google_venue_comments=google_venue_comments,
                               user_already_rated=True)
        
    return render_template("venue.html",
                           venue_profile=venue_profile,
                           venue_comments=venue_comments,
                           google_venue_profile=google_venue_profile,
                           google_venue_comments=google_venue_comments)

@app.route("/venue/<venue_shortname>/comment", methods=["POST"])
def create_venue_comment(venue_shortname):
    venue_shortname = super_sanitize_str(venue_shortname)

    result = None
    ratingval_errmsg = None

    #Sanitize and check fields
    request_commentFname = sanitize_str(request.form['commentFname'])
    request_commentText = sanitize_str(request.form['commentText'])
    userbrowser = sanitize_str(request.headers.get("User-Agent"))
    try:
        int(request.form['venueid']) #Cheap way to make sure venueid is an integer
        if int(request.form['ratingval']) == 0:  #TODO: Instead of checking just 0, need to check all rating types
            ratingval_errmsg = "Please select a star!"
            return json.dumps({"status":"ERR","errmsg":ratingval_errmsg})
    except Exception as e:
        applog.critical("SECURITY: Potential sql injection attemp. Unexpected type received when trying to insert rating value")
        applog.critical("SECURITY: Exception: %s" % str(e))
        ratingval_errmsg = "Whoa! We got a weird value. Admins have been notified."
        return json.dumps({"status":"ERR","errmsg":ratingval_errmsg})

    #Attempt insert
    if len(request.form['commentText'].strip()) > 0:
        result = db.insert_venue_user_rating_w_comment(request.form['venueid'],
                                                       request.form['ratingval'],
                                                       escape_str(request_commentText),
                                                       userfname=escape_str(request_commentFname),
                                                       userip = request.remote_addr,
                                                       userbrowser = userbrowser)
    else:
        result = db.insert_venue_user_rating(request.form['venueid'],
                                             request.form['ratingval'],
                                             userip = request.remote_addr,
                                             userbrowser = userbrowser)
                
    if result:
        if appconf.autotweet:
            tweet = {"f_name":request_commentFname, "ratingval": request.form['ratingval'], "text":request_commentText, "venue_shortname":venue_shortname}
            applog.debug("Queueing Tweet: %s" % tweet) 
            tweetQueue.put(tweet) 

        resp = make_response(json.dumps({"status":"OK"}))
        resp.set_cookie('user-rated-%s' % request.form['venueid'], "true")
        return resp 

    return json.dumps({"status":"ERR"})

@app.route("/venue/<venue_shortname>/comment/<commentid>", methods=["GET", "POST"])
def venue_comment(venue_shortname, commentid):
    """
    Used to increment/decrement a comments like/dislike count
    """
    venue_shortname = super_sanitize_str(venue_shortname)
    commentid = super_sanitize_str(commentid)
    try:
        like = int(request.args.get('like',0))
        if like not in (0, 1, -1):
            raise Exception("")
    except Exception as e:
        applog.critical("Received bad value for like. Value: %s" % request.args.get('like'))
        applog.criticla("Error message: %s" % e)
        return render_template("venue_comment.html",
                               successful="false",
                               errmsg="Received bad value for like")

    try:
        dislike = int(request.args.get('dislike',0))
        if dislike not in (0, 1, -1):
            raise Exception("")
    except Exception as e:
        applog.critical("Received bad value for dislike. Value: %s" % request.args.get('dislike'))
        applog.criticla("Error message: %s" % e)
        return render_template("venue_comment.html",
                               successful="false",
                               errmsg="Received bad value for dislike")
    if like == dislike or (like + dislike) < 0:
        applog.critical("Received bad value for dislike. Value: %s" % request.args.get('dislike'))
        return render_template("venue_comment.html",
                               successful="false",
                               errmsg="Received bad values or bad combo for like and/or dislike.")

    ##
    #This seems complicated, but its needed to adjust counts if
    #the user clicks either like,dislike and then switches choice
    ##
    applog.debug("Assigning like to comment id: %s" % commentid)
    errmsg = None
    if like == 1 and dislike == 0:
        #User pressed like count
        applog.debug("User clicked like for commentid %s" % commentid)
        if db.incr_comment_like_cnt(commentid) != 1:
            errmsg = "Unable to increment like count"
    elif like == 1 and dislike == -1:
        #User clicked like after clicking dislike
        applog.debug("User switched from dislike to like for comment id %s" % commentid)
        if db.incr_comment_like_cnt(commentid) != 1:
            errmsg = "Unable to increment like count." 
        else:
            if db.decr_comment_dislike_cnt(commentid) != 1:
                errmsg = "Unable to decrement dislike count"
    elif like == 0 and dislike == 1:
        #User clicked dislike button
        applog.debug("User disliked commentid %s" % commentid)
        if db.incr_comment_dislike_cnt(commentid) != 1:
            errmsg = "Unable to increment dislike count"
    elif like == -1 and dislike == 1:
        #User clicked dislike after clicking like
        applog.debug("User switched from like to dislike for sommen id %s" % commentid)
        if db.incr_comment_dislike_cnt(commentid) != 1:
            errmsg = "Unable to increment comment dislike count"
        else:
            if db.decr_comment_like_cnt(commentid) != 1:
                errmsg = "Unable to decrement comment like count"

    if errmsg:
        return render_template('venue_comment.html', successful="false", errmsg=errmsg) 
    else:

        applog.debug("Building success response")
        resp = make_response(render_template('venue_comment.html', successful="true", errmsg=""))

        like_list = request.cookies.get("likes")
        if like_list:
            like_list = json.loads(like_list)
        else:
            like_list = {}
        
        like_list[commentid] = "U" if like == 1 else "D"
        resp.set_cookie("likes",json.dumps(like_list))
        return resp

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        #Verify Feedbacktyp code
        feedbacktypcd = super_sanitize_str(request.form["feedbacktypcd"])
        feedbacktypcd_errmsg = "Invalid type passed. Admins have been notified."

        for typ in db.feedback_types:
            if typ['feedbacktypcd'] == feedbacktypcd:
                feedbacktypcd_errmsg = None

        if feedbacktypcd_errmsg:
            applog.critical("Possible SQL Injection attack. Invalid value: %s passed to contact form" %
                            feedbacktypcd)

        #Verify UserFeedbackText
        userFeedbackText = sanitize_str(request.form["userFeedbackText"])
        userFeedbackText_errmsg = None

        if userFeedbackText.strip() == "":
            userFeedbackText_errmsg = "You forgot to provide us with some feedback!"

        #Verify User email
        userEmail = sanitize_str(request.form["userEmail"])
        userEmail_errmsg = None

        #TODO: Validate email
        if userEmail.strip() != "":
            if "@" not in userEmail or "." not in userEmail:
                userEmail_errmsg = "Invalid email format"
            elif len(userEmail) > 200:
                #Shorten email so that when the field in the template is populated we're not
                #passing back and forth huge chunks of data which could be a possible DoS attack
                userEmail = userEmail[0:200]
                userEmail_errmsg = "Whoa! Way too long of an email. Max 200 chars."

        if feedbacktypcd_errmsg or userFeedbackText_errmsg or userEmail_errmsg:
            applog.debug("Error inserting feedback")
            return render_template('contact.html',
                                   feedback_types=db.feedback_types,
                                   userEmail=userEmail,
                                   userEmail_errmsg=userEmail_errmsg,
                                   userFeedbackText=userFeedbackText,
                                   userFeedbackText_errmsg=userFeedbackText_errmsg,
                                   feedbacktypcd=feedbacktypcd,
                                   feedbacktypcd_errmsg=feedbacktypcd_errmsg)
        else:
            applog.debug("Inserting Feedback")
            result = db.insert_feedback(feedbacktypcd, userFeedbackText[0:1999], userEmail) 
            if result != 0:
                applog.debug("Feedback inserted successfully")
                return render_template('contact.html',
                                       feedback_types=db.feedback_types,
                                       insert_success=True)
            else:
                applog.critical("Unable to insert feedback. db.insert_feedback call returned 0")
                return render_template('contact.html',
                                       feedback_types=db.feedback_types,
                                       userEmail=userEmail,
                                       userFeedbackText=userFeedbackText,
                                       feedbacktypcd=feedbacktypcd,
                                       insert_failure=True)

    return render_template('contact.html', feedback_types=db.feedback_types)

@app.route('/advertise')
def advertise():
    return render_template('advertise.html')

@app.route('/vail')
def vail():
    return render_template('vail.html')

@app.route('/search', methods=["GET"])
def search():
    query = super_sanitize_str(request.args.get("q",''))
    applog.debug("Searching for query: " + str(query))
    results = db.search_venues(query)
    applog.debug("results: " + str(results))
    return render_template('search.html',results=results)

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/robots.txt')
def robots():
    return render_template("robots.txt")


###
# Admin, This needs to be moved!!
###
@app.route('/coffee',methods=["GET","POST"])
def admin():
    if request.method == "POST":
        if request.form['username'] == "vailko" and request.form['password'] == "tfcu25535":
            session["loggedin"] = "true"
            
    return render_template('admin.html')

@app.route('/coffee/status',methods=["GET"])
def adminstatus():
    if 'loggedin' in session:
        return render_template('adminstatus.html',
                               feedback=db.get_feedback(),
                               latest_comments=db.get_latest_five_comments(),
                               total_userratings=db.total_userratings())
    else:
        return redirect("/coffee")

@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml')


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
