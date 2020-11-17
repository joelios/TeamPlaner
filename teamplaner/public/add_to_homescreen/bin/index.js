const UglifyJS = require( "uglify-es" ),
    path = require( "path" ),
    fs = require( "fs" );

let utf8 = "utf8";

function uglifyScript() {

    return new Promise( ( resolve, reject ) => {

        let script = fs.readFileSync( "../src/addtohomescreen.js", utf8 );
        let min = new UglifyJS.minify( script, {} );

        if ( min.error ) {
            reject( min.error );
        } else {

            if ( min.code && min.code !== "" ) {

                fs.writeFileSync( "../src/addtohomescreen.min.js", min.code, utf8 );

                resolve();

            }

        }

    } );

}

uglifyScript();