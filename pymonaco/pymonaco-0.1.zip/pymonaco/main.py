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


import numpy as np

from .monacoread import pull_monaco_dose, pull_item_from_monaco


def load_monaco_slice(filepath, orientation_to_collimator_axis=None, SSD=None):
    """Takes the input of monaco filepath combined with the orientation to
    collimator axis of the slice. Loads and returns the coordinates and dose
    grid within the file.
    """
    if orientation_to_collimator_axis == 'parallel':
        # If the slice is parallel to the colimator axis then an SSD parameter
        # is required to convert to depth
        x, y, dose = monaco_parallel_slice(filepath, SSD=SSD)
    elif orientation_to_collimator_axis == 'perpendicular':
        x, y, dose = monaco_perpendicular_slice(filepath)
    else:
        # Raise error if an orientation_to_gantry_axis was not set
        raise Exception(
            "orientation_to_gantry_axis must be perpendicular or parallel")

    # Remove all rows and columns that only contain zero dose
    x, y, dose = compress(x, y, dose)

    return x, y, dose


def compress(x, y, dose):
    """Removes all rows and columns that only contain zero dose.
    """
    # Find the reference of rows and columns that have all dose equal to 0
    blank_axis_0 = np.all(dose == 0, axis=0)
    blank_axis_1 = np.all(dose == 0, axis=1)

    # Return x, y, and dose that are not full of zeros
    x = x[~blank_axis_0]
    y = y[~blank_axis_1]

    dose = dose[:, ~blank_axis_0]
    dose = dose[~blank_axis_1, :]

    return x, y, dose


def monaco_parallel_slice(filepath, SSD=None):
    """Takes the input of monaco filepath and SSD for a slice that is
    parallel to the colimator axis.

    Loads and returns the coordinates and dose grid within the file.
    """
    if SSD is None:
        raise Exception("Must define SSD for a perpendicular slice")

    # Load contents of file into file_contents
    with open(filepath) as file_pointer:
        file_contents = np.array(file_pointer.readlines())

    # Extract the dose grid from the file_contents
    dose = pull_monaco_dose(file_contents)

    # Pull relevant information out of the monaco file header
    upper_left = pull_item_from_monaco('Upperleft', file_contents)
    dose_res = pull_item_from_monaco('DoseResmm', file_contents)
    dosepts = pull_item_from_monaco('DosePtsxy', file_contents)
    calcgrid = pull_item_from_monaco('CalcGridResmm (x,y,z)', file_contents)

    # Monaco coordinates are set so that (0, 0) is at isocentre. Therefore
    # the use of SSD is required to be able to tranform monaco y-coord into
    # depth. The addition of half the calcgrid is to correct for Monaco's
    # incorrect SSD that occurs due to the true SSD occuring in the middle
    # of a calculation grid voxel.
    isocentre_distance = 1000
    shift = isocentre_distance - SSD*10 # + calcgrid[2]/2

    # Pull the length of the dimensions
    distance_len = np.shape(dose)[1]
    y_len = np.shape(dose)[0]

    # Confirm that the dimension lengths agree with the header value DosePtsxy
    assert np.all(dosepts == np.array([distance_len, y_len]))

    # Determine the range of the dimension values from the header value
    # Upperleft, dimension lengths and the dose grid resolution in DoseResmm.
    distance_min = upper_left[0]
    distance_max = distance_min + (distance_len - 1) * dose_res
    y_max = upper_left[1]
    y_min = y_max - (y_len - 1) * dose_res

    # Create an array with the determined min, max, and resolution values for
    # the coordinates
    distance = np.arange(distance_min, distance_max + dose_res, dose_res)
    y = np.arange(y_max, y_min - dose_res, -dose_res)

    # Convert the y coordinate into depth
    depth = shift - y

    return distance, depth, dose


def monaco_perpendicular_slice(filepath):
    """Takes the input of monaco filepath for a slice that is perpendicular to
    the colimator axis.

    Loads and returns the coordinates and dose grid within the file.
    """
    # Load contents of file into file_contents
    with open(filepath) as file_pointer:
        file_contents = np.array(file_pointer.readlines())

    # Extract the dose grid from the file_contents
    dose_before_flip = pull_monaco_dose(file_contents)

    # Use the np.flipud to flip in the "up down" direction the dose array
    dose = np.flipud(dose_before_flip)

    # Pull relevant information out of the monaco file header
    upper_left = pull_item_from_monaco('Upperleft', file_contents)
    dose_res = pull_item_from_monaco('DoseResmm', file_contents)
    dosepts = pull_item_from_monaco('DosePtsxy', file_contents)

    # Pull the length of the dimensions
    crossplane_len = np.shape(dose)[1]
    inplane_len = np.shape(dose)[0]

    # Confirm that the dimension lengths agree with the header value DosePtsxy
    assert np.all(dosepts == np.array([crossplane_len, inplane_len]))

    # Determine the range of the dimension values from the header value
    # Upperleft, dimension lengths and the dose grid resolution in DoseResmm.
    crossplane_min = upper_left[0]
    crossplane_max = crossplane_min + (crossplane_len - 1) * dose_res
    inplane_max = upper_left[1]
    inplane_min = inplane_max - (inplane_len - 1) * dose_res

    # Create an array with the determined min, max, and resolution values for
    # the coordinates
    crossplane = np.arange(crossplane_min, crossplane_max + dose_res, dose_res)
    inplane = np.arange(inplane_min, inplane_max + dose_res, dose_res)

    return crossplane, inplane, dose
