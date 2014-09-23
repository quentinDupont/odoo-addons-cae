# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Mail Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
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
    'name': 'CIS - Mail Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'description': """
Manage the concept of fiscal company if Mail module is installed
================================================================
Features :
----------
    * Add a default value:
        * Model: 'res.partner';
        * Field : 'notification_email_send';
        * Value : 'comment';

Technical Information:
----------------------
    * The default value is added to allow test in base_fiscal_company, when
    tests create partners, because there is now default value for this
    mandatory field;

Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Author :
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mail',
        'base_fiscal_company',
    ],
    'data': [
        'data/ir_values.yml',
    ],
    'auto_install': True,
}
