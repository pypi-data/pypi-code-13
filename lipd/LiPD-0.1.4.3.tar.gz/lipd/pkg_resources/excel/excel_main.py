import csv

import xlrd

from ..doi.doi_resolver import *
from ..helpers.bag import *
from ..helpers.directory import *
from ..helpers.zips import *
from ..helpers.blanks import *
from ..helpers.loggers import *
from ..helpers.alternates import *
from ..helpers.regexes import RE_SHEET


logger_excel = create_logger('excel_main')


def excel():
    """
    Parse data from Excel spreadsheets into LiPD files.
    :return:
    """
    dir_root = os.getcwd()

    # Find excel files
    f_list = list_files('.xls') + list_files('.xlsx')
    print("Found " + str(len(f_list)) + " Excel files")
    logger_excel.info("found excel files: {}".format(len(f_list)))

    # Run once for each file
    for name_ext in f_list:

        # Filename without extension
        name = os.path.splitext(name_ext)[0]
        name_lpd = name + '.lpd'
        print("processing: {}".format(name_ext))
        logger_excel.info("processing: {}".format(name_ext))

        # Create a temporary folder and set paths
        dir_tmp = create_tmp_dir()
        dir_bag = os.path.join(dir_tmp, name)
        dir_data = os.path.join(dir_bag, 'data')

        # Make folders in tmp
        os.mkdir(os.path.join(dir_bag))
        os.mkdir(os.path.join(dir_data))

        pending_csv = []
        paleo_ct = 1
        chron_ct = 1
        sheets = []
        final = OrderedDict()
        logger_excel.info("variables initialized")

        """
        EACH DATA TABLE WILL BE STRUCTURED LIKE THIS
        "paleo_chron": "paleo",
        "pc_idx": 1,
        "model_idx": "",
        "table_type": "measurement",
        "table_idx": 1,
        "name": sheet,
        "filename": sheet,
        "data": { column data }
        """

        # Open excel workbook with filename
        try:
            workbook = xlrd.open_workbook(name_ext)
            logger_excel.info("opened XLRD workbook")

        except Exception as e:
            # There was a problem opening a file with XLRD
            print("Failed to open Workbook: {}".format(name))
            logger_excel.debug("excel: xlrd failed to open workbook: {}, {}".format(name, e))

        if workbook:
            # Check what worksheets are available, so we know how to proceed.
            for sheet in workbook.sheet_names():

                # Use this for when we are dealing with older naming styles of "data (qc), data, and chronology"
                old = "".join(sheet.lower().strip().split())

                # Group the related sheets together, so it's easier to place in the metadata later.
                if 'metadata' in sheet.lower():
                    metadata_str = sheet
                elif "about" not in sheet.lower() and "proxy" not in sheet.lower():
                    m = re.match(RE_SHEET, sheet.lower())
                    if m:
                        # print(m.groups())
                        model_idx = None
                        # Get the model idx number from string if it exists
                        if m.group(3):
                            model_idx = int(filter(str.isdigit, m.group(3)))

                        # Standard naming. This matches the regex and the sheet name is how we want it.
                        # paleo/chron - idx - table_type - idx
                        # Not sure what to do with m.group(2) yet
                        sheets.append({
                            "paleo_chron": m.group(1),
                            "pc_idx": int(m.group(2)),
                            "model_idx": model_idx,
                            "table_type": m.group(4),
                            "table_idx": int(m.group(5)),
                            "name": sheet,
                            "filename": sheet,
                            "data": ""
                        })
                    elif old == "data" or old in "data(qc)":
                        sheets.append({
                            "paleo_chron": "paleo",
                            "pc_idx": paleo_ct,
                            "model_idx": None,
                            "table_type": "measurement",
                            "table_idx": 1,
                            "name": sheet,
                            "filename": "Paleo{}.MeasurementTable1".format(paleo_ct),
                            "data": ""
                        })
                        paleo_ct += 1
                    elif "chronology" in old:
                        sheets.append({
                            "paleo_chron": "chron",
                            "pc_idx": chron_ct,
                            "model_idx": None,
                            "table_type": "measurement",
                            "table_idx": 1,
                            "name": sheet,
                            "filename": "Chron{}.MeasurementTable1".format(chron_ct),
                            "data": ""
                        })
                        chron_ct += 1
                    else:
                        # Sheet naming is not standard. Let the user know that this we need this to parse the sheet.
                        print("Sheet does not conform to naming standard. Skipping : {}".format(sheet))

                    # todo handling for sheet names that don't conform to standard. User input here
                    # else:
                    #     # Sheet name does not conform to standard. Prompt user
                    #     print("This sheet name does not conform to standards: {}".format(sheet))
                    #     sheet_type = input("Is this a (p) paleo or (c) chronology sheet?")
                    #     if sheet_type.lower() in ("p", "c", "paleo", "chron", "chronology"):
                    #         sheet_table = input("Is this a (d) distribution,
                        # (e) ensemble, (m) measurement, (s) summary sheet?")
                    #         if sheet_table.lower() in ("d", "e", "m", "s", "distribution", "dist",
                    #                                    "ens", "ensemble", "meas", "measurement", "sum", "summary"):
                    #             pass

            # METADATA WORKSHEETS
            # Parse Metadata sheet and add to output dictionary
            if metadata_str:
                logger_excel.info("parsing metadata worksheet")
                cells_dn_meta(workbook, metadata_str, 0, 0, final)

            # PALEO AND CHRON SHEETS
            for sheet in sheets:
                sheet_meta, sheet_csv = _parse_sheet(name, workbook, sheet)
                pending_csv.append(sheet_csv)
                sheet["data"] = sheet_meta

            # Reorganize sheet metadata into LiPD structure
            d_paleo, d_chron = _place_tables(sheets)

            # Add organized metadata into final dictionary
            final['paleoData'] = d_paleo
            final['chronData'] = d_chron

            # OUTPUT

            # Create new files and dump data in dir_data
            os.chdir(dir_data)

            # WRITE CSV
            _write_data_csv(pending_csv)

            # JSON-LD
            # Invoke DOI Resolver Class to update publisher data
            try:
                logger_excel.info("invoking doi resolver")
                final = DOIResolver(dir_root, name, final).main()
            except Exception as e:
                print("Error: doi resolver failed: {}".format(name))
                logger_excel.debug("excel: doi resolver failed: {}, {}".format(name, e))

            # Dump final_dict to a json file.
            final["LiPDVersion"] = 1.2
            write_json_to_file(name + '.jsonld', final)

            # Move files to bag root for re-bagging
            # dir : dir_data -> dir_bag
            logger_excel.info("start cleanup")
            dir_cleanup(dir_bag, dir_data)

            # Create a bag for the 3 files
            finish_bag(dir_bag)

            # dir: dir_tmp -> dir_root
            os.chdir(dir_root)

            # Check if same lpd file exists. If so, delete so new one can be made
            if os.path.isfile(name_lpd):
                os.remove(name_lpd)

            # Zip dir_bag. Creates in dir_root directory
            logger_excel.info("re-zip and rename")
            re_zip(dir_tmp, name, name_lpd)
            os.rename(name_lpd + '.zip', name_lpd)

        # Move back to dir_root for next loop.
        os.chdir(dir_root)

        # Cleanup and remove tmp directory
        shutil.rmtree(dir_tmp)

    print("Process Complete")
    return


