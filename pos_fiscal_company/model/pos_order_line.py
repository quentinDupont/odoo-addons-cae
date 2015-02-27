# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Point Of Sale Module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
from openerp.osv import fields


class pos_order_line(Model):
    _inherit = 'pos.order.line'

    def _amount_line_all(self, cr, uid, ids, field_names, arg, context=None):
        res = dict([(i, {}) for i in ids])
        account_tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids, context=context):
            taxes_ids = [
                tax for tax in line.product_id.taxes_id if (
                    tax.company_id.id == line.order_id.company_id.id or
                    (tax.company_id.id ==
                        line.order_id.company_id.fiscal_company.id))]
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = account_tax_obj.compute_all(
                cr, uid, taxes_ids, price, line.qty, product=line.product_id,
                partner=line.order_id.partner_id or False)

            cur = line.order_id.pricelist_id.currency_id
            res[line.id]['price_subtotal'] = cur_obj.round(
                cr, uid, cur, taxes['total'])
            res[line.id]['price_subtotal_incl'] = cur_obj.round(
                cr, uid, cur, taxes['total_included'])
        return res

    _columns = {
        'price_subtotal': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Subtotal w/o Tax', store=True),
        'price_subtotal_incl': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Subtotal', store=True),
    }
