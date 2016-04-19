#!/bin/sh

PLUGIN=UserManual
GITVERSION=kadas

make package VERSION=$GITVERSION
scp $PLUGIN.zip pkg@pkg:www/qgis/vbs/
ssh pkg@pkg qgis-plugin-repo-scan http://pkg.sourcepole.ch/qgis /home/pkg/www/qgis
