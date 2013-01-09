// ==UserScript==
// @match 	        http://*/*
// @name            HTML5 video replacement
// @namespace       media-berry
// @description     Replaces HTML5 to local link starting native player
// @include         *
// @version         0.5
// ==/UserScript==
// a function that loads jQuery and calls a callback function when jQuery has finished loading
function addJQuery(callback) {
    var script = document.createElement("script");
    script.setAttribute("src", "//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js");
    script.addEventListener('load', function () {
        var script = document.createElement("script");
        script.textContent = "window.jQ=jQuery.noConflict(true);(" + callback.toString() + ")();";
        document.body.appendChild(script);
    }, false);
    document.body.appendChild(script);
}


// the guts of this userscript
function main() {
    // Note, jQ replaces $ to avoid conflicts.
    //alert("There are " + jQ('a').length + " links on this page.");
    var videoLinks = [];
    jQ("<div id='watch-media-berry-tmp' style='display: none' />").appendTo('body');

    jQ("video").each(function (index) {

        // TODO wir nehmen jetzt einfach mal das erste
        var src = jQ(this).children("source:first").attr("src");

        videoLinks[index] = convertToAbsolut(src);

        if (videoLinks[index]) {

            jQ(this).replaceWith('<img class="watch-media-berry" alt="'+videoLinks[index]+'" style="cursor: pointer;" src="http://cdn1.iconfinder.com/data/icons/realistiK-new/128x128/actions/player_play.png">');
        }
    });

    jQ(".watch-media-berry").click(function(){
        console.log(jQ(this).attr("alt"));
        jQ('<iframe />').attr('src', ' http://localhost:29876/'+encodeURIComponent(jQ(this).attr("alt"))).appendTo("#watch-media-berry-tmp");
    });



// Dirty to do this here but JQuery seems to do this in further versions
    function convertToAbsolut(link) {
        if (link.indexOf("http") == 0) {
            return link;
        }
        if (link.indexOf(".") != 0) {
            if (link.indexOf("/") == 0) {
               link = link.substr(1,link.length);
            }
            return getAbsolutePath() + link;


        }
    }

    function getAbsolutePath() {
        var loc = window.location;
        var pathName = loc.pathname.substring(0, loc.pathname.lastIndexOf('/') + 1);
        return loc.href.substring(0, loc.href.length - ((loc.pathname + loc.search + loc.hash).length - pathName.length));
    }
}


// load jQuery and execute the main function
addJQuery(main);
