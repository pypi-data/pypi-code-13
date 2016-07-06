from __future__ import absolute_import, division, print_function

from collections import OrderedDict

import numpy as np
import pandas as pd

from glue.external import six
from glue.core.message import (DataUpdateMessage,
                               DataAddComponentMessage, NumericalDataChangedMessage,
                               SubsetCreateMessage, ComponentsChangedMessage,
                               ComponentReplacedMessage)
from glue.core.decorators import clear_cache
from glue.core.util import split_component_view
from glue.core.hub import Hub
from glue.core.subset import Subset, SubsetState
from glue.core.component_link import ComponentLink, CoordinateComponentLink
from glue.core.exceptions import IncompatibleAttribute
from glue.core.visual import VisualAttributes
from glue.core.coordinates import Coordinates
from glue.core.contracts import contract
from glue.config import settings
from glue.utils import view_shape


# Note: leave all the following imports for component and component_id since
# they are here for backward-compatibility (the code used to live in this
# file)
from glue.core.component import Component, CoordinateComponent, DerivedComponent
from glue.core.component_id import ComponentID, ComponentIDDict, PixelComponentID

__all__ = ['Data']


class Data(object):

    """The basic data container in Glue.

    The data object stores data as a collection of
    :class:`~glue.core.component.Component` objects.  Each component stored in a
    dataset must have the same shape.

    Catalog data sets are stored such that each column is a distinct
    1-dimensional :class:`~glue.core.component.Component`.

    There are several ways to extract the actual numerical data stored in a
    :class:`~glue.core.data.Data` object::

       data = Data(x=[1, 2, 3], label='data')
       xid = data.id['x']

       data[xid]
       data.get_component(xid).data
       data['x']  # if 'x' is a unique component name

    Likewise, datasets support :ref:`fancy indexing <numpy:basics.indexing>`::

        data[xid, 0:2]
        data[xid, [True, False, True]]

    See also: :ref:`data_tutorial`
    """

    def __init__(self, label="", **kwargs):
        """

        :param label: label for data
        :type label: str

        Extra array-like keywords are extracted into components
        """
        # Coordinate conversion object
        self.coords = Coordinates()
        self._shape = ()

        # Components
        self._components = OrderedDict()
        self._pixel_component_ids = []
        self._world_component_ids = []

        self.id = ComponentIDDict(self)

        # Subsets of the data
        self._subsets = []

        # Hub that the data is attached to
        self.hub = None

        self.style = VisualAttributes(parent=self)

        self._coordinate_links = None

        self.data = self
        self.label = label

        self.edit_subset = None

        for lbl, data in sorted(kwargs.items()):
            self.add_component(data, lbl)

        self._key_joins = {}

    @property
    def subsets(self):
        """
        Tuple of subsets attached to this dataset
        """
        return tuple(self._subsets)

    @property
    def ndim(self):
        """
        Dimensionality of the dataset
        """
        return len(self.shape)

    @property
    def shape(self):
        """
        Tuple of array dimensions, like :attr:`numpy.ndarray.shape`
        """
        return self._shape

    @property
    def label(self):
        """ Convenience access to data set's label """
        return self._label

    @label.setter
    def label(self, value):
        """ Set the label to value
        """
        self._label = value
        self.broadcast(attribute='label')

    @property
    def size(self):
        """
        Total number of elements in the dataset.
        """
        return np.product(self.shape)

    @contract(component=Component)
    def _check_can_add(self, component):
        if isinstance(component, DerivedComponent):
            return component._data is self
        else:
            if len(self._components) == 0:
                return True
            return component.shape == self.shape

    @contract(cid=ComponentID, returns=np.dtype)
    def dtype(self, cid):
        """Lookup the dtype for the data associated with a ComponentID"""

        # grab a small piece of data
        ind = tuple([slice(0, 1)] * self.ndim)
        arr = self[cid, ind]
        return arr.dtype

    @contract(component_id=ComponentID)
    def remove_component(self, component_id):
        """ Remove a component from a data set

        :param component_id: the component to remove
        :type component_id: :class:`~glue.core.component_id.ComponentID`
        """
        if component_id in self._components:
            self._components.pop(component_id)

    @contract(other='isinstance(Data)',
              cid='cid_like',
              cid_other='cid_like')
    def join_on_key(self, other, cid, cid_other):
        """
        Create an *element* mapping to another dataset, by
        joining on values of ComponentIDs in both datasets.

        This join allows any subsets defined on `other` to be
        propagated to self.

        :param other: :class:`~glue.core.data.Data` to join with
        :param cid: str or :class:`glue.core.component_id.ComponentID` in this dataset to use as a key
        :param cid_other: ComponentID in the other dataset to use as a key

        :example:

        >>> d1 = Data(x=[1, 2, 3, 4, 5], k1=[0, 0, 1, 1, 2], label='d1')
        >>> d2 = Data(y=[2, 4, 5, 8, 4], k2=[1, 3, 1, 2, 3], label='d2')
        >>> d2.join_on_key(d1, 'k2', 'k1')

        >>> s = d1.new_subset()
        >>> s.subset_state = d1.id['x'] > 2
        >>> s.to_mask()
        array([False, False,  True,  True,  True], dtype=bool)

        >>> s = d2.new_subset()
        >>> s.subset_state = d1.id['x'] > 2
        >>> s.to_mask()
        array([ True, False,  True,  True, False], dtype=bool)

        The subset state selects the last 3 items in d1. These have
        key values k1 of 1 and 2. Thus, the selected items in d2
        are the elements where k2 = 1 or 2.
        """
        _i1, _i2 = cid, cid_other
        cid = self.find_component_id(cid)
        cid_other = other.find_component_id(cid_other)
        if cid is None:
            raise ValueError("ComponentID not found in %s: %s" %
                             (self.label, _i1))
        if cid_other is None:
            raise ValueError("ComponentID not found in %s: %s" %
                             (other.label, _i2))

        self._key_joins[other] = (cid, cid_other)
        other._key_joins[self] = (cid_other, cid)

    @contract(component='component_like', label='cid_like')
    def add_component(self, component, label, hidden=False):
        """ Add a new component to this data set.

        :param component: object to add. Can be a Component,
                          array-like object, or ComponentLink

        :param label:
              The label. If this is a string,
              a new :class:`glue.core.component_id.ComponentID` with this label will be
              created and associated with the Component

        :type component: :class:`~glue.core.component.Component` or
                         array-like
        :type label: :class:`str` or :class:`~glue.core.component_id.ComponentID`

        :raises:

           TypeError, if label is invalid
           ValueError if the component has an incompatible shape

        :returns:

           The ComponentID associated with the newly-added component
        """

        if isinstance(component, ComponentLink):
            component = DerivedComponent(self, component)

        if not isinstance(component, Component):
            component = Component.autotyped(component)

        if isinstance(component, DerivedComponent):
            component.set_parent(self)

        if not(self._check_can_add(component)):
            raise ValueError("The dimensions of component %s are "
                             "incompatible with the dimensions of this data: "
                             "%r vs %r" % (label, component.shape, self.shape))

        if isinstance(label, ComponentID):
            component_id = label
        else:
            component_id = ComponentID(label, hidden=hidden)

        is_present = component_id in self._components
        self._components[component_id] = component

        first_component = len(self._components) == 1
        if first_component:
            if isinstance(component, DerivedComponent):
                raise TypeError("Cannot add a derived component as "
                                "first component")
            self._shape = component.shape
            self._create_pixel_and_world_components()

        if self.hub and (not is_present):
            msg = DataAddComponentMessage(self, component_id)
            self.hub.broadcast(msg)
            msg = ComponentsChangedMessage(self)
            self.hub.broadcast(msg)

        return component_id

    @contract(link=ComponentLink,
              label='cid_like|None',
              returns=DerivedComponent)
    def add_component_link(self, link, label=None):
        """ Shortcut method for generating a new :class:`~glue.core.component.DerivedComponent`
        from a ComponentLink object, and adding it to a data set.

        :param link: :class:`~glue.core.component_link.ComponentLink`
        :param label: The ComponentID or label to attach to.
        :type label: :class:`~glue.core.component_id.ComponentID` or str

        :returns:
            The :class:`~glue.core.component.DerivedComponent` that was added
        """
        if label is not None:
            if not isinstance(label, ComponentID):
                label = ComponentID(label)
            link.set_to_id(label)

        if link.get_to_id() is None:
            raise TypeError("Cannot add component_link: "
                            "has no 'to' ComponentID")

        dc = DerivedComponent(self, link)
        to_ = link.get_to_id()
        self.add_component(dc, to_)
        return dc

    def _create_pixel_and_world_components(self):
        for i in range(self.ndim):
            comp = CoordinateComponent(self, i)
            label = pixel_label(i, self.ndim)
            cid = PixelComponentID(i, "Pixel Axis %s" % label, hidden=True)
            self.add_component(comp, cid)
            self._pixel_component_ids.append(cid)
        if self.coords:
            for i in range(self.ndim):
                comp = CoordinateComponent(self, i, world=True)
                label = self.coords.axis_label(i)
                cid = self.add_component(comp, label, hidden=True)
                self._world_component_ids.append(cid)

    @property
    def components(self):
        """ All :class:`ComponentIDs <glue.core.component_id.ComponentID>` in the Data

        :rtype: list
        """
        return sorted(self._components.keys(), key=lambda x: x.label)

    @property
    def visible_components(self):
        """ :class:`ComponentIDs <glue.core.component_id.ComponentID>` for all non-hidden components.

        :rtype: list
        """
        return [cid for cid, comp in self._components.items()
                if not cid.hidden and not comp.hidden]

    @property
    def primary_components(self):
        """The ComponentIDs not associated with a :class:`~glue.core.component.DerivedComponent`

        :rtype: list
        """
        return [c for c in self.component_ids() if
                not isinstance(self._components[c], DerivedComponent)]

    @property
    def derived_components(self):
        """The ComponentIDs for each :class:`~glue.core.component.DerivedComponent`

        :rtype: list
        """
        return [c for c in self.component_ids() if
                isinstance(self._components[c], DerivedComponent)]

    @property
    def pixel_component_ids(self):
        """
        The :class:`ComponentIDs <glue.core.component_id.ComponentID>` for each pixel coordinate.
        """
        return self._pixel_component_ids

    @property
    def world_component_ids(self):
        """
        The :class:`ComponentIDs <glue.core.component_id.ComponentID>` for each world coordinate.
        """
        return self._world_component_ids

    @contract(label='cid_like', returns='inst($ComponentID)|None')
    def find_component_id(self, label):
        """ Retrieve component_ids associated by label name.

        :param label: ComponentID or string to search for

        :returns:
            The associated ComponentID if label is found and unique, else None
        """
        result = [cid for cid in self.component_ids() if
                  cid.label == label or cid is label]
        if len(result) == 1:
            return result[0]

    @property
    def coordinate_links(self):
        """A list of the ComponentLinks that connect pixel and
        world. If no coordinate transformation object is present,
        return an empty list.
        """
        if self._coordinate_links:
            return self._coordinate_links

        if not self.coords:
            return []

        if self.ndim != len(self._pixel_component_ids) or \
                self.ndim != len(self._world_component_ids):
                # haven't populated pixel, world coordinates yet
            return []

        def make_toworld_func(i):
            def pix2world(*args):
                return self.coords.pixel2world(*args[::-1])[::-1][i]
            return pix2world

        def make_topixel_func(i):
            def world2pix(*args):
                return self.coords.world2pixel(*args[::-1])[::-1][i]
            return world2pix

        result = []
        for i in range(self.ndim):
            link = CoordinateComponentLink(self._pixel_component_ids,
                                           self._world_component_ids[i],
                                           self.coords, i)
            result.append(link)
            link = CoordinateComponentLink(self._world_component_ids,
                                           self._pixel_component_ids[i],
                                           self.coords, i, pixel2world=False)
            result.append(link)

        self._coordinate_links = result
        return result

    @contract(axis=int, returns=ComponentID)
    def get_pixel_component_id(self, axis):
        """Return the pixel :class:`glue.core.component_id.ComponentID` associated with a given axis
        """
        return self._pixel_component_ids[axis]

    @contract(axis=int, returns=ComponentID)
    def get_world_component_id(self, axis):
        """Return the world :class:`glue.core.component_id.ComponentID` associated with a given axis
        """
        return self._world_component_ids[axis]

    @contract(returns='list(inst($ComponentID))')
    def component_ids(self):
        """
        Equivalent to :attr:`Data.components`
        """
        return list(self._components.keys())

    @contract(subset='isinstance(Subset)|None',
              color='color|None',
              label='string|None',
              returns=Subset)
    def new_subset(self, subset=None, color=None, label=None, **kwargs):
        """
        Create a new subset, and attach to self.

        .. note:: The preferred way for creating subsets is via
            :meth:`~glue.core.data_collection.DataCollection.new_subset_group`.
            Manually-instantiated subsets will **not** be
            represented properly by the UI

        :param subset: optional, reference subset or subset state.
                       If provided, the new subset will copy the logic of
                       this subset.

        :returns: The new subset object
        """
        nsub = len(self.subsets)
        color = color or settings.SUBSET_COLORS[nsub % len(settings.SUBSET_COLORS)]
        label = label or "%s.%i" % (self.label, nsub + 1)
        new_subset = Subset(self, color=color, label=label, **kwargs)
        if subset is not None:
            new_subset.subset_state = subset.subset_state.copy()

        self.add_subset(new_subset)
        return new_subset

    @contract(subset='inst($Subset, $SubsetState)')
    def add_subset(self, subset):
        """Assign a pre-existing subset to this data object.

        :param subset: A :class:`~glue.core.subset.Subset` or
                       :class:`~glue.core.subset.SubsetState` object

        If input is a :class:`~glue.core.subset.SubsetState`,
        it will be wrapped in a new Subset automatically

        .. note:: The preferred way for creating subsets is via
            :meth:`~glue.core.data_collection.DataCollection.new_subset_group`.
            Manually-instantiated subsets will **not** be
            represented properly by the UI
        """
        if subset in self.subsets:
            return  # prevents infinite recursion
        if isinstance(subset, SubsetState):
            # auto-wrap state in subset
            state = subset
            subset = Subset(None)
            subset.subset_state = state

        self._subsets.append(subset)

        if subset.data is not self:
            subset.do_broadcast(False)
            subset.data = self
            subset.label = subset.label  # hacky. disambiguates name if needed

        if self.hub is not None:
            msg = SubsetCreateMessage(subset)
            self.hub.broadcast(msg)

        subset.do_broadcast(True)

    @contract(hub=Hub)
    def register_to_hub(self, hub):
        """ Connect to a hub.

        This method usually doesn't have to be called directly, as
        DataCollections manage the registration of data objects
        """
        if not isinstance(hub, Hub):
            raise TypeError("input is not a Hub object: %s" % type(hub))
        self.hub = hub

    @contract(attribute='string')
    def broadcast(self, attribute):
        """
        Send a :class:`~glue.core.message.DataUpdateMessage` to the hub

        :param attribute: Name of an attribute that has changed (or None)
        :type attribute: string
        """
        if not self.hub:
            return
        msg = DataUpdateMessage(self, attribute=attribute)
        self.hub.broadcast(msg)

    @contract(old=ComponentID, new=ComponentID)
    def update_id(self, old, new):
        """Reassign a component to a different :class:`glue.core.component_id.ComponentID`

        :param old: The old :class:`glue.core.component_id.ComponentID`.
        :param new: The new :class:`glue.core.component_id.ComponentID`.
        """

        if new is old:
            return

        changed = False
        if old in self._components:
            self._components[new] = self._components[old]
            changed = True
        try:
            index = self._pixel_component_ids.index(old)
            self._pixel_component_ids[index] = new
            changed = True
        except ValueError:
            pass
        try:
            index = self._world_component_ids.index(old)
            self._world_component_ids[index] = new
            changed = True
        except ValueError:
            pass

        if changed and self.hub is not None:
            # promote hidden status
            new._hidden = new.hidden and old.hidden

            # remove old component and broadcast the change
            # see #508 for discussion of this
            self._components.pop(old)
            msg = ComponentReplacedMessage(self, old, new)
            self.hub.broadcast(msg)

    def __str__(self):
        s = "Data Set: %s\n" % self.label
        s += "Number of dimensions: %i\n" % self.ndim
        s += "Shape: %s\n" % ' x '.join([str(x) for x in self.shape])
        s += "Components:\n"
        for i, component in enumerate(self._components):
            s += " %i) %s\n" % (i, component)
        return s[:-1]

    def __repr__(self):
        return 'Data (label: %s)' % self.label

    def __setattr__(self, name, value):
        if name == "hub" and hasattr(self, 'hub') \
                and self.hub is not value and self.hub is not None:
            raise AttributeError("Data has already been assigned "
                                 "to a different hub")
        object.__setattr__(self, name, value)

    def __getitem__(self, key):
        """ Shortcut syntax to access the numerical data in a component.
        Equivalent to:

        ``component = data.get_component(component_id).data``

        :param key:
          The component to fetch data from

        :type key: :class:`~glue.core.component_id.ComponentID`

        :returns: :class:`~numpy.ndarray`
        """
        key, view = split_component_view(key)
        if isinstance(key, six.string_types):
            _k = key
            key = self.find_component_id(key)
            if key is None:
                raise IncompatibleAttribute(_k)

        if isinstance(key, ComponentLink):
            return key.compute(self, view)

        try:
            comp = self._components[key]
        except KeyError:
            raise IncompatibleAttribute(key)

        shp = view_shape(self.shape, view)
        if view is not None:
            result = comp[view]
        else:
            if comp.categorical:
                result = comp.codes
            else:
                result = comp.data

        assert result.shape == shp, \
            "Component view returned bad shape: %s %s" % (result.shape, shp)
        return result

    def __setitem__(self, key, value):
        """
        Wrapper for data.add_component()
        """
        self.add_component(value, key)

    @contract(component_id='cid_like|None', returns=Component)
    def get_component(self, component_id):
        """Fetch the component corresponding to component_id.

        :param component_id: the component_id to retrieve
        """
        if component_id is None:
            raise IncompatibleAttribute()

        if isinstance(component_id, six.string_types):
            component_id = self.id[component_id]

        try:
            return self._components[component_id]
        except KeyError:
            raise IncompatibleAttribute(component_id)

    def to_dataframe(self, index=None):
        """ Convert the Data object into a pandas.DataFrame object

        :param index: Any 'index-like' object that can be passed to the pandas.Series constructor

        :return: pandas.DataFrame
        """

        h = lambda comp: self.get_component(comp).to_series(index=index)
        df = pd.DataFrame(dict((comp.label, h(comp)) for comp in self.components))
        order = [comp.label for comp in self.components]
        return df[order]

    @contract(mapping="dict(inst($Component, $ComponentID):array_like)")
    def update_components(self, mapping):
        """
        Change the numerical data associated with some of the Components
        in this Data object.

        All changes to component numerical data should use this method,
        which broadcasts the state change to the appropriate places.

        :param mapping: A dict mapping Components or ComponenIDs to arrays.

        This method has the following restrictions:
          - New compoments must have the same shape as old compoments
          - Component subclasses cannot be updated.
        """
        for comp, data in mapping.items():
            if isinstance(comp, ComponentID):
                comp = self.get_component(comp)
            data = np.asarray(data)
            if data.shape != self.shape:
                raise ValueError("Cannot change shape of data")

            comp._data = data

        # alert hub of the change
        if self.hub is not None:
            msg = NumericalDataChangedMessage(self)
            self.hub.broadcast(msg)

        for subset in self.subsets:
            clear_cache(subset.subset_state.to_mask)


@contract(i=int, ndim=int)
def pixel_label(i, ndim):
    label = "{0}".format(i)
    if 1 <= ndim <= 3:
        label += " [{0}]".format('xyz'[ndim - 1 - i])
    return label
