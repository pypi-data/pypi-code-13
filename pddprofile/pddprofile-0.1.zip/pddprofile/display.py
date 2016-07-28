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
import bokeh.plotting as bkh


def bokeh_display(distance, relative_dose):
    """Plot the distance and relative_dose of each scan. Used to display the
    results of the mephisto import.
    """
    # Initialise the plot
    fig = bkh.figure(plot_width=600, plot_height=400)

    # Loop through all data and add a line to the plot
    for i in range(len(relative_dose)):
        # Create a random colour for plotting the line
        random_colour = tuple(np.random.uniform(high=256, size=3).astype(int))

        # Add line to the figure
        fig.line(
            distance[i], relative_dose[i], alpha=0.7, line_width=2,
            line_color=random_colour)

    # Show the figure to the user
    bkh.show(fig)
