# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - Calendar Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'description': """
Specific Settings for Cooperative and Calendar Module
=====================================================

Multi Company Settings
----------------------

TODO
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'base_calendar',
    ],
    'data': [
        'views/view_calendar_event.xml',
        'views/view_crm_meeting.xml',
        'views/view_crm_meeting_type.xml',
        'security/ir_rule.xml',
    ],
    'auto_install': True,
}