# SORT PARSED DATA

def _place_tables(metadata):
    """

    :param metadata:
    :return:
    """

    paleo, chron = _create_metadata_skeleton(metadata)

    for item in metadata:
        pc_idx = item["pc_idx"] - 1
        m_idx = item["model_idx"]
        table_idx = item["table_idx"] - 1
        pc = item["paleo_chron"]
        name = item["name"]
        table_type = item["table_type"]
        data = item["data"]

        # Can only decrement model index if it exists. Check first.
        if m_idx:
            m_idx -= 1

        if pc == "paleo":
            # If it's measurement table, it goes in first.
            if table_type == "measurement":
                paleo[pc_idx]["paleoMeasurementTable"][table_idx] = data
            # Other types of tables go one step below
            elif table_type in ("ensemble", "distribution", "model"):
                if table_type == "model":
                    paleo[pc_idx]["paleoModel"][m_idx]["paleoModelTable"] = data
                elif table_type == "ensemble":
                    paleo[pc_idx]["paleoModel"][m_idx]["ensembleTable"] = data
                elif table_type == "distribution":
                    paleo[pc_idx]["paleoModel"][m_idx]["distributionTable"][table_idx] = data

        elif pc == "chron":
            # If it's measurement table, it goes in first.
            if table_type == "measurement":
                chron[pc_idx]["chronMeasurementTable"][table_idx] = data
            # Other types of tables go one step below
            elif table_type in ("ensemble", "distribution", "model"):
                if table_type == "model":
                    paleo[pc_idx]["chronModel"][m_idx]["chronModelTable"] = data
                elif table_type == "ensemble":
                    paleo[pc_idx]["chronModel"][m_idx]["ensembleTable"] = data
                elif table_type == "distribution":
                    paleo[pc_idx]["chronModel"][m_idx]["distributionTable"][table_idx] = data

    return paleo, chron


