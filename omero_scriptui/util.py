
import csv

from omero.util.populate_roi import DownloadingOriginalFileProvider
from omero.constants.metadata import NSCLIENTMAPANNOTATION

def read_csv(conn, original_file, delimiter, import_tags):
    """ Dedicated function to read the CSV file """
    print("Using FileAnnotation",
          f"{original_file.id.val}:{original_file.name.val}")
    provider = DownloadingOriginalFileProvider(conn)
    # read the csv
    # Needs omero-py 5.9.1 or later

    try:
        temp_file = provider.get_original_file_data(original_file)
        with open(temp_file.name, mode="rt", encoding='utf-8-sig') as f:
            csv_content = f.readlines()
    except UnicodeDecodeError as e:
        assert False, ("Error while reading the csv, convert your " +
                       "file to utf-8 encoding" +
                       str(e))

    if delimiter is None:
        try:
            # Sniffing on a maximum of four lines
            delimiter = csv.Sniffer().sniff("\n".join(csv_content[:4]),
                                            ",;\t").delimiter
        except Exception as e:
            assert False, ("Failed to sniff CSV delimiter: " + str(e))
    rows = list(csv.reader(csv_content, delimiter=delimiter))

    rowlen = len(rows[0])
    error_msg = (
        "CSV rows length mismatch: Header has {} " +
        "items, while line {} has {}"
    )
    for i in range(1, len(rows)):
        assert len(rows[i]) == rowlen, error_msg.format(
            rowlen, i, len(rows[i])
        )

    # keys are in the header row (first row for no namespaces
    # second row with namespaces declared)
    namespaces = []
    if rows[0][0].lower() == "namespace":
        namespaces = [el.strip() for el in rows[0]]
        namespaces = [ns if ns else NSCLIENTMAPANNOTATION for ns in namespaces]
        rows = rows[1:]
    header = [el.strip() for el in rows[0]]
    rows = rows[1:]

    if not import_tags:
        # We filter out the tag columns
        idx_l = [i for i in range(len(header)) if header[i].lower() != "tag"]
        header = [header[i] for i in idx_l]
        if len(namespaces) > 0:
            namespaces = [namespaces[i] for i in idx_l]
        for j in range(len(rows)):
            rows[j] = [rows[j][i] for i in idx_l]

    print(f"Header: {header}\n")
    return rows, header, namespaces
