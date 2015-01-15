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
from openerp.tools.translate import _


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    # Overload Section
    def begin(self, cr, uid, id, context=None):
        ss_obj = self.pool['sale.shop']
        res = super(res_company_create_wizard, self).begin(
            cr, uid, id, context=context)
        rccw = self.browse(cr, uid, id, context=context)

        # Create Sale Shop
        ss_obj.create(cr, uid, {
            'name': _('%s - Shop') % (rccw.code),
            'warehouse_id': res['warehouse_id'],
            'payment_default_id': res['payment_term_id'],
            'pricelist_id': res['public_pricelist_id'],
            'company_id': rccw.company_id.id,
        }, context=context)

        return res
