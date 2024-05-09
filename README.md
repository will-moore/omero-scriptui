OMERO.omero_scriptui
=======================

User Interfaces for running various OMERO scripts.

Installation
============

Install `omero_scriptui` in development mode as follows:

    # within your python venv:
    $ cd omero-scriptui
    $ pip install -e .

Add the app to the `omero.web.apps` setting:

N.B. Here we use single quotes around double quotes:

    $ omero config append omero.web.apps '"omero_scriptui"'

Optionally, add a link "Script UI" at the top of the webclient to
open the index page of this app:

    $ omero config append omero.web.ui.top_links '["Script UI", "omero_scriptui_index", {"title": "Open Script UI in new tab", "target": "_blank"}]'


Configure Open-with...

    $ omero config append omero.web.open_with '["Import Annotations from CSV", "scriptui_import_from_csv", {"supported_objects": ["projects", "datasets", "images", "screens", "plates"]}]'


Now restart your `omero-web` server and go to
<http://localhost:4080/omero_scriptui/> in your browser.


Further Info
============

1.  This app was derived from [cookiecutter-omero-webapp](https://github.com/ome/cookiecutter-omero-webapp).
2.  For further info on depolyment, see [Deployment](https://docs.openmicroscopy.org/latest/omero/developers/Web/Deployment.html)
