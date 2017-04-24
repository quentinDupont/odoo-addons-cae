# -*- coding: utf-8 -*-
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'CIS - Stock Fiscal Company',
    'version': '1.1',
    'category': 'CIS',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'account_fiscal_company',
        'stock',
    ],
    'demo': [
        'demo/stock_location.xml',
        'demo/stock_warehouse.xml',
    ],
    'data': [
        'security/ir_rule.xml',
        'view/view.xml',
        'view/view_stock_picking_type.xml',
    ],
    'installable': True,
    'auto_install': True,
}