def _create_metadata_skeleton(metadata):
    """
    Find out what the highest number index table is, and create a list of that length.
    :return list: Blank list of N indices
    """
    pd_tmp = {"paleoMeasurementTable": [], "paleoModel": []}
    cd_tmp = {"chronMeasurementTable": [], "chronModel": []}
    cm_tmp = {"chronModelTable": {}, "ensembleTable": {}, "distributionTable": []}
    pm_tmp = {"paleoModelTable": {}, "ensembleTable": {}, "distributionTable": []}

    chron_numbers = {}
    paleo_numbers = {}

    # First, get the max number index for each list we need to build.
    for item in metadata:
        pc = item["paleo_chron"]
        tt = item["table_type"]
        pc_idx = item["pc_idx"]
        t_idx = item["table_idx"]
        m_idx = item["model_idx"]

        # Tree for chron types
        if pc == "chron":
            # Create an index for this table if there is not one already.
            if pc_idx not in chron_numbers:
                chron_numbers[pc_idx] = {"meas": 0, "models": 0, "model": {}}
            # Otherwise, start comparing indices to get the highest number for this table

            # If the models list idx is higher, then swap it.
            if m_idx:
                if m_idx > chron_numbers[pc_idx]["models"]:
                    chron_numbers[pc_idx]["models"] = m_idx

                # If this model index is not tracked yet, create it.
                if m_idx not in chron_numbers[pc_idx]["model"]:
                    chron_numbers[pc_idx]["model"] = {m_idx: {"ens": 0, "mod": 0, "dist": 0}}

            # Find what kind of table it is, and then increment count if it's higher than current.
            if tt == "measurement":
                if t_idx > chron_numbers[pc_idx]["meas"]:
                    chron_numbers[pc_idx]["meas"] = t_idx
            elif tt == "dist":
                if t_idx > chron_numbers[pc_idx]["model"][m_idx]["dist"]:
                    chron_numbers[pc_idx]["model"][m_idx]["dist"] = t_idx

        # Tree for paleo types
        elif pc == "paleo":
            # Create an index for this table if there is not one already.
            if pc_idx not in paleo_numbers:
                paleo_numbers[pc_idx] = {"meas": 0, "models": 0, "model": {}}
            # Otherwise, start comparing indices to get the highest number for this table

            # If the models list idx is higher, then swap it.
            if m_idx:
                if m_idx > paleo_numbers[pc_idx]["models"]:
                    paleo_numbers[pc_idx]["models"] = m_idx

                # If this model index is not tracked yet, create it.
                if m_idx not in paleo_numbers[pc_idx]["model"]:
                    paleo_numbers[pc_idx]["model"] = {m_idx: {"ens": 0, "mod": 0, "dist": 0}}

            # Find what kind of table it is, and then increment count if it's higher than current.
            if tt == "measurement":
                if t_idx > paleo_numbers[pc_idx]["meas"]:
                    paleo_numbers[pc_idx]["meas"] = t_idx
            elif tt == "dist":
                if t_idx > paleo_numbers[pc_idx]["model"][m_idx]["dist"]:
                    paleo_numbers[pc_idx]["model"][m_idx]["dist"] = t_idx

            # elif tt == "model":
            #     if t_idx > paleo_numbers[pc_idx]["model"]:
            #         paleo_numbers[pc_idx]["model"] = t_idx

            # elif tt == "ens":
            #     if t_idx > paleo_numbers[pc_idx]["model"][m_idx]["ens"]:
            #         paleo_numbers[pc_idx]["ens"] = t_idx

    # Create top lists with N tables
    paleo = [copy.deepcopy(pd_tmp)] * len(paleo_numbers)
    chron = [copy.deepcopy(cd_tmp)] * len(chron_numbers)

    for idx1, table in paleo_numbers.items():
        paleo[idx1-1]["paleoMeasurementTable"] = [None] * paleo_numbers[idx1]["meas"]
        paleo[idx1-1]["paleoModel"] = [copy.deepcopy(cm_tmp)] * paleo_numbers[idx1]["models"]
        for idx2, nums in table["model"].items():
            paleo[idx1-1]["paleoModel"][idx2-1] = {"paleoModelTable": {}, "ensembleTable": {},
                                               "distributionTable": [None] * nums["dist"]}

    for idx1, table in chron_numbers.items():
        chron[idx1-1]["chronMeasurementTable"] = [None] * chron_numbers[idx1]["meas"]
        chron[idx1-1]["chronModel"] = [copy.deepcopy(cm_tmp)] * chron_numbers[idx1]["models"]
        for idx2, nums in table["model"].items():
            chron[idx1-1]["chronModel"][idx2] = {"chronModelTable": {}, "ensembleTable": {},
                                               "distributionTable": [None] * nums["dist"]}

    return paleo, chron


# PARSE


