# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CIS - Barcodes Fiscal Company',
    'version': '1.0',
    'category': 'CIS',
    'description': """

=======================================================
Specific option for Fiscal Company and Barcodes modules
=======================================================

* Add company_id on the following models:
    * barcode.rule
    * barcode.nomenclature

Roadmaps
--------

* Create new barcode nomenclature, when a new company is created.

Copyright, Author and Licence
-----------------------------

* Copyright : 2013-Today, Groupement Régional Alimentaire de Proximité;
* Author :
    * Sylvain LE GAL (https://twitter.com/legalsylvain);
* Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'base_fiscal_company',
        'barcodes',
    ],
    'data': [
        'security/ir_rule.xml',
        'views/view_barcode_nomenclature.xml',
        'views/view_barcode_rule.xml',
    ],
    'installable': True,
    'auto_install': True,
}
