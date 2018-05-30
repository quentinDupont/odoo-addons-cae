# coding: utf-8
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Overide Section
    @api.multi
    def _check_company_journal(self):
        # Sale Journal can belong to another company
        return True

    @api.multi
    def _check_company_payment(self):
        # Payment Journals can belong to another company
        return True

    _constraints = [
        (_check_company_journal, "Disabled.", ['company_id', 'journal_id']),
        (_check_company_payment, "Disabled.", ['company_id', 'journal_ids']),
    ]
