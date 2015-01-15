# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Product Module for Odoo
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
    'name': 'CIS - Product Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'summary': 'Glue Module between CIS and product',
    'description': """
Glue Module between CIS and product
===================================

Features :
----------
    * company_id is now mandatory on product_product;
    * user in mother company can see product of all child company;
    * user in fiscal company can see but not update / delete product
      of mother company;
    * Add a field 'is_administrative' on product.product; if checked the
      product will not be updatable by basic users;

Technical Information:
----------------------
    * After installing this module, please fill correctly the field"""
    """'company_id' in the table 'product_product';

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
        'product',
        'base_fiscal_company',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'security/ir_rule.xml',
        'view/view.xml',
    ],
    'auto_install': True,
}
