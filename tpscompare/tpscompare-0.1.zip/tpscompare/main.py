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


# The os module allows for os independent file path manipulations
import os

import numpy as np

# glob allows for the use of wildcards (*) in searching for files and folders
from glob import glob

# This is the interactive plotting module
import bokeh.plotting as bkh

# Used to interpolate on a 2d grid
from scipy.interpolate import RectBivariateSpline

# This package can be installed by running:
# S:\Python Packages\run_install_all.bat
from pymonaco import load_monaco_slice


def search_and_transform_parallel_monaco(directory, scan_curvetype, scan_depth,
                                         SSD=None, average_pdd=False):
    """Search within a directory for sagittal and transverse files and then
    pull out PDDs and profiles to match that provided within the variables
    scan_curvetype and scan_depth.

    Returns the distance and relative dose to match the inputs scan_curvetype
    and scan_depth.
    """
    # Search for sagittal files within the given directory
    sagittal_filepath = glob(
        os.path.join(directory, '*Sagittal*'))[0]
    # Pull the coordinates and dose grid from within the sagittal file
    inplane_distance, inplane_depth, inplane_dose = load_monaco_slice(
        sagittal_filepath,
        orientation_to_collimator_axis='parallel', SSD=SSD)

    # Search for transverse files within the given directory
    transverse_filepath = glob(
        os.path.join(directory, '*Transverse*'))[0]
    # Pull the coordinates and dose grid from within the transverse file
    crossplane_distance, crossplane_depth, crossplane_dose = load_monaco_slice(
        transverse_filepath,
        orientation_to_collimator_axis='parallel', SSD=SSD)

    # Given the requested scan_curvetype and scan_depth convert the coordinates
    # and dose grids into profiles and pdds to match.
    distance, relative_dose = monaco_parallel_slice_to_scans(
        inplane_distance, inplane_depth, inplane_dose,
        crossplane_distance, crossplane_depth, crossplane_dose,
        scan_curvetype, scan_depth, average_pdd=average_pdd)

    return distance, relative_dose


def search_and_transform_perpendicular_monaco(directory, scan_curvetype,
                                              scan_depth):
    """A function that steps through coronal files pulling the relevent depths
    in order to return profiles with given distances and doses that can be
    plotted with scans of given curvetype and depth.

    Of importance is that to accomidate off axis scans this function makes use
    of the "centre of mass" in a given direction in order to determine the off
    axis scanning position.
    """
    # Initialise a series of python dictionaries for storing labelled data
    crossplane = {}
    inplane = {}
    monaco_dose = {}
    interpolation = {}

    inplane_offset = {}
    crossplane_offset = {}

    # Need to transform depth into the z coord slice according to how Monaco
    # saves files. This assumes the 60cm SBWaterTank phantom.
    z_slices = 300 - np.array(scan_depth).astype(int)

    # Step through each unique depth and load the relevent coronal file
    for key in np.unique(z_slices):
        # Find the filepath of the relevant coronal file
        filepath_list = glob(
            os.path.join(directory, '*Coronal.{}*'.format(key)))

        # If no file was found for the requested depth raise a meaningful error
        if len(filepath_list) < 1:
            raise Exception(
                "Searching for *Coronal.{}* returned no results".format(key))

        # Pull the first file that meets the criteria
        filepath = filepath_list[0]

        # Load the coronal file
        crossplane[key], inplane[key], monaco_dose[key] = load_monaco_slice(
            filepath, orientation_to_collimator_axis='perpendicular')
        # Create interpolation
        interpolation[key] = RectBivariateSpline(
            inplane[key], crossplane[key], monaco_dose[key], kx=1, ky=1)

        # Create offset values by finding the centre of mass in each axis
        xx, yy = np.meshgrid(crossplane[key], inplane[key])
        threshold = 0.5 * np.max(monaco_dose[key])
        weights = monaco_dose[key].copy()
        weights[weights < threshold] = 0

        inplane_offset[key] = np.average(xx, weights=weights)
        crossplane_offset[key] = np.average(yy, weights=weights)

    # Initialise the distance and relative_dose variables as a python list
    distance = []
    relative_dose = []

    # Step through the scan_curvetypes
    for i, curvetype in enumerate(scan_curvetype):
        key = z_slices[i]
        # Define the normalisation point using the centre of mass of the
        # coronal plane
        normalisation = 100 / interpolation[key].ev(
            crossplane_offset[key], inplane_offset[key])

        # If the profile is inplane then append the relevent inplane distance
        # and use the inplane offset to create the profile.
        if curvetype == 'INPLANE_PROFILE':
            distance.append(inplane[key])
            unnorm_profile = interpolation[key].ev(
                inplane[key], inplane_offset[key])
            relative_dose.append(normalisation * unnorm_profile)

        # If the profile is crossplane then append the relevent crossplane
        # distance and use the crossplane offset to create the profile.
        elif curvetype == 'CROSSPLANE_PROFILE':
            distance.append(crossplane[key])
            unnorm_profile = interpolation[key].ev(
                crossplane_offset[key], crossplane[key])
            relative_dose.append(normalisation * unnorm_profile)

        # If neither of the above two conditions are met raise an exception.
        # Slices that are perpendicular to the collimator axis are not optimum
        # for pulling PDD data.
        else:
            raise Exception("Unexpected scan_curvetype")

    return distance, relative_dose


