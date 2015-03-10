#!/bin/bash

AWK="gawk"
_7Z="7za"
DEST_BASE_DIR="../repository-downloads"

PATH=/Util/UnixUtils:$PATH


for EACH in `find . -name '*' -type 'd' -print -maxdepth 1|sed 's:\\\\:/:g'`; do
    #Find version
    ADDON_XML=`find $EACH -type 'f' -name 'addon.xml' -print -maxdepth 2|sed 's:\\\\:/:g'`
    if [ "$ADDON_XML" != "" ]; then
        ADDON_VERSION=`$AWK 'BEGIN{RS=">"}{if (match($0,"<addon ") > 0) {sub("^.*version=\"*",""); sub("\"* .*$",""); print $0}}' $ADDON_XML`
        echo "Compressing $EACH, version: $ADDON_VERSION..."
        if [ ! -d "$DEST_BASE_DIR/$EACH" ]; then
            echo "Directory $DEST_BASE_DIR/$EACH does not exist! Will create it"
            mkdir "$DEST_BASE_DIR/$EACH"
        fi
        $_7Z a -mx=0 -xr!*.pyo -xr!*.pyc -xr!.* -xr!*.*~ "$DEST_BASE_DIR/$EACH/$EACH-$ADDON_VERSION.zip" $EACH
        #copy latest icon.png, if one is available
        ADDON_ICON=`find $EACH -type 'f' -name 'icon.png' -print -maxdepth 2|sed 's:\\\\:/:g'`
        if [ "$ADDON_ICON" != "" ]; then
            cp -fp $ADDON_ICON "$DEST_BASE_DIR/$EACH"
        fi
    fi
done

