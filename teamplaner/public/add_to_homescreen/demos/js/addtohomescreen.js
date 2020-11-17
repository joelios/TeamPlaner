/* Add to Homescreen v4.0.0 ~ (c) 2019 Chris Love ~ @license: https://love2dev.com/pwa/add-to-homescreen/ */
/*
Check out these PWA Resources:

https://love2dev.com/pwa/pwa-starter/
https://pwastarter.love2dev.com/
https://love2dev.com/blog/beforeinstallprompt/

*/

/*
       _   _ _____     _____
 ___ _| |_| |_   _|___|  |  |___ _____ ___ ___ ___ ___ ___ ___ ___
| .'| . | . | | | | . |     | . |     | -_|_ -|  _|  _| -_| -_|   |
|__,|___|___| |_| |___|__|__|___|_|_|_|___|___|___|_| |___|___|_|_|
	by Matteo Spinelli ~ http://cubiq.org <-- No longer there :<
	Upgraded for PWA Support by Chris Love ~ https://love2dev.com/
	USE PWA Starter to scaffold your core PWA files ~ https://pwastarter.love2dev.com/
*/

(function(window, document, undefined) {
  "use strict";

  // load session
  var _instance,
    _default = {
      getSesssion: getSesssion,
      updateSessionProperty: updateSessionProperty,
      updateSession: updateSession,
      clearSession: clearSession,
      optOut: optOut,
      optIn: optIn,
      displayed: displayed,
      clearDisplayCount: clearDisplayCount,
      version: "2.0.0"
    },
    SESSION_KEY = "a2hs-state";

  var platform = {
    isCompatible: false,
    nativePrompt: "onbeforeinstallprompt" in window
  };

  if ("onbeforeinstallprompt" in window) {
    window.addEventListener("beforeinstallprompt", beforeInstallPrompt);
  }

  function writeLog(logStr) {
    if (_instance.logging) {
      if (_instance.logger) {
        _instance.logger.log(logStr);
      } else {
        console.log(logStr);
      }
    }
  }

  function ath(settings) {
    //prevent duplicate instances
    if (!_instance) {
      _instance = Object.assign({}, _default, settings);

      // override defaults that are dependent on each other
      if (_instance.debug && typeof _instance.logging === "undefined") {
        _instance.logging = true;
      }

      //if no service worker then no add to homescreen
      if ("serviceWorker" in navigator) {
        var manifestEle = document.querySelector("[rel='manifest']");

        //if no manifest file then no add to homescreen
        if (!manifestEle) {
          writeLog("no manifest file");
          writeLog(
            "Add to homescreen: not displaying callout because no web manifest file present"
          );
        } else {
          navigator.serviceWorker.getRegistration().then(afterSWCheck);
        }
      } else {
        writeLog("service worker not supported");
        writeLog(
          "Add to homescreen: not displaying callout because service workers are not supported"
        );
      }
    }

    return _instance;
  }

  if ("onappinstalled" in window) {
    window.addEventListener("appinstalled", function(evt) {
      writeLog("a2hs", "installed");

      if (_instance.onInstall) {
        _instance.onInstall(evt);
      }
    });
  }

  function afterSWCheck(sw) {
    if (!sw) {
      writeLog("no service worker");
      platform.isCompatible = false;
      //return, no need to go further
      return;
    }

    checkPlatform();

    // setup the debug environment
    if (_instance.debug) {
      platform.isCompatible = true;
    }

    if (platform.isCompatible && _instance.onCanInstall) {
      _instance.onCanInstall(platform, _instance);
    }
  }

  function checkPlatform() {
    // browser info and capability
    var _ua = window.navigator.userAgent;

    platform.isIDevice = /iphone|ipod|ipad/i.test(navigator.platform);
    platform.isSamsung = /Samsung/i.test(_ua);
    platform.isFireFox = /Firefox/i.test(_ua);
    platform.isOpera = /opr/i.test(_ua);
    platform.isEdge = /edg/i.test(_ua);

    // Opera & FireFox only Trigger on Android
    if (platform.isFireFox) {
      platform.isFireFox = /android/i.test(_ua);
    }

    if (platform.isOpera) {
      platform.isOpera = /android/i.test(_ua);
    }

    platform.isChromium = "onbeforeinstallprompt" in window;
    platform.isInWebAppiOS = window.navigator.standalone === true;
    platform.isInWebAppChrome =
      window.matchMedia("(display-mode: fullscreen)").matches ||
      window.matchMedia("(display-mode: standalone)").matches ||
      window.matchMedia("(display-mode: minimal-ui)").matches;
    platform.isMobileSafari =
      platform.isIDevice &&
      _ua.indexOf("Safari") > -1 &&
      _ua.indexOf("CriOS") < 0;
    platform.isStandalone = platform.isInWebAppiOS || platform.isInWebAppChrome;
    platform.isiPad = platform.isMobileSafari && _ua.indexOf("iPad") > -1;
    platform.isiPhone = platform.isMobileSafari && _ua.indexOf("iPad") === -1;
    platform.isCompatible =
      platform.isChromium ||
      platform.isMobileSafari ||
      platform.isSamsung ||
      platform.isFireFox ||
      platform.isOpera ||
      platform.isIDevice;
  }

  function beforeInstallPrompt(evt) {
    evt.preventDefault();

    console.log("capturing the native A2HS prompt");

    platform.beforeInstallPrompt = evt;

    if (_instance.onBeforeInstallPrompt) {
      _instance.onBeforeInstallPrompt(platform);
    }
  }

  //session members
  function getSesssion() {
    return JSON.parse(localStorage.getItem(SESSION_KEY)) || _defaultSession;
  }

  function updateSessionProperty(prop, value) {
    var session = getSesssion();

    session[prop] = value;

    updateSession(session);
  }

  function updateSession(session) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }

  function clearSession() {
    session = _defaultSession;
    updateSession();
  }

  function optOut() {
    updateSessionProperty("optedout", true);
  }

  function optIn() {
    updateSessionProperty("optedout", false);
  }

  function displayed() {
    var session = getSesssion();

    session.displayCount += 1;

    updateSessionProperty("displayCount", session.displayCount);
  }

  function clearDisplayCount() {
    updateSessionProperty("displayCount", 0);
  }

  // expose to the world
  window.addToHomescreen = ath;
})(window, document);
