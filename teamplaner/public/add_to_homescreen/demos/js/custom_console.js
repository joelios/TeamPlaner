//==========================================================
// CUSTOM JAVASCRIPT CONSOLE
// built by jakub fiala
//
// this small script intercepts the standard console methods
// and provides a way of accessing their messages,
// as well as stack traces, which is really cool.
// it formats the stack traces for popular browsers
//
// contributions welcome!
//==========================================================


//taken from http://stackoverflow.com/a/21350614
//modified to get rid of the unused add variable
function str_splice( str, index, endIndex ) {
    return str.slice( 0, index ) + str.slice( endIndex );
}

//taken from http://stackoverflow.com/a/7123542
//modified to make spans rather than anchors
if ( !String.linkify ) {

    String.prototype.linkify = function () {

        // http://, https://, ftp://
        var urlPattern = /\b(?:https?|ftp):\/\/[a-z0-9-+&@#\/%?=~_|!:,.;]*[a-z0-9-+&@#\/%=~_|]/gim;

        // www. sans http:// or https://
        var pseudoUrlPattern = /(^|[^\/])(www\.[\S]+(\b|$))/gim;

        // Email addresses
        var emailAddressPattern = /[\w.]+@[a-zA-Z_-]+?(?:\.[a-zA-Z]{2,6})+/gim;

        return this
            .replace( urlPattern, '<span class="link" data-href="$&">$&</span>' )
            .replace( pseudoUrlPattern, '$1<span class="link" data-href="http://$2">$2</span>' )
            .replace( emailAddressPattern, '<span class="link" data-href="mailto:$&">$&</span>' );
    };
}

var is_safari = navigator.userAgent.indexOf( "Safari" ) > -1;

function stack_trace_format( stackTrace ) {

    //    if ( is_safari ) {

    //this seems to kind of work for both
    //turn spaces into list elmt boundaries, linkify, and replace at signs with html entities, just for the lulz
    stackTrace = '<li>' + stackTrace.replace( /\s/gm, '</li><li>' ).linkify().replace( /\@/gm, '&commat;' );

    //again, look for the first part of the trace (which is this method, we don't want that)
    for ( var i = 0; i < stackTrace.length; i++ ) {
        if ( stackTrace[ i ] == '<' && stackTrace[ i + 1 ] == '/' && stackTrace[ i + 2 ] == 'l' ) {
            var index = i;
            //found end of this part, remove it
            stackTrace = str_splice( stackTrace, 0, index );

            break;
        }
    }

    //    }

    return stackTrace;
}

//this is where everything happens
//basic code taken from http://tobyho.com/2012/07/27/taking-over-console-log/
( function custom_console_with_traces() {

    var console = window.console;

    if ( !console ) {
        alert( "console not supported :(" );
        return;
    }

    function intercept( method ) {

        var original = console[ method ];

        console[ method ] = function () {

            var message = Array.prototype.slice.apply( arguments ).join( ' ' );

            //create an Error and get its stack trace and format it
            //            var stackTrace = stack_trace_format( new Error().stack );

            //==========================================================
            //do whatever you want with the stack trace and message here
            //==========================================================


            var target = document.querySelector( ".log-target" );

            if ( target ) {
                target.innerText += "\r\n" + message;
            }

            //==========================================================
            //make sure we still call the original method
            original.call( console, message );
        };

    }
    //intercept all methods including trace
    var methods = [ 'log', 'warn', 'error', 'trace' ];

    for ( var i = 0; i < methods.length; i++ ) {
        intercept( methods[ i ] );
    }

} )();