def _parse_sheet(name, workbook, sheet):
    """
    The universal spreadsheet parser. Parse chron or paleo tables of type ensemble/model/summary.
    :param str name: Filename
    :param obj workbook: Excel Workbook
    :param dict sheet: Sheet path and naming info
    :return dict dict: Table metadata and numeric data
    """
    logger_excel.info("enter parse_sheet: {}".format(sheet["name"]))

    # Open the sheet from the workbook
    temp_sheet = workbook.sheet_by_name(sheet["name"])

    # Store table metadata and numeric data separately
    filename = "{}.{}.csv".format(str(name), str(sheet["name"]))
    table_name = "{}DataTableName".format(sheet["paleo_chron"])

    # Organize our root table data
    table_metadata = OrderedDict()
    table_metadata[table_name] = sheet["name"]
    table_metadata['filename'] = filename
    table_metadata['missingValue'] = 'NaN'

    # Store all CSV in here by rows
    table_data = {filename: []}

    # Master list of all column metadata
    column_metadata = []

    # Index tracks which cells are being parsed
    col_num = 0
    row_num = 0
    nrows = temp_sheet.nrows

    # Tracks which "number" each metadata column is assigned
    col_add_ct = 1

    header_keys = []
    variable_keys = []
    mv = ""

    # Markers to track where we are on the sheet
    var_header_done = False
    metadata_on = False
    metadata_done = False
    data_on = False

    try:
        # Loop for every row in the sheet
        for i in range(0, nrows):
            # Hold the contents of the current cell
            cell = temp_sheet.cell_value(row_num, col_num)

            # Skip all template lines
            if isinstance(cell, str):
                # Note and missing value entries are rogue. They are not close to the other data entries.
                if cell.lower().strip() not in EXCEL_TEMPLATE:

                    if "notes" in cell.lower():
                        # Store at the root table level
                        table_data["notes"] = temp_sheet.cell_value(row_num, 1)

                    elif cell.lower().strip() in ALTS_MV:
                        # Store at the root table level and in our function
                        mv = temp_sheet.cell_value(row_num, 1)
                        table_metadata["missingValue"] = mv

                    # Variable template header row
                    elif cell.lower() in EXCEL_HEADER:

                        # Grab the header line
                        row = temp_sheet.row(row_num)
                        header_keys = _get_header_keys(row)

                        # Turn on the marker
                        var_header_done = True

                    # Start parsing data section (bottom)
                    elif data_on:

                        # Get row of data
                        row = temp_sheet.row(row_num)

                        # Replace missing values where necessary
                        row = _replace_mvs(row, mv)

                        # Append row to list we will use to write out csv file later.
                        table_data[filename].append(row)

                    # Start parsing the metadata section. (top)
                    elif metadata_on:

                        # Reached an empty cell while parsing metadata. Mark the end of the section.
                        if cell in EMPTY:
                            metadata_on = False
                            metadata_done = True

                            # Create a list of all the variable names found
                            for entry in column_metadata:
                                try:
                                    variable_keys.append(entry["variableName"])
                                except KeyError:
                                    # missing a variableName key
                                    pass

                        # Not at the end of the section yet. Parse the metadata
                        else:
                            # Get the row data
                            row = temp_sheet.row(row_num)

                            # Get column metadata
                            col_tmp = _compile_column_metadata(row, header_keys, col_add_ct)

                            # Append to master list
                            column_metadata.append(col_tmp)
                            col_add_ct += 1

                    # Variable metadata, if variable header exists
                    elif var_header_done and not metadata_done:

                        # Start piecing column metadata together with their respective variable keys
                        metadata_on = True

                        # Get the row data
                        row = temp_sheet.row(row_num)

                        # Get column metadata
                        col_tmp = _compile_column_metadata(row, header_keys, col_add_ct)

                        # Append to master list
                        column_metadata.append(col_tmp)
                        col_add_ct += 1

                    # Variable metadata, if variable header does not exist
                    elif not var_header_done and not metadata_done and cell:
                        # LiPD Version 1.1 and earlier: Chronology sheets don't have variable headers
                        # We could blindly parse, but without a header row_num we wouldn't know where
                        # to save the metadata
                        # Play it safe and assume data for first column only: variable name
                        metadata_on = True

                        # Get the row data
                        row = temp_sheet.row(row_num)

                        # Get column metadata
                        col_tmp = _compile_column_metadata(row, header_keys, col_add_ct)

                        # Append to master list
                        column_metadata.append(col_tmp)
                        col_add_ct += 1

                    # Numeric Data. Column metadata exists and metadata_done marker is on.
                    elif metadata_done and cell in variable_keys:
                        data_on = True

            # If this is a numeric cell, 99% chance it's parsing the data columns.
            elif isinstance(cell, float) or isinstance(cell, int):
                if data_on or metadata_done:
                    # Get row of data
                    row = temp_sheet.row(row_num)

                    # Replace missing values where necessary
                    for idx, v in enumerate(row):
                        row[idx] = v.value

                    # Append row to list we will use to write out csv file later.
                    table_data[filename].append(row)

            # Move on to the next row
            row_num += 1
        table_metadata["columns"] = column_metadata
    except IndexError as e:
        logger_excel.debug("parse_sheet: IndexError: sheet: {}, row_num: {}, col_num: {}, {}".format(sheet, row_num, col_num, e))

    logger_excel.info("exit parse_sheet: {}".format(sheet))
    return table_metadata, table_data


