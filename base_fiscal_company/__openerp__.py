# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - Base Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'summary': 'Manage the concept of fiscal company',
    'description': """
Manage the concept of fiscal company
====================================
Features
--------

* Add field 'fiscal_company' and 'fiscal_type' in the table res_company;
* A company can be 'normal', 'fiscal_mother' or 'fiscal_child' ;
* If a user has access rights to a 'fiscal_mother' so he has access
  rights to all 'fiscal_child' companies;

Limits / Roadmaps / TODO
------------------------
* Created partner from users / companies, must be disabled by default.
  (maybe create a new module for that feature)

Copyright, Author and Licence
-----------------------------
    * Copyright : 2013, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir_rule.xml',
        'security/res_groups.yml',
        'views/action.xml',
        'views/menu.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/res_company_create_wizard_view.xml',
    ],
    'demo': [
        'demo/demo.xml',
        'demo/res_users.yml',
        'demo/res_groups.yml',
    ],
}
