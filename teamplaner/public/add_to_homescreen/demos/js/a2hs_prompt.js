/* Add to Homescreen Prompt v0.0.1 ~ (c) 2020 Chris Love ~ @license: https://love2dev.com/pwa/add-to-homescreen/ */
/*

This is a usable reference library to demonstrate add to homescreen best practices and integration with the add to homescreen library
The library works in concert with the add to homescreen library to know if a user can be prompted. If they can be prompted 
and the logic allows a visible prompt trigger is fired.
The real magic comes from the library maintaining the user prompt and descision state across page views.
You, the developer still need to display any dynamic prompting.
if you need to update the state, say from a menu triggered prompt, you can do that as well.

Check out these PWA Resources:

https://love2dev.com/pwa/pwa-starter/
https://pwastarter.love2dev.com/
https://love2dev.com/blog/beforeinstallprompt/

*/


( function ( window, document, undefined ) {
    "use strict";

    var _instance,
        platform,
        session;

    var options = {},
        defaults = {
            appID: "com.love2dev.addtohome", // local storage name (no need to change)
            appName: "Progressive Web App",
            debug: false, // override browser checks
            logging: false, // log reasons for showing or not showing to js console; defaults to true when debug is true
            modal: false, // prevent further actions until the message is closed
            mandatory: false, // you can't proceed if you don't add the app to the homescreen
            autostart: true, // show the message automatically
            skipFirstVisit: false, // show only to returning visitors (ie: skip the first time you visit)
            minSessions: 0, //show only after minimum number of page views
            startDelay: 1, // display the message after that many seconds from page load
            lifespan: 15, // life of the message in seconds
            displayPace: 1440, // minutes before the message is shown again (0: display every time, default 24 hours)
            mustShowCustomPrompt: false,
            maxDisplayCount: 0, // absolute maximum number of times the message will be shown to the user (0: no limit)
            validLocation: [], // list of pages where the message will be shown (array of regexes)
            onInit: null, // executed on instance creation
            onShow: null, // executed when the message is shown
            onAdd: null, // when the application is launched the first time from the homescreen (guesstimate)
            onInstall: null,
            onCancel: null,
            customCriteria: null,
            manualPrompt: null
        };


    function cancelPrompt( evt ) {

        evt.preventDefault();

        if ( options.onCancel ) {
            options.onCancel();
        }

        return false;
    }

    function handleInstall( evt ) {

        if ( options.onInstall ) {
            options.onInstall( evt );
        }

        if (
            _beforeInstallPrompt &&
            ( !options.debug || getPlatform() === "native" )
        ) {

            triggerNativePrompt();
        }

        return false;
    }

    function getPlatform( native ) {
        if ( options.debug && typeof options.debug === "string" ) {
            return options.debug;
        }

        //these should represent just about all browsers that offer an A2HS experience
        if ( platform.isChromium && native === undefined && !native ) {
            return "native";
        } else if ( platform.isFireFox ) {
            return "firefox";
        } else if ( platform.isiPad ) {
            return "ipad";
        } else if ( platform.isiPhone ) {
            return "iphone";
        } else if ( platform.isOpera ) {
            return "opera";
        } else if ( platform.isSamsung ) {
            return "samsung";
        } else if ( platform.isEdge ) {
            return "edge";
        } else if ( platform.isChromium ) {
            return "chromium";
        } else {
            return "";
        }
    }

    //this will execute a custom criteria method or just check a value to see if it returns true
    //this gives the application developer a hook to add extra custom logic to the workflow
    function passCustomCriteria() {

        if (
            options.customCriteria !== null ||
            options.customCriteria !== undefined
        ) {
            var passCustom = false;

            if ( typeof options.customCriteria === "function" ) {
                passCustom = options.customCriteria();
            } else {
                passCustom = !!options.customCriteria;
            }

            options.customCriteria = passCustom;

            if ( !passCustom ) {
                writeLog(
                    "Add to homescreen: not displaying callout because a custom criteria was not met."
                );
            }

            return passCustom;
        }

        //no custom criteria so just return true to not block the process
        return true;
    }

    //performs various checks to see if we are cleared for prompting
    function canPrompt() {
        //already evaluated the situation, so don't do it again
        if ( _canPrompt !== undefined ) {
            return _canPrompt;
        }

        _canPrompt = false;

        if ( !passCustomCriteria() ) {
            _canInstall = false;
            return false;
        }

        // the device is not supported
        if ( !platform.isCompatible ) {
            writeLog(
                "Add to homescreen: not displaying callout because device not supported"
            );
            return false;
        }

        var now = Date.now(),
            lastDisplayTime = session.lastDisplayTime;

        // we obey the display pace (prevent the message to popup too often)
        if ( now - lastDisplayTime < options.displayPace * 60000 ) {
            writeLog(
                "Add to homescreen: not displaying callout because displayed recently"
            );
            return false;
        }

        // obey the maximum number of display count
        if (
            options.maxDisplayCount &&
            session.displayCount >= options.maxDisplayCount
        ) {
            writeLog(
                "Add to homescreen: not displaying callout because displayed too many times already"
            );
            return false;
        }

        if ( session.sessions < options.minSessions ) {
            writeLog(
                "Add to homescreen: not displaying callout because not enough visits"
            );
            return false;
        }

        if (
            options.nextSession &&
            options.nextSession > 0 &&
            session.sessions >= options.nextSession
        ) {
            writeLog(
                "Add to homescreen: not displaying callout because waiting on session " +
                options.nextSession
            );
            return false;
        }

        // critical errors:
        if ( session.optedout ) {
            writeLog(
                "Add to homescreen: not displaying callout because user opted out"
            );
            return false;
        }

        if ( session.added ) {
            writeLog(
                "Add to homescreen: not displaying callout because already added to the homescreen"
            );
            return false;
        }

        // check if the app is in stand alone mode
        //this applies to iOS
        if ( platform.isStandalone ) {
            // execute the onAdd event if we haven't already
            if ( !session.added ) {
                session.added = true;
                updateSession();

                if ( options.onAdd ) {
                    options.onAdd( _instance, session );
                }
            }

            writeLog(
                "Add to homescreen: not displaying callout because in standalone mode"
            );
            return false;
        }

        // check if this is a returning visitor
        if ( !session.returningVisitor ) {
            session.returningVisitor = true;
            updateSession();

            // we do not show the message if this is your first visit
            if ( options.skipFirstVisit ) {
                writeLog(
                    "Add to homescreen: not displaying callout because skipping first visit"
                );
                return false;
            }
        }

        _canPrompt = true;

        console.log( "end canPrompt" );

        return true;
    }

    function show( force ) {
        // message already on screen
        if ( session.shown && !force ) {
            writeLog(
                "Add to homescreen: not displaying callout because already shown on screen"
            );
            return;
        }

        session.shown = true;

        if (
            document.readyState === "interactive" ||
            document.readyState === "complete"
        ) {
            _delayedShow();
        } else {
            document.onreadystatechange = function () {
                if ( document.readyState === "complete" ) {
                    _delayedShow();
                }
            };
        }
    }

    /* displays native A2HS prompt & stores results */
    function triggerNativePrompt() {

        if ( !_beforeInstallPrompt ) {
            return Promise.resolve();
        }

        return _beforeInstallPrompt
            .prompt()
            .then( function ( evt ) {
                // Wait for the user to respond to the prompt
                return _beforeInstallPrompt.userChoice;
            } )
            .then( function ( choiceResult ) {
                session.added = choiceResult.outcome === "accepted";

                if ( session.added ) {

                    writeLog( "User accepted the A2HS prompt" );

                    if ( options.onAdd ) {
                        options.onAdd( choiceResult );
                    }

                } else {

                    if ( options.onCancel ) {
                        options.onCancel( choiceResult );
                    }

                    session.optedout = true;
                    writeLog( "User dismissed the A2HS prompt" );
                }

                updateSession();

                _beforeInstallPrompt = null;
            } )
            .catch( function ( err ) {
                writeLog( err.message );

                if ( err.message.indexOf( "user gesture" ) > -1 ) {
                    options.mustShowCustomPrompt = true;
                    _delayedShow();
                } else if ( err.message.indexOf( "The app is already installed" ) > -1 ) {
                    console.log( err.message );
                    session.added = true;
                    updateSession();
                } else {
                    console.log( err );

                    return err;
                }
            } );
    }

    function removeSession( appID ) {
        localStorage.removeItem( appID || ath.defaults.appID );
    }

    function writeLog( logStr ) {
        if ( options.logging ) {

            if ( options.logger ) {
                options.logger.log( logStr );
            } else {
                console.log( logStr );
            }

        }
    }

    function _show() {

        if ( canPrompt() ) {

            _instance.beforeInstallPrompt = "onbeforeinstallprompt" in window;

            // fire the custom onShow event
            if ( options.onShow ) {
                options.onShow( platform, session, _instance );
            }

            // increment the display count
            session.lastDisplayTime = Date.now();
            session.displayCount++;

            updateSession();

        } else if ( canInstall() ) {
            // fire the custom onShow event
            if ( options.onCanInstall ) {
                options.onCanInstall( platform, session, _instance );
            }

        }
    }

    function trigger() {
        _show();
    }

    function updateSession() {
        localStorage.setItem( options.appID, JSON.stringify( session ) );
    }

    function clearSession() {
        session = _defaultSession;
        updateSession();
    }

    function optOut() {
        session.optedout = true;
        updateSession();
    }

    function optIn() {
        session.optedout = false;
        updateSession();
    }

    function clearDisplayCount() {
        session.displayCount = 0;
        updateSession();
    }

    function _delayedShow( e ) {
        setTimeout( _show(), options.startDelay * 1000 + 500 );
    }

    // expose to the world
    window.a2hsPrompt = function initialize( settings ) {

        if ( !_instance ) {
            _instance = {
                trigger: trigger,
                updateSession: updateSession,
                clearSession: clearSession,
                removeSession: removeSession,
                optOut: optOut,
                optIn: optIn,
                clearDisplayCount: clearDisplayCount,
                triggerNativePrompt: triggerNativePrompt,
                "options": Object.assign( {}, defaults, settings )
            };

        }

        return _instance;

    };


} )( window, document );