def monaco_parallel_slice_to_scans(x_inplane, depth_inplane, dose_inplane,
                                   x_crossplane, depth_crossplane,
                                   dose_crossplane,
                                   scan_curvetype, scan_depth, average_pdd=False):
    """Takes the inplane and crossplane coordinates and their dose grids and
    pulls out the relevent PDDs or profiles as defined by scan_curvetype and
    scan_depth

    Returns the distance and relative_dose that defines these pdds and profiles
    """
    # Initialise a distance and relative_dose python list
    distance = []
    relative_dose = []

    # Step through each curvetype given within scan_curvetype
    for i, curvetype in enumerate(scan_curvetype):
        # If the curvetype in this iteration is PDD then append PDD data
        if curvetype == 'PDD':            
            distance.append(depth_inplane)
            
            if average_pdd:
                relative_dose.append(
                    average_pdd_from_monaco_slices(
                        x_inplane, depth_inplane, dose_inplane,
                        x_crossplane, depth_crossplane, dose_crossplane))
            
            else:                
                relative_dose.append(
                    pdd_from_monaco_slice(x_inplane, depth_inplane, dose_inplane))

        # Otherwise if the curvetype this iteration is an inplane profile then
        # append inplane profile data
        elif curvetype == 'INPLANE_PROFILE':
            distance.append(x_inplane)
            relative_dose.append(profile_from_monaco_slice(
                x_inplane, depth_inplane, dose_inplane,
                scan_depth[i]))

        # Otherwise if the curvetype this iteration is a crossplane profile
        # then append crossplane profile data
        elif curvetype == 'CROSSPLANE_PROFILE':
            distance.append(x_crossplane)
            relative_dose.append(profile_from_monaco_slice(
                x_crossplane, depth_crossplane, dose_crossplane,
                scan_depth[i]))

        # If none of the prior conditions have been met then an unexpected
        # curvetype was used. This should raise an error.
        else:
            raise Exception("Unexpected scan_curvetype")

    return distance, relative_dose


def pdd_from_monaco_slice(x, depth, dose):
    """Takes coordinates and a dose grid and returns the pdd normalised to dmax
    """
    interpolation = RectBivariateSpline(depth, x, dose, kx=1, ky=1)
    pdd = interpolation.ev(depth, 0)
    normalisation = 100 / pdd.max()

    return pdd * normalisation

    
def average_pdd_from_monaco_slices(x_inplane, depth_inplane, dose_inplane,
                                   x_crossplane, depth_crossplane, dose_crossplane):
    """Takes coordinates and a dose grid and returns the pdd normalised to dmax
    """
    interpolation_inplane = RectBivariateSpline(
        depth_inplane, x_inplane, dose_inplane, kx=1, ky=1)
    interpolation_crossplane = RectBivariateSpline(
        depth_crossplane, x_crossplane, dose_crossplane, kx=1, ky=1)
        
    assert np.all(depth_inplane == depth_crossplane)
    depth = depth_inplane
    pillar = np.hstack([
        interpolation_inplane.ev(depth[:,None], np.array([-6, -4, -2, 0, 2, 4, 6])[None,:]),
        interpolation_crossplane.ev(depth[:, None], np.array([-6, -4, -2, 0, 2, 4, 6])[None,:])])
    pdd = np.mean(pillar, axis=1)
    normalisation = 100 / pdd.max()

    return pdd * normalisation
    
    
def profile_from_monaco_slice(x, depth, dose, scan_depth):
    """Takes the coordinates, dose grid, and requested scan_depth and returns
    the profile normalised to the CRA.
    """
    interpolation = RectBivariateSpline(depth, x, dose, kx=1, ky=1)

    profile = interpolation.ev(scan_depth, x)
    normalisation = 100 / interpolation.ev(scan_depth, 0)

    return profile * normalisation


def bokeh_display(all_distance, all_relative_dose, legend, title, colour):
    """Loop through all the given distances and relative doses producing
    an interactive bokeh plot for each.
    """
    # Step through all the provided different plots
    for i in range(len(all_distance[0])):
        # Initialise the plot
        fig = bkh.figure(plot_width=600, plot_height=400, title=title[i])

        # Step through each line to be drawn on this plot
        for j in range(len(all_distance)):
            # Draw the relevant line
            fig.line(
                all_distance[j][i], all_relative_dose[j][i], alpha=0.7,
                line_width=2, line_color=colour[j], legend=legend[j])

        # Display the figure in the notebook
        bkh.show(fig)


def make_title(label, scan_curvetype, scan_depth):
    """Utility to create a list of titles for use with the bokeh_display
    function.
    """
    title = []
    for i, curvetype in enumerate(scan_curvetype):
        if curvetype == 'PDD':
            title.append(label + " | PDD")
        elif curvetype == 'INPLANE_PROFILE':
            title.append(label + " | inplane | " + str(scan_depth[i]))
        elif curvetype == 'CROSSPLANE_PROFILE':
            title.append(label + " | crossplane | " + str(scan_depth[i]))
        else:
            raise Exception("Unexpected curvetype")

    return title
