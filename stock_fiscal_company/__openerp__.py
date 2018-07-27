# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# @author: Julien WESTE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'CIS - Stock Fiscal Company',
    'version': '8.0.2.0.0',
    'category': 'CIS',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'stock',
    ],
    'demo': [
        'demo/stock_location.xml',
        'demo/stock_warehouse.xml',
        'demo/res_groups.xml',
    ],
    'data': [
        'security/ir_rule.xml',
        'views/view_procurement_rule.xml',
        'views/view_res_company_create_wizard.xml',
        'views/view_stock_location.xml',
        'views/view_stock_location_route.xml',
        'views/view_stock_picking_type.xml',
        'views/view_stock_warehouse.xml',
        'views/view_stock_warehouse_orderpoint.xml',

    ],
    'installable': True,
    'auto_install': True,
}
