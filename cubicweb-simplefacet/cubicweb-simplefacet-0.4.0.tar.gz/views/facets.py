# -*- coding: utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-simplefacet views/facets for web ui"""

###############################################################################
### FACETS ####################################################################
###############################################################################

from contextlib import contextmanager

from rql import nodes

from logilab.common.registry import Predicate
from logilab.common.decorators import cachedproperty
from logilab.mtconverter import xml_escape

from cubicweb.utils import make_uid
from cubicweb.web import facet as facetbase, htmlwidgets
from cubicweb.web.views.facets import HasTextFacet

from cubes.simplefacet.views.views import normalize_facetid

@contextmanager
def simplefacet_facetform(wdg, onsubmit=''):
    w = wdg.w
    facet = wdg.facet
    req = facet._cw
    w(u'<form class="form-inline" action="%s" onsubmit="%s" method="post">'
      % (xml_escape(facet._cw.build_url('view')), onsubmit))
    # if the selection is started with this facet
    if '_original_rql_' in req.form:
        original_rql = req.form['_original_rql_']
    else:
        original_rql = facet.cw_rset.printable_rql()
    prefix = 'facet+rql:'
    if not original_rql.startswith(prefix):
        original_rql = '%s%s' % (prefix, original_rql)
    if req.form.get('__sts', None):
        w(u'<input type="hidden" name="__sts" value="%s" />' %  req.form['__sts'])
    w(u'<input type="hidden" name="rql" value="%s" />' % xml_escape(original_rql))
    for param, values in req.form.items():
        if param in ('_original_rql_', 'vid', '_facet'): # XXX hardcoded list
            if isinstance(values, basestring):
                values = (values,)
            for value in values:
                w(u'<input type="hidden" name="%s" value="%s" />'
                  % (xml_escape(param), xml_escape(value)))
    yield
    w(u'</form>')

class facet_applied(Predicate):
    """return 1 if the one of the specified facet is applied, 0 otherwise

    For instance, the selector below::

        __select__ = facet_applied('etype-facet')

    will return 1 if 'etype-facet' is currently applied
    """
    def __init__(self, *facetids):
        self.facetids = facetids

    def __call__(self, cls, req, *args, **kwargs):
        applied_facet_infos = req.form.get('_facet', ())
        if isinstance(applied_facet_infos, basestring):
            applied_facet_infos = (applied_facet_infos,)
        for facet_info in applied_facet_infos:
            facetid = facet_info.split('-', 1)[0]
            if facetid in self.facetids:
                return 1
        return 0

class SimpleFacetRangeFacet(facetbase.RangeFacet):
    """custom range facet on years.

    This facet allows to have only one boundary specified
    (i.e. either min-only, max-only or min-and-max).
    """
    @property
    def wdgclass(self):
        return TextInputRangeWidget

    def add_rql_restrictions(self):
        value = self._cw.form[self.__regid__]
        if not value:
            return
        infvalue, supvalue = value.split('-', 1)
        if infvalue:
            self._add_restriction(infvalue, '>=')
        if supvalue:
            self._add_restriction(supvalue, '<=')

class SimpleFacetDateRangeFacet(SimpleFacetRangeFacet):
    """custom date-range facet on years.

    This facet allows to have only one boundary specified
    (i.e. either min-only, max-only or min-and-max).
    """
    def formatvalue(self, value):
        try:
            date_value = int(value)
        except (ValueError, TypeError):
            return u'"date out-of-range"'
        return '"%04d/01/01"' % date_value


HasTextFacet.wdgclass = property(lambda self: SimpleFacetStringWidget)

class SimpleFacetRangeRQLPathFacet(facetbase.RQLPathFacet, facetbase.RangeFacet):

    @property
    def wdgclass(self):
        return TextInputRangeWidget

    def vocabulary(self):
        """return vocabulary for this facet, eg a list of (label, value)"""
        select = self.select
        select.save_state()
        if self.rql_sort:
            sort = self.sortasc
        else:
            sort = None # will be sorted on label
        try:
            facetbase.cleanup_select(select, self.filtered_variable)
            varmap, restrvar = self.add_path_to_select()

            # select.append_selected(nodes.VariableRef(restrvar))
            if self.label_variable:
                attrvar = varmap[self.label_variable]
            else:
                attrvar = restrvar
            # start RangeFacet
            minf = nodes.Function('MIN')
            minf.append(nodes.VariableRef(restrvar))
            select.add_selected(minf)
            maxf = nodes.Function('MAX')
            maxf.append(nodes.VariableRef(restrvar))
            select.add_selected(maxf)
            # end RangeFacet
            # select.append_selected(nodes.VariableRef(attrvar))
            # if sort is not None:
            #     facetbase._set_orderby(select, attrvar, sort, self.sortfunc)
            try:
                rset = self.rqlexec(select.as_string(), self.cw_rset.args)
            except Exception:
                self.exception('error while getting vocabulary for %s, rql: %s',
                               self, select.as_string())
                return ()
        finally:
            select.recover()
        # don't call rset_vocabulary on empty result set, it may be an empty
        # *list* (see rqlexec implementation)
        if rset:
            minv, maxv = rset[0]
            return [(unicode(minv), minv), (unicode(maxv), maxv)]
        return []

    def add_rql_restrictions(self):
        value = self._cw.form[self.__regid__]
        if not value:
            return
        varmap, restrvar = self.add_path_to_select(
            skiplabel=True, skipattrfilter=True)
        restrel = None
        for part in self.path:
            if isinstance(part, basestring):
                part = part.split()
            subject, rtype, object = part
            if object == self.filter_variable:
                restrel = rtype
        assert restrel
        infvalue, supvalue = value.split('-', 1)
        if infvalue:
            self._add_restriction(infvalue, '>=', restrvar, restrel)
        if supvalue:
            self._add_restriction(supvalue, '<=', restrvar, restrel)

    def _add_restriction(self, value, operator, restrvar, restrel):
        self.select.add_constant_restriction(restrvar,
                                             restrel,
                                             self.formatvalue(value),
                                             self.target_attr_type, operator)

