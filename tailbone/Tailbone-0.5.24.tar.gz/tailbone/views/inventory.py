# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2016 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Views for inventory batches
"""

from __future__ import unicode_literals, absolute_import

from rattail.db.batch.inventory.handler import InventoryBatchHandler

import formalchemy as fa
from webhelpers.html import tags

from tailbone import forms
from tailbone.views.batch import BatchMasterView

from dtail.db import model


class HandheldBatchFieldRenderer(fa.FieldRenderer):
    """
    Renderer for inventory batch's "handheld batch" field.
    """

    def render_readonly(self, **kwargs):
        batch = self.raw_value
        if batch:
            return tags.link_to(
                batch.id_str,
                self.request.route_url('batch.handheld.view', uuid=batch.uuid))
        return ''


class InventoryBatchView(BatchMasterView):
    """
    Master view for inventory batches.
    """
    model_class = model.InventoryBatch
    model_title_plural = "Inventory Batches"
    batch_row_class = model.InventoryBatchRow
    batch_handler_class = InventoryBatchHandler
    route_prefix = 'batch.inventory'
    url_prefix = '/batch/inventory'
    creatable = False

    def configure_fieldset(self, fs):
        fs.configure(
            include=[
                fs.id,
                fs.created,
                fs.created_by,
                fs.handheld_batch.with_renderer(HandheldBatchFieldRenderer),
                fs.executed,
                fs.executed_by,
            ])
        if not self.viewing:
            del fs.handheld_batch

    def configure_row_grid(self, g):
        g.configure(
            include=[
                g.sequence,
                g.upc.label("UPC"),
                g.brand_name.label("Brand"),
                g.description,
                g.size,
                g.cases,
                g.units,
                g.status_code.label("Status"),
            ],
            readonly=True)

    def row_grid_row_attrs(self, row, i):
        attrs = {}
        if row.status_code == row.STATUS_PRODUCT_NOT_FOUND:
            attrs['class_'] = 'warning'
        return attrs

    @classmethod
    def defaults(cls, config):

        # fix permission group title
        config.add_tailbone_permission_group('batch.inventory', "Inventory Batches")

        cls._batch_defaults(config)
        cls._defaults(config)


def includeme(config):
    InventoryBatchView.defaults(config)
