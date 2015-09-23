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
from openerp.addons.account_fiscal_company.decorator import \
    switch_company, \
    switch_company_period, \
    add_user_company


class account_period(Model):
    _inherit = 'account.period'

    @switch_company_period
    def find(self, cr, uid, dt=None, context=None):
        return super(account_period, self).find(
            cr, uid, dt=dt, context=context)


class account_fiscalyear(Model):
    _inherit = 'account.fiscalyear'

    @switch_company_period
    def find(self, cr, uid, dt=None, exception=True, context=None):
        return super(account_fiscalyear, self).find(
            cr, uid, dt=dt, exception=exception, context=context)


class account_move(Model):
    _inherit = 'account.move'

    _columns = {
        'company_id': fields.many2one(
            'res.company', string='Company', required=True)
    }


class account_journal(Model):
    _inherit = 'account.journal'

    @switch_company
    def search(
            self, cr, user, args, offset=0, limit=None, order=None,
            context=None, count=False):
        return super(account_journal, self).search(
            cr, user, args, offset=offset, limit=limit, order=order,
            context=context, count=count)


class account_account(Model):
    _inherit = 'account.account'

    @switch_company
    def search(
            self, cr, uid, args, offset=0, limit=None,
            order=None, context=None, count=False):
        return super(account_account, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    @add_user_company
    def compute(
            self, cr, uid, ids, field_names, arg=None, context=None, query='',
            query_params=()):
        return super(account_account, self).__compute(
            cr, uid, ids=ids, field_names=field_names, arg=arg,
            context=context, query=query, query_params=query_params)


class account_invoice(Model):
    _inherit = 'account.invoice'

    def onchange_journal_id(
            self, cr, uid, ids, journal_id=False, context=None):
        res = super(account_invoice, self).onchange_journal_id(
            cr, uid, ids, journal_id=journal_id, context=context)
        return True
        if res.get('value', False):
            res['value'].pop('company_id', False)
        return res
