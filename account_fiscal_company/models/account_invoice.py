# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.addons.account_fiscal_company.decorator import \
    switch_company, \
    switch_company_period, \
    add_user_company


class account_invoice(Model):
    _inherit = 'account.invoice'

    def onchange_journal_id(
            self, cr, uid, ids, journal_id=False, context=None):
        res = super(account_invoice, self).onchange_journal_id(
            cr, uid, ids, journal_id=journal_id, context=context)
        if res.get('value', False):
            res['value'].pop('company_id', False)
        return res