SimpleFacetRangeRQLPathFacet.get_widget = facetbase.RangeFacet.get_widget

## widgets ####################################################################

class BasicFacetWidget(facetbase.FacetVocabularyWidget):
    """custom widget for vocabulary facets.

    The layout is kept really simple::

    <div class="facet">
      <ul>
        <li class="facetitem"><a href="...">%s</a></li>
        ...
        <li class="facetitem"><a href="...">%s</a></li>
      </ul>
    </div>
    """
    form_args = ('_facet', 'vid')

    @property
    def current_value(self):
        current_value = None
        applied_facet_infos = self.facet._cw.form.get('_facet', ())
        if isinstance(applied_facet_infos, basestring):
            applied_facet_infos = (applied_facet_infos,)
        for info in applied_facet_infos:
            facetid, facet_value = info.split(':')
            if facetid == self.facet.__regid__:
                current_value = facet_value
                break
        return current_value

    @cachedproperty
    def original_rql(self):
        if '_original_rql_' in self.facet._cw.form:
            return self.facet._cw.form['_original_rql_']
        else:
            return self.facet.cw_rset.printable_rql()

    @cachedproperty
    def facet_baseurl(self):
        req = self.facet._cw
        kwargs = {'rql': 'facet+rql:%s' % self.original_rql}
        # keep the track of a tsearch request
        if req.form.get('__sts', None):
            kwargs.update({'__sts': req.form['__sts']})
        for arg in self.form_args:
            if arg in req.form:
                kwargs[arg] = req.form[arg]
        return req.build_url('view', **kwargs)

    def build_faceturl(self, value):
        return u'%s&_facet=%s:%s' % (self.facet_baseurl, self.facet.__regid__,
                                     self.facet._cw.url_quote(value))

    def _render(self):
        w = self.w
        current_value = self.current_value
        w(u'<div class="facet">\n')
        w(u'<ul>')
        for value, label, __ in self.items:
            if value is None:
                continue
            if unicode(value) == current_value:
                continue
            w(u'<li class="facetitem"><a data-value="%s" href="%s">%s</a></li>'
              % (value, self.build_faceturl(value),
                 label))  # do not xml_escape label as it may be html
        w(u'</ul>\n')
        w(u'</div>\n')

# Make this widget the default one
facetbase.VocabularyFacet.wdgclass = property(lambda self: BasicFacetWidget)

class SimpleFacetVocabularyWidget(facetbase.FacetVocabularyWidget):

    def _render(self):
        w = self.w
        title = xml_escape(self.facet.title)
        facetid = make_uid(self.facet.__regid__)
        w(u'<div id="%s" class="facet btn-group">\n' % facetid)
        ## if self.facet._support_and_compat():
        ##     self._render_and_or(w)
        w(u'<div class="facetTitle" cubicweb:facetName="%s"></div>\n' %
          xml_escape(self.facet.__regid__))
        w(u'<button data-toggle="dropdown" class="btn dropdown-toggle">'
          '%s<span class="caret"></span></button>' % title)
        cssclass = 'facetBody vocabularyFacet vocabularyFacetBody'
        w(u'<ul class="dropdown-menu %s">' % cssclass)
        for value, label, selected in self.items:
            if value is None:
                continue
            w(u'<li ><div class="facetValue facetCheckBox" cubicweb:value="%s">%s</div></li>'
              % (xml_escape(unicode(value)), label))
        w(u'</ul>\n')
        w(u'</div>\n')

class TextInputRangeWidget(facetbase.FacetRangeWidget):
    def _render(self):
        facet = self.facet
        onsubmit = (u"return cw.cubes.simplefacet.finalizeRangeFacet($(this), '%s')"
                    % normalize_facetid(self.facet.__regid__))
        with simplefacet_facetform(self, onsubmit):
            w = self.w
            facet = self.facet
            w(u'<div class="control-group">')
            w(u'<input class="input-small" type="text" id="%s-fromdate" placeholder="%s" />'
              % (facet.__regid__, facet._cw._('From')))
            w(u'<input class="input-small" type="text" id="%s-todate" placeholder="%s" />'
              % (facet.__regid__, facet._cw._('To')))
            w(u'<button type="submit" class="btn">%s</button>' % facet._cw._('facet_ok'))
            w(u'</div>')

class SimpleFacetStringWidget(facetbase.FacetStringWidget):
    def _render(self):
        onsubmit = (u"return cw.cubes.simplefacet.finalizeFtiSearch($(this), '%s')"
                    % normalize_facetid(self.facet.__regid__))
        with simplefacet_facetform(self, onsubmit):
            w = self.w
            w(u'<div class="control-group">')
            w(u'<input placeholder="%s" class="search-query input-medium" type="text" />\n'
              % self.facet._cw._('search ...'))
            w(u'<button type="submit" class="btn">%s</button>' % self.facet._cw._('facet_ok'))
            w(u'</div>')