def _replace_mvs(row, mv):
    """
    Replace Missing Values in the data rows where applicable
    :param list row: Row
    :return list: Modified row
    """
    for idx, v in enumerate(row):
        try:
            if v.value.lower() in EMPTY or v.value.lower() == mv:
                row[idx] = "NaN"
            else:
                row[idx] = v.value
        except AttributeError:
            row[idx] = v.value

    return row


def _get_header_keys(row):
    """
    Get the variable header keys from this special row
    :return list: Header keys
    """
    # Swap out NOAA keys for LiPD keys
    for idx, key in enumerate(row):
        if key.value.lower() in EXCEL_KEYS:
            row[idx] = EXCEL_KEYS[key.value.lower()]
        else:
            try:
                row[idx] = key.value.lower()
            except AttributeError:
                pass

    header_keys = _rm_cells_reverse(row)
    return header_keys


def _compile_column_metadata(row, keys, number):
    """
    Compile column metadata from one excel row ("9 part data")
    :param list row: Row of cells
    :param list keys: Variable header keys
    :return dict: Column metadata
    """
    # Store the variable keys by index in a dictionary
    column = {}

    # Use the header keys to place the column data in the dictionary
    if keys:
        for idx, key in enumerate(keys):
            column[key] = row[idx].value
        column["number"] = number

    # If there are not keys, that means it's a header-less metadata section.
    else:
        # Assume we only have one cell, because we have no keys to know what data is here.
        column["variableName"] = row[0].value
        column["number"] = number

    # Add this column to the overall metadata
    column = {k: v for k, v in column.items() if v}
    return column


def _rm_cells_reverse(l):
    """
    Remove the cells that are empty or template in reverse order. Stop when you hit data.
    :param list l: One row from the spreadsheet
    :return list: Modified row
    """
    rm = []
    # Iter the list in reverse, and get rid of empty and template cells
    for idx, key in reversed(list(enumerate(l))):
        if key.lower() in EXCEL_TEMPLATE:
            rm.append(idx)
        elif key in EMPTY:
            rm.append(idx)
        else:
            break

    for idx in rm:
        l.pop(idx)
    return l


# CSV


def _write_data_csv(csv_data):
    """
    CSV data has been parse by this point, so take it and write it file by file.
    :return:
    """
    logger_excel.info("enter write_data_csv")
    # Loop for each file and data that is stored
    for file in csv_data:
        for filename, data in file.items():

            # Make sure we're working with the right data types before trying to open and write a file
            if isinstance(filename, str) and isinstance(data, list):
                try:
                    with open(filename, 'w+') as f:
                        w = csv.writer(f)
                        for line in data:
                            w.writerow(line)
                except Exception:
                    logger_excel.debug("write_data_csv: Unable to open/write file: {}".format(filename))

    logger_excel.info("exit write_data_csv")
    return


# GEO DATA METHODS

def geometry_linestring(lat, lon, elev):
    """
    GeoJSON Linestring. Latitude and Longitude have 2 values each.
    :param list lat: Latitude values
    :param list lon:  Longitude values
    :return dict:
    """
    logger_excel.info("enter geometry_linestring")
    d = OrderedDict()
    coordinates = []
    temp = ["", ""]

    # Point type, Matching pairs.
    if lat[0] == lat[1] and lon[0] == lon[1]:
        logger_excel.info("matching geo coordinate")
        lat.pop()
        lon.pop()
        d = geometry_point(lat, lon, elev)

    else:
        # Creates coordinates list
        logger_excel.info("unique geo coordinates")
        for i in lat:
            temp[0] = i
            for j in lon:
                temp[1] = j
                coordinates.append(copy.copy(temp))
        if elev:
            for i in coordinates:
                i.append(elev)
        # Create geometry block
        d['type'] = 'Linestring'
        d['coordinates'] = coordinates
    logger_excel.info("exit geometry_linestring")
    return d


def geometry_point(lat, lon, elev):
    """
    GeoJSON point. Latitude and Longitude only have one value each
    :param list lat: Latitude values
    :param list lon: Longitude values
    :return dict:
    """
    logger_excel.info("enter geometry_point")
    coordinates = []
    point_dict = OrderedDict()
    for idx, val in enumerate(lat):
        try:
            coordinates.append(lat[idx])
            coordinates.append(lon[idx])
        except IndexError as e:
            print("Error: Invalid geo coordinates")
            logger_excel.debug("geometry_point: IndexError: lat: {}, lon: {}, {}".format(lat, lon, e))

    coordinates.append(elev)
    point_dict['type'] = 'Point'
    point_dict['coordinates'] = coordinates
    logger_excel.info("exit geometry_point")
    return point_dict


