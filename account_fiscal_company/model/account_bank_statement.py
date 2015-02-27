# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
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

from openerp.osv.orm import Model
from openerp.osv import fields


class account_bank_statement(Model):
    _name = 'account.bank.statement'
    _inherit = 'account.bank.statement'

    _columns = {
        'company_id': fields.many2one('res.company',
                                      string='Company',
                                      required=True)
    }

    def _check_company_id(self, cr, uid, ids, context=None):
        for statement in self.browse(cr, uid, ids, context=context):
            if (statement.company_id.fiscal_company !=
                    statement.period_id.company_id.fiscal_company):
                return False
        return True

    _constraints = [
        (_check_company_id, 'The journal and period chosen have \
        to belong to the same company.', ['journal_id', 'period_id']),
    ]
