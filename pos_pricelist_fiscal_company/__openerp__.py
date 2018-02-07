# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - PoS Pricelist Fiscal Company',
    'version': '1.1',
    'category': 'CIS',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'pos_pricelist',
    ],
    'data': [
        'security/ir_rule.xml',
    ],
    'installable': True,
    'auto_install': True,
}
