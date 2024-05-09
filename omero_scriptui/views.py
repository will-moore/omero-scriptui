#
# Copyright (c) 2017 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.shortcuts import render
from django.http import JsonResponse

from omeroweb.webclient.decorators import login_required
from omeroweb.webclient.controller.container import BaseContainer

from omero.model import OriginalFileI
from .util import read_csv

ALLOWED_PARAM = {
    "Project": ["Project", "Dataset", "Image"],
    "Dataset": ["Dataset", "Image"],
    "Image": ["Image"],
    "Screen": ["Screen", "Plate", "Well", "Acquisition", "Image"],
    "Plate": ["Plate", "Well", "Acquisition", "Image"],
    "Well": ["Well", "Image"],
    "Acquisition": ["Acquisition", "Image"],
    "Tag": ["Project", "Dataset", "Image",
            "Screen", "Plate", "Well", "Acquisition"]
}


# login_required: if not logged-in, will redirect to webclient
# login page. Then back to here, passing in the 'conn' connection
# and other arguments **kwargs.
@login_required()
def index(request, conn=None, **kwargs):
    # We can load data from OMERO via Blitz Gateway connection.
    # See https://docs.openmicroscopy.org/latest/omero/developers/Python.html
    experimenter = conn.getUser()

    # A dictionary of data to pass to the html template
    context = {
        "firstName": experimenter.firstName,
        "lastName": experimenter.lastName,
        "experimenterId": experimenter.id,
    }
    # print can be useful for debugging, but remove in production
    # print('context', context)

    # Render the html template and return the http response
    return render(request, "omero_scriptui/index.html", context)


@login_required()
def import_from_csv(request, conn=None, **kwargs):

    script_service = conn.getScriptService()
    sid = script_service.getScriptID("/omero/annotation_scripts/Import_from_csv.py")

    source_ids = []
    source_names = []
    source_dtype = None
    target_types = []
    for dtype in ALLOWED_PARAM.keys():
        obj_ids = request.GET.getlist(dtype.lower())
        if len(obj_ids) > 0:
            source_dtype = dtype
            target_types = ALLOWED_PARAM[dtype]
            for obj in conn.getObjects(dtype, obj_ids):
                source_names.append(obj.getName())
                source_ids.append(obj.getId())
            break

    context = {"script_id": sid,
               "source_dtype": source_dtype,
               "source_names": source_names,
               "source_ids": source_ids,
               "target_types": target_types
              }
    return render(request, "omero_scriptui/import_from_csv.html", context)


@login_required(setGroupContext=True)
def post_file_annotation(request, conn=None, **kwargs):

    fileupload = (
        "file_annotation" in request.FILES and request.FILES["file_annotation"] or None
    )
    fileAnnId = None
    if fileupload is not None and fileupload != "":
        manager = BaseContainer(conn)
        fileAnnId = manager.createFileAnnotations(fileupload, [])

    return JsonResponse({'fileAnnId': fileAnnId})


@login_required()
def read_csv_annotation(request, annId, conn=None, **kwargs):
    """
    Use read_csv() function copied from Import_from_csv script

    Returns JSON of rows (first 10), header, namespaces and row_count
    """

    file_ann = conn.getObject("Annotation", annId)
    if file_ann is None:
        return JsonResponse({"Error": "Annotation not Found"})
    original_file = file_ann.getFile()
    if original_file is None:
        return JsonResponse({"Error": "Annotation has no Original File"})
    delimiter = None
    import_tags = True
    rows, header, namespaces = read_csv(conn, original_file._obj, delimiter, import_tags)
    # Don't send all the rows back - just need enough for preview
    row_count = len(rows)
    rows = rows[:10]
    rsp = {
        "rows": rows, "header": header, "namespaces": namespaces, "row_count": row_count
    }
    return JsonResponse(rsp)
