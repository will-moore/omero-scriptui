OMERO.omero_scriptui
=======================

This is an experimental repo to explore the steps needed to create custom user interfaces
for running OMERO scripts. It is hoped that this process can be improved and documented
to make it easier for users who wish to develop UIs for their OMERO scripts.

The process currently involves these key steps, as followed when creating
the first example UI for [Import_from_csv.py](https://github.com/ome/omero-scripts/blob/8dc923b3206cbc1334dbcb7eead6e60f222982c3/omero/annotation_scripts/Import_from_csv.py). NB: these steps can be seen in the first few commits of this repo:

 - Create a new repo from [cookiecutter-omero-webapp](https://github.com/ome/cookiecutter-omero-webapp).
 - Run `git init` and start tracking changes.
 - In the OMERO webclient, launch the script you wish to create a UI for and copy the html for the script dialog.
 - Add a url to urls.py with a corresponding views.py method and html template, using the script dialog html.
 - Remove all the script tags. This aims to reduce dependencies on jQuery etc that are used in the webclient script dialog, but removal of ajax-form functionality does result in a less smooth user experience. Needs more investigation on best approach.
 - In the views.py we need to look-up the correct script based on path, pass the ID to the template and use it to render the correct path to submit the form to webclient.
 - Add a `csrf_token` to the form.
 - Add `enctype='multipart/form-data'` attribute to the `<form>` element to all inclusion of Files.
 - Add [open_with](https://omero.readthedocs.io/en/stable/developers/Web/LinkingFromWebclient.html#open-with) functionality: Add config to the README and handle query parameters in views.py to process and pass objects to the html template.
 
 At this point (commit `eca38cc`) you should have a working UI that you can then customise further as desired, e.g.

 - Rearrange form inputs to present a more intuitive and helpful layout to users.
 - Load additional data based on selected objects to improve the script UI. E.g. load images in a selected Dataset or show Images or thumbnails in the UI.
 - Add some interactivity to the form, so users can appreciate the effect of choosing different options.
 - Based on the user's interactions, it may be possible to auto-populate various form fields (script parameters).

In the case of `Import_from_csv.py`, the following improvements were made:
 - Add a drag-and-drop file uploader to allow easier upload of a chosen CSV file.
 - Display the chosen CSV file as an html table with options for choosing columns.
 - Allow the user to select a table column that contains target object identifiers.


Add a JavaScript Framework and build tool
-----------------------------------------

We'll use [vite.js](https://vitejs.dev/) to build our JavaScript bundle, choosing the same
name for our project as above: `omero-scriptui`. I have also chosen to use React and
Vanilla JavaScript...

    cd omero-scriptui
    mkdir TEMP && cd TEMP
    npm create vite@latest
    ✔ Project name: … omero-scriptui
    ✔ Select a framework: › React
    ✔ Select a variant: › JavaScript

    # Combine the projects:
    cat omero-scriptui/.gitignore >> ../omero-scriptui/.gitignore
    rm omero-scriptui/.gitignore 
    rm omero-scriptui/README.md     # don't need this
    mv omero-scriptui/* ../omero-scriptui/
    mv omero-scriptui/.eslintrc.cjs ../omero-scriptui/
    cd ../ && rm -rf TEMP

    # we can now run Vite dev server
    cd omero-scriptui
    npm install
    npm run dev


Installation
============

Install `omero_scriptui` in development mode as follows:

    # within your python venv:
    $ cd omero-scriptui
    $ pip install -e .

Add the app to the `omero.web.apps` setting:

N.B. Here we use single quotes around double quotes:

    $ omero config append omero.web.apps '"omero_scriptui"'

Configure Open-with for individual scripts. Currently just one supported (requires https://github.com/ome/omero-scripts/pull/216)

    $ omero config append omero.web.open_with '["Import Annotations from CSV", "scriptui_import_from_csv", {"supported_objects": ["projects", "datasets", "images", "screens", "plates"]}]'


Now restart your `omero-web` server and go to
<http://localhost:4080/omero_scriptui/> in your browser.


Further Info
============

1.  This app was derived from [cookiecutter-omero-webapp](https://github.com/ome/cookiecutter-omero-webapp).
2.  For further info on depolyment, see [Deployment](https://docs.openmicroscopy.org/latest/omero/developers/Web/Deployment.html)
