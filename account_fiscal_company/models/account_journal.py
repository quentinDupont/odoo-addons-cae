# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today: GRAP (http://www.grap.coop)
# @author:
#    Julien WESTE
#    Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.addons.account_fiscal_company.decorator import \
    switch_company


class account_journal(Model):
    _inherit = 'account.journal'

    @switch_company
    def search(
            self, cr, user, args, offset=0, limit=None, order=None,
            context=None, count=False):
        return super(account_journal, self).search(
            cr, user, args, offset=offset, limit=limit, order=order,
            context=context, count=count)
