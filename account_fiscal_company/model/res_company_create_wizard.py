# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Stock Module for Odoo
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


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    # Overload Section
    def begin(self, cr, uid, id, context=None):
        imd_obj = self.pool['ir.model.data']
        res = super(res_company_create_wizard, self).begin(
            cr, uid, id, context=context)
        print "account_fiscal_company"
        print res

        # Define Payment Term. (Static for the moment)
        payment_term_id = imd_obj.get_object_reference(
            cr, uid, 'account', 'account_payment_term_immediate')[1]

        res.update({
            'payment_term_id': payment_term_id,
            })
        return res

    def finish(self, cr, uid, id, context=None):
        res = super(res_company_create_wizard, self).finish(
            cr, uid, id, context=context)

        # Create Account Property based on
        # account_receivable
        # account_payable
        # account_expense_categ
        # account_income_categ
        # stock_account_input
        # stock_account_output
        # stock_account_input_categ
        # stock_account_output_categ
        # property_stock_journal

        return res