def compile_geometry(lat, lon, elev):
    """
    Take in lists of lat and lon coordinates, and determine what geometry to create
    :param list lat: Latitude values
    :param list lon: Longitude values
    :param float elev: Elevation value
    :return dict:
    """
    logger_excel.info("enter compile_geometry")
    lat = _remove_geo_placeholders(lat)
    lon = _remove_geo_placeholders(lon)

    # 4 coordinate values
    if len(lat) == 2 and len(lon) == 2:
        logger_excel.info("found 4 coordinates")
        geo_dict = geometry_linestring(lat, lon, elev)

        # # 4 coordinate values
        # if (lat[0] != lat[1]) and (lon[0] != lon[1]):
        #     geo_dict = geometry_polygon(lat, lon)
        # # 3 unique coordinates
        # else:
        #     geo_dict = geometry_multipoint(lat, lon)
        #

    # 2 coordinate values
    elif len(lat) == 1 and len(lon) == 1:
        logger_excel.info("found 2 coordinates")
        geo_dict = geometry_point(lat, lon, elev)

    # Too many points, or no points
    else:
        geo_dict = {}
        logger_excel.warn("compile_geometry: invalid coordinates: lat: {}, lon: {}".format(lat, lon))
        print("Error: Invalid geo coordinates")
    logger_excel.info("exit compile_geometry")
    return geo_dict


def compile_geo(d):
    """
    Compile top-level Geography dictionary.
    :param d:
    :return:
    """
    logger_excel.info("enter compile_geo")
    d2 = OrderedDict()
    d2['type'] = 'Feature'
    # If the necessary keys are missing, put in placeholders so there's no KeyErrors.
    for key in EXCEL_GEO:
        if key not in d:
            d[key] = ""
    # Compile the geometry based on the info available.
    d2['geometry'] = compile_geometry([d['latMin'], d['latMax']], [d['lonMin'], d['lonMax']], d['elevation'])
    try:
        d2['properties'] = {'siteName': d['siteName']}
    except KeyError as e:
        logger_excel.warn("compile_geo: KeyError: {}, {}".format("siteName", e))

    logger_excel.info("exit compile_geo")
    return d2


def compile_authors(cell):
    """
    Split the string of author names into the BibJSON format.
    :param str cell: Data from author cell
    :return: (list of dicts) Author names
    """
    logger_excel.info("enter compile_authors")
    author_lst = []
    s = cell.split(';')
    for w in s:
        author_lst.append(w.lstrip())
    logger_excel.info("exit compile_authors")
    return author_lst


# MISC HELPER METHODS


def compile_temp(d, key, value):
    """
    Compiles temporary dictionaries for metadata. Adds a new entry to an existing dictionary.
    :param dict d:
    :param str key:
    :param any value:
    :return dict:
    """
    if not value:
        d[key] = None
    elif len(value) == 1:
        d[key] = value[0]
    else:
        d[key] = value
    return d


def compile_fund(workbook, sheet, row, col):
    """
    Compile funding entries. Iter both rows at the same time. Keep adding entries until both cells are empty.
    :param obj workbook:
    :param str sheet:
    :param int row:
    :param int col:
    :return list of dict: l
    """
    logger_excel.info("enter compile_fund")
    l = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col < temp_sheet.ncols:
        col += 1
        try:
            agency = temp_sheet.cell_value(row, col)
            grant = temp_sheet.cell_value(row+1, col)
            if (agency != xlrd.empty_cell and agency not in EMPTY) or (grant != xlrd.empty_cell and grant not in EMPTY):
                if agency in EMPTY:
                    l.append({'grant': grant})
                elif grant in EMPTY:
                    l.append({'agency': agency})
                else:
                    l.append({'agency': agency, 'grant': grant})
        except IndexError as e:
            logger_excel.debug("compile_fund: IndexError: sheet:{} row:{} col:{}, {}".format(sheet, row, col, e))
    logger_excel.info("exit compile_fund")
    return l


def name_to_jsonld(title_in):
    """
    Convert formal titles to camelcase json_ld text that matches our context file
    Keep a growing list of all titles that are being used in the json_ld context
    :param str title_in:
    :return str:
    """
    title_out = ''
    try:
        title_in = title_in.lower()
        title_out = EXCEL_KEYS[title_in]
    except (KeyError, AttributeError) as e:
        for k, v in EXCEL_KEYS.items():
            if title_in == k:
                title_out = v
            elif k in title_in:
                title_out = v
    if not title_out:
        logger_excel.debug("name_to_jsonld: No match found: {}".format(title_in))
    return title_out


def instance_str(cell):
    """
    Match data type and return string
    :param any cell:
    :return str:
    """
    if isinstance(cell, str):
        return 'str'
    elif isinstance(cell, int):
        return 'int'
    elif isinstance(cell, float):
        return 'float'
    else:
        return 'unknown'


