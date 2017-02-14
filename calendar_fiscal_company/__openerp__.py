# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Calendar Module',
    'version': '8.0.1.0.0',
    'category': 'CAE',
    'summary': 'Manage CAE for Calendar module',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'calendar',
    ],
    'data': [
        'views/view_calendar_event.xml',
        'security/ir_rule.xml',
    ],
    'installable': True,
    'auto_install': True,
}
