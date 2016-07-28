# Copyright (C) 2015 Simon Biggs
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# http://www.gnu.org/licenses/.


import re
import numpy as np


def pull_monaco_dose(file):
    """Returns the dose grid as written within the provided monaco file.
    """
    # Find all rows that contain at least 5 decimal numbers
    # Demo of match -- https://regex101.com/r/lR4pS2/11
    # Demo of ignoring a row with numbers -- https://regex101.com/r/lR4pS2/12
    # Basic guide to regular expressions (regex):
    #    http://www.regular-expressions.info/quickstart.html
    index = np.array([
        i for i, item in enumerate(file)
        if re.search(
            '(^\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+,.*$)', item)]
        ).astype(int)

    # Read and convert these numbers to floating point
    dose = np.array([
        re.search(
            '(^\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+,\d+\.\d+,.*$)', item
        ).group(1).split(',')
        for item in file[index]]).astype(float)

    return dose


def pull_item_from_monaco(string, file):
    """Returns the values of a given header item within the given monaco file
    """
    # Convert the input string for use within regex
    string_test = re.escape(string)

    # Find the row matching the requested property
    index = np.array([
        i for i, item in enumerate(file)
        if re.search('^' + string_test + ',(.*)$', item)]).astype(int)

    # Return the item value of the given property
    result = np.array([
            re.search('^' + string_test + ',(.*)$', item).group(1).split(',')
            for item in file[index]]).astype(float)

    return np.squeeze(result)
