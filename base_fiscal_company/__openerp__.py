# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Base Module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'CIS - Base Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'summary': 'Manage the concept of fiscal company',
    'description': """
Manage the concept of fiscal company
====================================
Features :
----------
    * Add field 'fiscal_company' and 'fiscal_type' in the table res_company;
    * A company can be 'normal', 'fiscal_mother' or 'fiscal_child' ;
    * If a user has access rights to a 'fiscal_mother' so he has access"""
    """rights to all 'fiscal_child' companies;

Copyright, Author and Licence :
-------------------------------
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
        'view/view.xml',
        'view/action.xml',
        'view/menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
        'demo/res_groups.yml',
    ],
}
