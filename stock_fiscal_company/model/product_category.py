# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Stock Module for Odoo
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


class product_category(Model):
    _inherit = 'product.category'

    def init(self, cr):
        print "===================== COINCOIN"
        self._PRODUCT_CATEGORY_FISCAL_PROPERTY_LIST.extend([
            'property_stock_journal',
            'property_stock_account_input_categ',
            'property_stock_account_output_categ',
            'property_stock_valuation_account_id',
        ])
