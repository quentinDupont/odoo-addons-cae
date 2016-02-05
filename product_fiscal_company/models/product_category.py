# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from openerp.osv.orm import Model
from openerp.osv import fields


class ProductCategory(Model):
    _inherit = 'product.category'

    # Overload Section
    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False):
        """Add a required modifiers on the field code"""
        res = super(ProductCategory, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar)
        if view_type in ('form', 'tree')\
                and 'code' in res['fields']:
            res['fields']['required'] = True
            doc = etree.XML(res['arch'])
            node = doc.xpath("//field[@name='code']")[0]
            node.set('modifiers', '{"required": true}')
            res['arch'] = etree.tostring(doc)
        return res

    # Columns Section
    _columns = {
        'code': fields.char(
            string='Code', size=3, help="This field is used as a prefix to"
            " generate automatic and unique reference for items"
            " (product, ...).\n"
            "Warning, changing this value will change the reference of all"
            " items of this category.",
        ),
    }
