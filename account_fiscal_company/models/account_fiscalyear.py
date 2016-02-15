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


class account_fiscalyear(Model):
    _inherit = 'account.fiscalyear'

    @switch_company_period
    def find(self, cr, uid, dt=None, exception=True, context=None):
        return super(account_fiscalyear, self).find(
            cr, uid, dt=dt, exception=exception, context=context)
