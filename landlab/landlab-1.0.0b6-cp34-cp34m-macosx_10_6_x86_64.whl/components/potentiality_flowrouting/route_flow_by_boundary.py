# -*- coding: utf-8 -*-
"""
This is an implementation of Vaughan Voller's experimental boundary method
reduced complexity flow router. Credit: Voller, Hobley, Paola.

Created on Fri Feb 20 09:32:27 2015

@author: danhobley (SiccarPoint), after volle001@umn.edu
"""

# ##in the diagonal case, even closed edges can produce "drag". Is this right?
# Could suppress by mirroring the diagonals

import numpy as np
from landlab import RasterModelGrid, Component, FieldError, INACTIVE_LINK, \
    CLOSED_BOUNDARY, CORE_NODE
import inspect
from landlab.utils.decorators import use_file_name_or_kwds


class PotentialityFlowRouter(Component):
    """Multidirectional flow routing using a novel method.

    This class implements Voller, Hobley, and Paola's experimental matrix
    solutions for flow routing. The method works by solving for a potential
    field at all nodes on the grid, which enforces both mass conservation
    and flow downhill along topographic gradients. It is order n and highly
    efficient, but does not return any information about flow connectivity.

    Options are permitted to allow "abstract" routing (flow enforced downslope,
    but no particular assumptions are made about the governing equations), or
    routing according to the Chezy or Manning equations. This routine assumes
    that water is distributed evenly over the surface of the cell in deriving
    the depth, and does not assume channelization. You will need to back-
    calculate channel depths for yourself using known widths at each node
    if that is what you want.

    It is VITAL you initialize this component AFTER setting boundary
    conditions.

    Note that this component offers the property `discharges_at_links`. This
    returns the discharges at all links. If method=='D8', this list will
    include diagonal links after the orthogonal links, which is why this
    information is not returned as a field.

    Discharges at nodes are recorded as the outgoing total discharge (i.e.,
    including any contribution from 'water__unit_flux_in').

    The primary method of this class is :func:`run_one_step`.

    Construction::

        PotentialityFlowRouter(grid, method='D8', flow_equation='default',
                     Chezys_C=30., Mannings_n=0.03)

    Note
    ----
    This is a "research grade" component, and is subject to dramatic change
    with little warning. No guarantees are made regarding its accuracy or
    utility. It is not recommended for user use yet!

    Parameters
    ----------
    grid : ModelGrid
        A grid.
    method : {'D8', 'D4'}, optional
        Routing method ('D8' is the default). This keyword has no effect for a
        Voronoi-based grid.
    flow_equation : {'default', 'Manning', 'Chezy'}, optional
        If Manning or Chezy, flow is routed according to the Manning or Chezy
        equation; discharge is allocated to multiple downslope nodes
        proportional to the square root of discharge; and a water__depth field
        is returned. If default, flow is allocated to multiple nodes linearly
        with slope; and the water__depth field is not calculated.
    Chezys_C : float (optional)
        Required if flow_equation == 'Chezy'.
    Mannings_n : float (optional)
        Required if flow_equation == 'Manning'.

    Examples
    --------
    >>> from landlab import HexModelGrid
    >>> import numpy as np
    >>> mg = HexModelGrid(4, 6, dx=2., shape='rect', orientation='vertical')
    >>> z = mg.add_zeros('node', 'topographic__elevation')
    >>> Q_in = mg.add_ones('node', 'water__unit_flux_in')
    >>> z += mg.node_y.copy()
    >>> potfr = PotentialityFlowRouter(mg)
    >>> potfr.run_one_step()
    >>> Q_at_core_nodes = np.array(
    ...     [ 17.02012846,  16.88791903,  13.65746194,  14.85578934,
    ...       11.41908145,  11.43630865,   8.95902559,  10.04348075,
    ...        6.28696459,   6.44316089,   4.62478522,   5.29145188])
    >>> np.allclose(mg.at_node['water__discharge'][mg.core_nodes],
    ...             Q_at_core_nodes)
    True
    """
    _name = 'PotentialityFlowRouter'

    _input_var_names = ('topographic__elevation',
                        'water__unit_flux_in',
                        )

    _output_var_names = ('water__discharge',
                         'flow__potential',
                         'water__depth',
                         )

    _var_units = {'topographic__elevation': 'm',
                  'water__unit_flux_in': 'm/s',
                  'water__discharge': 'm**3/s',
                  'flow__potential': 'm**3/s',
                  'water__depth': 'm',
                  }

    _var_mapping = {'topographic__elevation': 'node',
                    'water__unit_flux_in': 'node',
                    'water__discharge': 'node',
                    'flow__potential': 'node',
                    'water__depth': 'node',
                    }

    _var_doc = {
        'topographic__elevation': 'Land surface topographic elevation',
        'water__unit_flux_in': (
            'External volume water per area per time input to each node ' +
            '(e.g., rainfall rate)'),
        'water__discharge': (
            'Magnitude of volumetric water flux out of each node'),
        'flow__potential': (
            'Value of the hypothetical field "K", used to force water flux ' +
            'to flow downhill'),
        'water__depth': (
            'If Manning or Chezy specified, the depth of flow in the cell, ' +
            'calculated assuming flow occurs over the whole surface'),
                  }

    _min_slope_thresh = 1.e-24
    # if your flow isn't connecting up, this probably needs to be reduced

    @use_file_name_or_kwds
    def __init__(self, grid, method='D8', flow_equation='default',
                 Chezys_C=30., Mannings_n=0.03, **kwds):
        """Initialize flow router.
        """
        if RasterModelGrid in inspect.getmro(grid.__class__):
            assert grid.number_of_node_rows >= 3
            assert grid.number_of_node_columns >= 3
            self._raster = True
        else:
            self._raster = False

        self._grid = grid
        self.equation = flow_equation
        assert self.equation in ('default', 'Chezy', 'Manning')
        if self.equation == 'Chezy':
            self.chezy_C = Chezys_C
        elif self.equation == 'Manning':
            self.manning_n = Mannings_n
        assert method in ('D8', 'D4')
        if method == 'D8':
            self.route_on_diagonals = True
        else:
            self.route_on_diagonals = False

        # hacky fix because water__discharge is defined on both links and nodes
        for out_field in self._output_var_names:
            if self._var_mapping[out_field] == 'node':
                try:
                    self.grid.add_zeros(self._var_mapping[out_field],
                                        out_field, dtype=float)
                except FieldError:
                    pass
            else:
                pass
            try:
                self.grid.add_zeros('node', 'water__discharge', dtype=float)
            except FieldError:
                pass

        if self._raster:
            self.equiv_circ_diam = 2. * np.sqrt(grid.dx * grid.dy / np.pi)
        else:
            for_cell_areas = 2. * np.sqrt(grid.area_of_cell / np.pi)
            mean_A = for_cell_areas.mean()
            self.equiv_circ_diam = for_cell_areas[grid.cell_at_node]
            self.equiv_circ_diam[grid.cell_at_node == -1] = mean_A
        # ^this is the equivalent seen CSWidth of a cell for a flow in a
        # generic 360 direction
        if self.route_on_diagonals and self._raster:
            grid._create_diag_links_at_node()  # ...in case not present yet
            self._discharges_at_link = np.empty(grid._number_of_d8_links)
        else:
            self._discharges_at_link = self.grid.empty('link')

    def route_flow(self, **kwds):
        """
        """
        grid = self.grid
        self._K = grid.at_node['flow__potential']
        self._Qw = grid.at_node['water__discharge']
        z = grid.at_node['topographic__elevation']
        qwater_in = grid.at_node['water__unit_flux_in'].copy()
        qwater_in[grid.node_at_cell] *= grid.area_of_cell
        prev_K = self._K.copy()
        mismatch = 10000.
        # do the ortho nodes first, in isolation
        g = grid.calc_grad_at_link(z)
        if self.equation != 'default':
            g = np.sign(g) * np.sqrt(np.fabs(g))
            # ^...because both Manning and Chezy actually follow sqrt
            # slope, not slope
        # weight by face width - NO, because diags
        # g *= grid.width_of_face[grid.face_at_link]
        link_grad_at_node_w_dir = (
            g[grid.links_at_node] * grid.active_link_dirs_at_node)
        # active_link_dirs strips "wrong" face widths

        # now outgoing link grad sum
        outgoing_sum = (np.sum((link_grad_at_node_w_dir).clip(0.), axis=1) +
                        self._min_slope_thresh)
        pos_incoming_link_grads = (-link_grad_at_node_w_dir).clip(0.)

        if not self.route_on_diagonals or not self._raster:
            while mismatch > 1.e-6:
                K_link_ends = self._K[grid.neighbors_at_node]
                incoming_K_sum = (pos_incoming_link_grads*K_link_ends
                                  ).sum(axis=1) + self._min_slope_thresh
                self._K[:] = (incoming_K_sum + qwater_in)/outgoing_sum
                mismatch = np.sum(np.square(self._K-prev_K))
                prev_K = self._K.copy()

            upwind_K = grid.map_value_at_max_node_to_link(z, self._K)
            self._discharges_at_link[:] = upwind_K * g
            self._discharges_at_link[grid.status_at_link == INACTIVE_LINK] = 0.
        else:
            # grad on diags:
            gwd = np.empty(grid._number_of_d8_links, dtype=float)
            gd = gwd[grid.number_of_links:]
            gd[:] = (z[grid._diag_link_tonode] - z[grid._diag_link_fromnode])
            gd /= (grid._length_of_link_with_diagonals[grid.number_of_links:])
            if self.equation != 'default':
                gd[:] = np.sign(gd)*np.sqrt(np.fabs(gd))
            diag_grad_at_node_w_dir = (gwd[grid._diagonal_links_at_node] *
                                       grid._diag_active_link_dirs_at_node)

            outgoing_sum += np.sum(diag_grad_at_node_w_dir.clip(0.), axis=1)
            pos_incoming_diag_grads = (-diag_grad_at_node_w_dir).clip(0.)
            while mismatch > 1.e-6:
                K_link_ends = self._K[grid.neighbors_at_node]
                K_diag_ends = self._K[grid._diagonal_neighbors_at_node]
                incoming_K_sum = ((pos_incoming_link_grads * K_link_ends
                                   ).sum(axis=1) +
                                  (pos_incoming_diag_grads * K_diag_ends
                                   ).sum(axis=1) + self._min_slope_thresh)
                self._K[:] = (incoming_K_sum + qwater_in) / outgoing_sum
                mismatch = np.sum(np.square(self._K - prev_K))
                prev_K = self._K.copy()

            # ^this is necessary to suppress stupid apparent link Qs at flow
            # edges, if present.
            upwind_K = grid.map_value_at_max_node_to_link(z, self._K)
            upwind_diag_K = np.where(
                z[grid._diag_link_tonode] > z[grid._diag_link_fromnode],
                self._K[grid._diag_link_tonode],
                self._K[grid._diag_link_fromnode])
            self._discharges_at_link[:grid.number_of_links] = upwind_K * g
            self._discharges_at_link[grid.number_of_links:] = (
                upwind_diag_K * gd)
            self._discharges_at_link[grid._all_d8_inactive_links] = 0.

        np.multiply(self._K, outgoing_sum, out=self._Qw)
        # there is no sensible way to save discharges at links, if we route
        # on diagonals.
        # for now, let's make a property

        # now process uval and vval to give the depths, if Chezy or Manning:
        if self.equation == 'Chezy':
            # Chezy: Q = C*Area*sqrt(depth*slope)
            grid.at_node['water__depth'][:] = (
                grid.at_node['flow__potential'] / self.chezy_C /
                self.equiv_circ_diam) ** (2. / 3.)
        elif self.equation == 'Manning':
            # Manning: Q = w/n*depth**(5/3)
            grid.at_node['water__depth'][:] = (
                grid.at_node['flow__potential'] * self.manning_n /
                self.equiv_circ_diam) ** 0.6
        else:
            pass

    def run_one_step(self, **kwds):
        """Route surface-water flow over a landscape.

        Both convergent and divergent flow can occur.
        """
        self.route_flow(**kwds)

    @property
    def discharges_at_links(self):
        """Return the discharges at links.

        Note that if diagonal routing, this will return number_of_d8_links.
        Otherwise, it will be number_of_links.
        """
        return self._discharges_at_link
