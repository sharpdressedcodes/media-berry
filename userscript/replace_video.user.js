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
	
	// Only execute replace logic if a video exists on this page
	if (jQ("video").length > 0){
	
	    // Note, jQ replaces $ to avoid conflicts.
	    //alert("There are " + jQ('a').length + " links on this page.");
	
	    jQ("<div id='watch-media-berry-tmp' style='display: none' />").appendTo('body');
	
	    jQ("video").each(function (index) {
	
	        // we use the first source tag - maybe we should use mp4
	        var src = jQ(this).children("source:first").attr("src");
	
	        src = convertToAbsolute(src);
	
	        if (src) {
	            jQ(this).replaceWith('<div class="media-berry-video"><img class="watch-media-berry" alt="' + src + '" style="cursor: pointer;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADNQTFRFBAcHwMHBFBcX7+/voaKiQ0VFIyYm4ODggYODYmRk0NDQU1VVsLGxkZKSMzY2cnR0////l9YmXAAAABF0Uk5T/////////////////////wAlrZliAAAC7klEQVR42uyayW4sIQxFzTzUlP//2tcvUhaRuuDamGpFwote4tM2UNi+9PVhowWwABbAAlgAC2ABLIA/CpD2vAVLPxZC9vUxAOdLpDdmtyPNB3A+UMNONgMPIBVLPdvMNAATCLLTTwFIoPvvTWnUAVwmlm1OF8BEYpo9NAEuEhgWBATAnSSyWHUAqiWhWa8BsIv9v8yPA3gasjIKMOi/T9AB2GnYjhGAascBOvugCeA0/BNVMcCp4p+sEwJcpGRBBmBIzQ4JgIt6AJQEAJei/0YSbgESqZpnAwRdgMgFMETPhICeCcB9CG4AanOxy+qF4AagNNcy7lILwXsA117r9eiu/BwZBoAHlvLcPBQGwIn8F26pYHGABAYz8fKwwwAezuYeR3PwFmDDtxMnDxEGsJz9zMhDAgES80DBedhBgJ17otE8ZBAg868ULA8BBAiSOw0p4ONMgFfg+lcjCCC81b/SJjgGmgD9PJjZAL08YABpBKCdBwzADAE08/AMgCuDAHUM4LAf3YTm/OgpcOWzx/Do3YUVAzhlAObUuopF34Je9O+epSQpzI0g+pzPsWcDgM30CwSoTID+V7BRHr59lPIAMlwiVRQgMAAYowwLP8sPGACO/vcEAwaoKEBmFageL06xhw13kORwgAwAJG6HYGOU56kLwK3Nb3s0JOlRGV5V3GoP3AG0qzMv6aFlXptOs1Hc7NnTrFkRGID7Vm18JgD3AOaZADTa9arN2uj4AMkqAhjJyObQ819kQ6swPwFtAKeVhCqdG1Yd/14+uvWTN0B/eJ1n+++O78uo/9MNChjKXP+AhGNogFm6ShpAxOKn5R+V8Rg74/xxhExJJCSAZESolEtwHEE1GSpm447p4q4u5+OM6WxGxXQcQaODC7Hi8FVZkk53RNV/zwb4XzB0bsbNMxfky3rdXm7iYDfv2MvJhM3VX+H3hgjlkCmbR6Td1Rjjj9ePGVhkidsXwAJYAAtgASyABbAAPg7wT4ABAEYSjudgB/2SAAAAAElFTkSuQmCC"></div>');
	        }
	    });
	
	    jQ(".media-berry-video").css("border","8px solid #969696");
	    jQ(".media-berry-video").css("width","230px");
	    jQ(".media-berry-video").css("height","132px");
	    jQ(".media-berry-video").css("background","#E0E0E0");
	    jQ(".media-berry-video").css("border-radius","5px");
	    jQ(".media-berry-video").css("text-align","center");
	
	    jQ(".watch-media-berry").click(function () {
	        jQ('<iframe />').attr('src', ' http://localhost:29876/play/' + encodeURIComponent(jQ(this).attr("alt"))).appendTo("#watch-media-berry-tmp");
	    });
	
	    jQ('body').keydown(function(e) {
	        jQ('<iframe />').attr('src', ' http://localhost:29876/control/' + String.fromCharCode(e.keyCode)).appendTo("#watch-media-berry-tmp");
	    });
	
	    // Dirty to do this here but JQuery seems to do this in further versions
	    function convertToAbsolute(link) {
	        if (link.indexOf("http") == 0) {
	            return link;
	        }
	        if (link.indexOf(".") != 0) {
	            if (link.indexOf("/") == 0) {
	                link = link.substr(1, link.length);
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
}

// load jQuery and execute the main function
addJQuery(main);
