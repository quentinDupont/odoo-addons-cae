# coding: utf-8
# Copyright (C) 2017-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp import api, fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    # Column Section
    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        store=True, related='warehouse_id.company_id')

    # Overload Section
    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form', toolbar=False,
            submenu=False):
        """Add a required modifiers on the field company_id"""
        res = super(StockPickingType, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type in ('form', 'tree')\
                and 'company_id' in res['fields']:
            res['fields']['company_id']['required'] = True
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='company_id']")[0]
            node.set('modifiers', '{"required": true}')
            res['arch'] = etree.tostring(doc)
        return res