def replace_mvs(cell_entry, missing_val):
    """
    The missing value standard is "NaN". If there are other missing values present, we need to swap them.
    :param str cell_entry: Contents of target cell
    :param str missing_val:
    :return str:
    """
    if isinstance(cell_entry, str):
        missing_val_list = ['none', 'na', '', '-', 'n/a']
        if missing_val.lower() not in missing_val_list:
            missing_val_list.append(missing_val)
        try:
            if cell_entry.lower() in missing_val_list:
                cell_entry = 'NaN'
        except (TypeError, AttributeError) as e:
            logger_excel.debug("replace_missing_vals: Type/AttrError: cell: {}, mv: {} , {}".format(cell_entry, missing_val, e))
    return cell_entry


def extract_units(string_in):
    """
    Extract units from parenthesis in a string. i.e. "elevation (meters)"
    :param str string_in:
    :return str:
    """
    start = '('
    stop = ')'
    return string_in[string_in.index(start) + 1:string_in.index(stop)]


def extract_short(string_in):
    """
    Extract the short name from a string that also has units.
    :param str string_in:
    :return str:
    """
    stop = '('
    return string_in[:string_in.index(stop)]


# DATA WORKSHEET HELPER METHODS


def cells_rt_meta_pub(workbook, sheet, row, col, pub_qty):
    """
    Publication section is special. It's possible there's more than one publication.
    :param obj workbook:
    :param str sheet:
    :param int row:
    :param int col:
    :param int pub_qty: Number of distinct publication sections in this file
    :return list: Cell data for a specific row
    """
    logger_excel.info("enter cells_rt_meta_pub")
    col_loop = 0
    cell_data = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col_loop < pub_qty:
        col += 1
        col_loop += 1
        cell_data.append(temp_sheet.cell_value(row, col))
    logger_excel.info("exit cells_rt_meta_pub")
    return cell_data


def cells_rt_meta(workbook, sheet, row, col):
    """
    Traverse all cells in a row. If you find new data in a cell, add it to the list.
    :param obj workbook:
    :param str sheet:
    :param int row:
    :param int col:
    :return list: Cell data for a specific row
    """
    logger_excel.info("enter cells_rt_meta")
    col_loop = 0
    cell_data = []
    temp_sheet = workbook.sheet_by_name(sheet)
    while col_loop < temp_sheet.ncols:
        col += 1
        col_loop += 1
        try:
            if temp_sheet.cell_value(row, col) != xlrd.empty_cell and temp_sheet.cell_value(row, col) != '':
                cell_data.append(temp_sheet.cell_value(row, col))
        except IndexError as e:
            logger_excel.warn("cells_rt_meta: IndexError: sheet: {}, row: {}, col: {}, {}".format(sheet, row, col, e))
    logger_excel.info("exit cells_right_meta")
    return cell_data


def cells_dn_meta(workbook, sheet, row, col, final_dict):
    """
    Traverse all cells in a column moving downward. Primarily created for the metadata sheet, but may use elsewhere.
    Check the cell title, and switch it to.
    :param obj workbook:
    :param str sheet:
    :param int row:
    :param int col:
    :param dict final_dict:
    :return: none
    """
    logger_excel.info("enter cells_dn_meta")
    row_loop = 0
    pub_cases = ['id', 'year', 'author', 'journal', 'issue', 'volume', 'title', 'pages',
                 'reportNumber', 'abstract', 'alternateCitation']
    geo_cases = ['latMin', 'lonMin', 'lonMax', 'latMax', 'elevation', 'siteName', 'location']

    # Temp
    pub_qty = 0
    geo_temp = {}
    general_temp = {}
    pub_temp = []
    funding_temp = []

    temp_sheet = workbook.sheet_by_name(sheet)

    # Loop until we hit the max rows in the sheet
    while row_loop < temp_sheet.nrows:
        try:
            # Get cell value
            cell = temp_sheet.cell_value(row, col)

            # If there is content in the cell...
            if cell not in EMPTY:

                # Convert title to correct format, and grab the cell data for that row
                title_formal = temp_sheet.cell_value(row, col)
                title_json = name_to_jsonld(title_formal)

                # If we don't have a title for it, then it's not information we want to grab
                if title_json:

                    # Geo
                    if title_json in geo_cases:
                        cell_data = cells_rt_meta(workbook, sheet, row, col)
                        geo_temp = compile_temp(geo_temp, title_json, cell_data)

                    # Pub
                    # Create a list of dicts. One for each pub column.
                    elif title_json in pub_cases:

                        # Authors seem to be the only consistent field we can rely on to determine number of Pubs.
                        if title_json == 'author':
                            cell_data = cells_rt_meta(workbook, sheet, row, col)
                            pub_qty = len(cell_data)
                            for i in range(pub_qty):
                                author_lst = compile_authors(cell_data[i])
                                pub_temp.append({'author': author_lst, 'pubDataUrl': 'Manually Entered'})
                        else:
                            cell_data = cells_rt_meta_pub(workbook, sheet, row, col, pub_qty)
                            for pub in range(pub_qty):
                                if title_json == 'id':
                                    pub_temp[pub]['identifier'] = [{"type": "doi", "id": cell_data[pub]}]
                                else:
                                    pub_temp[pub][title_json] = cell_data[pub]
                    # Funding
                    elif title_json == 'agency':
                        funding_temp = compile_fund(workbook, sheet, row, col)

                    # All other cases do not need fancy structuring
                    else:
                        cell_data = cells_rt_meta(workbook, sheet, row, col)
                        general_temp = compile_temp(general_temp, title_json, cell_data)

        except IndexError as e:
            logger_excel.debug("cells_dn_datasheets: IndexError: sheet: {}, row: {}, col: {}, {}".format(sheet, row, col, e))
        row += 1
        row_loop += 1

    # Compile the more complicated items
    geo = compile_geo(geo_temp)

    logger_excel.info("compile metadata dictionary")
    # Insert into final dictionary
    final_dict['@context'] = "context.jsonld"
    final_dict['pub'] = pub_temp
    final_dict['funding'] = funding_temp
    final_dict['geo'] = geo

    # Add remaining general items
    for k, v in general_temp.items():
        final_dict[k] = v
    logger_excel.info("exit cells_dn_meta")
    return


