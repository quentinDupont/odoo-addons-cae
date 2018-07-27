# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'CIS - Purchase Fiscal Company',
    'version': '1.1',
    'category': 'CIS',
    'description': """
Manage specific account move for cooperative
============================================

Features :
----------
    * TODO;

TODO :
------
    * Update the description of this module;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014-Today, Groupement Régional Alimentaire de Proximité;
    * Author : Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'stock_fiscal_company',
        'purchase',
    ],
    'data': [
        'views/view_purchase_order.xml',
    ],
    'installable': True,
    'auto_install': True,
}
