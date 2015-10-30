

var ratingstars = ["onestar", "twostar", "threestar", "fourstar", "fivestar"]; //Hold venue rating stars

function setStars() {
    for(j = 0; j < ratingstars.length; j++) {
        var ele_class = $("#" + ratingstars[j]).attr("class").split(" ")[1];
        if(ele_class == "glyphicon-star" && $("#" + ratingstars[j]).attr('value') > $("#ratingval").attr('value')) { //and ele_value < input_hidden_value
            $("#" + ratingstars[j]).toggleClass("glyphicon-star glyphicon-star-empty");
        }
    }

}


// Assign rating star functions
for(i = 0; i < ratingstars.length; i++) {
    var eleid = "#" + ratingstars[i];
    $(eleid).mouseover(function () { 
               var ele_position = $(this).attr("value");
               for(j = 0; j < ele_position; j++) {
                   var ele_class = $("#" + ratingstars[j]).attr("class").split(' ')[1];
                   if(ele_class == "glyphicon-star-empty" && $(this).attr('value') > $("#ratingval").attr("value")) {
                   $("#" + ratingstars[j]).toggleClass("glyphicon-star-empty glyphicon-star");
                   }
               }
            });

    $(eleid).mouseleave(setStars);
    
    $(eleid).click(function() {
            //Reassign rating value to the clicked stars value
            $("#ratingval").attr("value", $(this).attr("value"));
            setStars();
            });
}


/* Insert New Comment for Venue */
function postComment() {
    var venueid = document.getElementsByName("venueid")[0].value;
    var commentFname = document.getElementsByName("commentFname")[0].value;
    var commentText = document.getElementsByName("commentText")[0].value;
    var ratingval = document.getElementById("ratingval").value;

    if(ratingval < 1 || ratingval > 5) {
        $("#ratingval_errmsg").removeClass("hidden");
        return;
    } else {
        $("#ratingval_errmsg").addClass("hidden");
    }

    var data = $.param({"venueid":venueid,"commentFname":commentFname,"commentText":commentText,"ratingval":ratingval});
    
    $.ajax({
             url:'/venue/' + venueid + '/comment',
             type:"POST",
             processData:false,
             data:data,
             success: function(data) {
                var resp = jQuery.parseJSON(data);
                
                var userRatingForm = document.getElementById("user-rating-form");
                userRatingForm.parentNode.removeChild(userRatingForm);
                var userCommentEle = document.getElementById("userComment");
                if(resp['status'] == "OK") {
                    //userCommentEle.innerHTML += '<div class="alert alert-success">Success!</div>';
                    insertUserComment(ratingval, commentFname, commentText);
                    $("#new-comment").addClass("in");
                } else {
                    userCommentEle.innerHTML += '<div class="alert alert-danger">' + resp['errmsg'] + '</div>';
                }
             }
             });
}

function insertUserComment(ratingval, commentFname, userComment) {
    if(commentFname.length == 0) {
        var commentFname = "Anonymous";
    }
    var commentsEle = document.getElementById("new-comment");
    var ele = '<div class="venue-comment"><b style="margin-left:55px;">' + commentFname + '</b>';
    if(ratingval >= 3) {
        ele += '<div class="venue-user-rating text-success">';
    } else {
        ele += '<div class="venue-user-rating text-danger">';
    }

    for(i = 0; i < ratingval; i++) {
        ele += '<span class="glyphicon glyphicon-star"></span>';
    }
    for(i = 0; i < (5 - ratingval); i++) {
        ele += '<span class="glyphicon glyphicon-star-empty"></span>';
    }
    ele += '</div>';
    ele += '<p>' + userComment + '</p>';
    ele += '</div>';
    ele += '<hr>';

    commentsEle.innerHTML = ele + commentsEle.innerHTML;
}