# CHRONOLOGY HELPER METHODS


def count_chron_variables(temp_sheet):
    """
    Count the number of chron variables
    :param obj temp_sheet:
    :return int: variable count
    """
    total_count = 0
    start_row = traverse_to_chron_var(temp_sheet)
    while temp_sheet.cell_value(start_row, 0) != '':
        total_count += 1
        start_row += 1
    return total_count


def get_chron_var(temp_sheet, start_row):
    """
    Capture all the vars in the chron sheet (for json-ld output)
    :param obj temp_sheet:
    :param int start_row:
    :return: (list of dict) column data
    """
    col_dict = OrderedDict()
    out_list = []
    column = 1

    while (temp_sheet.cell_value(start_row, 0) != '') and (start_row < temp_sheet.nrows):
        short_cell = temp_sheet.cell_value(start_row, 0)
        units_cell = temp_sheet.cell_value(start_row, 1)
        long_cell = temp_sheet.cell_value(start_row, 2)

        # Fill the dictionary for this column
        col_dict['number'] = column
        col_dict['variableName'] = short_cell
        col_dict['description'] = long_cell
        col_dict['units'] = units_cell
        out_list.append(col_dict.copy())
        start_row += 1
        column += 1

    return out_list


def traverse_to_chron_data(temp_sheet):
    """
    Traverse down to the first row that has chron data
    :param obj temp_sheet:
    :return int: traverse_row
    """
    traverse_row = traverse_to_chron_var(temp_sheet)
    reference_var = temp_sheet.cell_value(traverse_row, 0)

    # Traverse past all the short_names, until you hit a blank cell (the barrier)
    while temp_sheet.cell_value(traverse_row, 0) != '':
        traverse_row += 1
    # Traverse past the empty cells until we hit the chron data area
    while temp_sheet.cell_value(traverse_row, 0) == '':
        traverse_row += 1

    # Check if there is a header row. If there is, move past it. We don't want that data
    if temp_sheet.cell_value(traverse_row, 0) == reference_var:
        traverse_row += 1
    logger_excel.info("traverse_to_chron_data: row:{}".format(traverse_row))
    return traverse_row


def traverse_to_chron_var(temp_sheet):
    """
    Traverse down to the row that has the first variable
    :param obj temp_sheet:
    :return int:
    """
    row = 0
    while row < temp_sheet.nrows - 1:
        if 'Parameter' in temp_sheet.cell_value(row, 0):
            row += 1
            break
        row += 1
    logger_excel.info("traverse_to_chron_var: row:{}".format(row))
    return row


def get_chron_data(temp_sheet, row, total_vars):
    """
    Capture all data in for a specific chron data row (for csv output)
    :param obj temp_sheet:
    :param int row:
    :param int total_vars:
    :return list: data_row
    """
    data_row = []
    missing_val_list = ['none', 'na', '', '-']
    for i in range(0, total_vars):
        cell = temp_sheet.cell_value(row, i)
        if isinstance(cell, str):
            cell = cell.lower()
        if cell in missing_val_list:
            cell = 'NaN'
        data_row.append(cell)
    return data_row


def _remove_geo_placeholders(l):
    """
    Remove placeholders from coordinate lists and sort
    :param list l: Lat or long list
    :return list: Modified list
    """
    for i in l:
        if not i:
            l.remove(i)
    l.sort()
    return l


if __name__ == '__main__':
    excel()
