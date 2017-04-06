# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CAE - Base Module',
    'version': '8.0.1.0.0',
    'category': 'CAE',
    'summary': 'Manage Cooperatives of Activities and Employment',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'sales_team_fiscal_company',
        'crm',
    ],
    'data': [
        'views/view_crm_case_categ.xml',
        'views/view_crm_tracking_medium.xml',
        'views/view_crm_tracking_campaign.xml',
        'views/view_crm_case_stage.xml',
        'views/view_crm_phonecall.xml',
        'security/ir_rule.xml',
    ],
    'installable': True,
    'auto_install': True,
}