/*
   Like and Dislike Comments
*/
function postCommentLike(url) {
    return $.ajax({
                type: "POST",
                url: url,
                success: function(data) {
                    var resp = jQuery.parseJSON(data);
                    if(resp['successful']) {
                        //Do nothing??
                        console.log("Success");
                    } else {
                        console.log("Error: " + resp['errmsg']);
                    }
                }
            });
}
function likeComment() {
    if(this.getAttribute("set") == "true") {
        return;
    } else {
        this.style.color="#3c763d";
        this.setAttribute("set", "true");

        //Find this elements id, need to see if the dislike is set
        var dislikeEleId = "dis" + this.getAttribute("id");
        var dislikeElement = document.getElementById(dislikeEleId);
        var commentid = this.getAttribute("id").split("-")[2];
        if(dislikeElement.getAttribute("set") == "true") {
            //Need to change its color, and decrement this comment dislike
            //Then increment like count
            dislikeElement.style.color = "black";
            dislikeElement.setAttribute("set", "false");
            var url = document.URL + "/comment/" + commentid + "?like=1&dislike=-1";
            postCommentLike(url);
        } else {
            //Increment like count
            var url = document.URL + "/comment/" + commentid + "?like=1&dislike=0";
            postCommentLike(url);
        }
        //Fake an auto update to the like count
        var likecnt_ele = document.getElementById("likecnt-commentid-" + commentid);
        likecnt_ele.innerText = parseInt(likecnt_ele.innerText) + 1;
    }
}

function dislikeComment(ele) {
    if(this.getAttribute('set') == "true") {
        return;
    } else {
        this.style.color="#a94442";
        this.setAttribute("set", "true");

        var likeEleId = this.getAttribute("id").substring(3);
        var likeElement = document.getElementById(likeEleId);
        var commentid = this.getAttribute("id").split("-")[2];

        if(likeElement.getAttribute("set") == "true") {
            likeElement.style.color = "black";
            likeElement.setAttribute("set","false");
            var url = document.URL + "/comment/" + commentid + "?like=-1&dislike=1";
            postCommentLike(url);
        } else {
            //Increment dislike count
            var url = document.URL + "/comment/" + commentid + "?like=0&dislike=1";
            postCommentLike(url);
        }
        //Fake an auto update to the like count
        var likecnt_ele = document.getElementById("likecnt-commentid-" + commentid);
        likecnt_ele.innerText = parseInt(likecnt_ele.innerText) - 1;
    }
}

function likeCommentHover() {
    this.style.color="#3c763d";
}

function likeCommentLeave() {
    if(this.getAttribute('set') == "false") {
        this.style.color="black";
    }
}

function dislikeCommentHover() {
    this.style.color="#a94442";
}

function dislikeCommentLeave() {
    if(this.getAttribute("set") == "false") {
        this.style.color="black";
    }
}

//Setup like elements
var likeElements = $(".glyphicon-thumbs-up");

for(i = 0; i < likeElements.length; i++) {
    var ele = likeElements[i];
    ele.onclick = likeComment
    ele.onmouseover = likeCommentHover;
    ele.onmouseleave = likeCommentLeave;
}

//Setup dislike elements
var dislikeElements = $(".glyphicon-thumbs-down");

for(i = 0; i < dislikeElements.length; i++){
    var ele = dislikeElements[i];
    ele.onclick = dislikeComment;
    ele.onmouseover = dislikeCommentHover;
    ele.onmouseleave = dislikeCommentLeave;
}

/*
   Listen to tab changes, to load comment
*/

$('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
            var activatedTab = e.target;
            var previousTab = e.relatedTarget;
            var activeTabId = activatedTab.getAttribute("id").split("-")[0];
            var previousTabId = previousTab.getAttribute("id").split("-")[0];

            if(activeTabId == "ratevail") {
                $("#user-rating-form").show();
            } else {
                $("#user-rating-form").hide();
            }

            $("#" + previousTabId + "-comments").hide();
            $("#" + activeTabId + "-comments").show();
            console.log(activeTabId);
            console.log(previousTabId);
        });

