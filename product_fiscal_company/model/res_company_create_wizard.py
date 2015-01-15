# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Product Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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

from openerp.osv.orm import TransientModel
from openerp.tools.translate import _


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    def begin(self, cr, uid, id, context=None):
        ip_obj = self.pool['ir.property']
        imd_obj = self.pool['ir.model.data']
        pp_obj = self.pool['product.pricelist']
        ppv_obj = self.pool['product.pricelist.version']
        ppi_obj = self.pool['product.pricelist.item']

        res = super(res_company_create_wizard, self).begin(
            cr, uid, id, context=context)

        rccw = self.browse(cr, uid, id, context=context)

        # creating Sale Pricelist
        pp_id = pp_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist') % (rccw.code),
            'currency_id': rccw.company_id.currency_id.id,
            'type': 'sale',
            'company_id': rccw.company_id.id,
        }, context=context)

        ppv_id = ppv_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist Version') % (rccw.code),
            'pricelist_id': pp_id,
        }, context=context)

        ppi_obj.create(cr, uid, {
            'name': _('%s - Default Public Pricelist Line') % (rccw.code),
            'price_version_id': ppv_id,
            'base': 1,
        }, context=context)

        # Create Properties
        ip_obj.create(cr, uid, {
            'name': 'property_product_pricelist',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'product',
                'field_res_partner_property_product_pricelist')[1],
            'type': 'many2one',
            'value_reference': 'product.pricelist,%s' % (pp_id),
        }, context=context)

        res.update({
            'public_pricelist_id': pp_id,
        })
        return res
