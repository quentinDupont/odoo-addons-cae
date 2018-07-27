# coding: utf-8
# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model


class product_category(Model):
    _inherit = 'product.category'

    def init(self, cr):
        self._PRODUCT_CATEGORY_FISCAL_PROPERTY_LIST.extend([
            'property_stock_journal',
            'property_stock_account_input_categ',
            'property_stock_account_output_categ',
            'property_stock_valuation_account_id',
        ])
