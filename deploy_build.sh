#!/bin/bash

echo "Deploying built resources..."

# output dir is static dir (js & css in correct place) - only need to move index.html
mkdir -p omero_scriptui/templates/omero_scriptui/
mv omero_scriptui/static/omero_scriptui/index.html omero_scriptui/templates/omero_scriptui/
