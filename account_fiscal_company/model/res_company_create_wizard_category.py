# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
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

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class ResCompanyCreateWizardCategory(TransientModel):
    _name = 'res.company.create.wizard.category'

    # Columns Section
    _columns = {
        'wizard_id': fields.many2one(
            'res.company.create.wizard', 'Wizard'),
        'company_id': fields.related(
            'wizard_id', 'company_id', type='many2one',
            string='Company', relation='res.company'),
        'category_id': fields.many2one(
            'product.category', 'Category'),
        'expense_account_id': fields.many2one(
            'account.account', 'Expense Account',
            domain="[('company_id', '=', company_id),"
            "('type', '=', 'other')]"),
        'income_account_id': fields.many2one(
            'account.account', 'Income Account',
            domain="[('company_id', '=', company_id),"
            "('type', '=', 'other')]"),
    }
