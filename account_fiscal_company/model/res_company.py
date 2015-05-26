# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import Model
from openerp.addons.account_fiscal_company.account_parameters \
    import propagate_properties_to_new_fiscal_child


class ResCompany(Model):
    _inherit = 'res.company'

    def create(self, cr, uid, vals, context=None):
        pc_obj = self.pool['product.category']
        res = super(ResCompany, self).create(
            cr, uid, vals, context=context)
        if vals.get('fiscal_type') == 'fiscal_child':
            # Apply all product category properties to the new company
            for property_name in pc_obj._PRODUCT_CATEGORY_FISCAL_PROPERTY_LIST:
                propagate_properties_to_new_fiscal_child(
                    self.pool, cr, uid,
                    vals.get('fiscal_company'),
                    res,
                    'product.category',
                    property_name,
                    context=context)
        return res