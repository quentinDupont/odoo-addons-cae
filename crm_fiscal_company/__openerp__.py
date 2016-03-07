# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - CRM Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'description': """
Specific Settings for Cooperative and CRM Module
================================================

Multi Company Settings
----------------------

TODO
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'crm',
    ],
    'data': [
        'views/view_crm_case_categ.xml',
        'views/view_crm_case_channel.xml',
        'views/view_crm_case_resource_type.xml',
        'views/view_crm_case_section.xml',
        'views/view_crm_case_stage.xml',
        'views/view_crm_phonecall.xml',
        'security/ir_rule.xml',
    ],
    'auto_install': True,
}
