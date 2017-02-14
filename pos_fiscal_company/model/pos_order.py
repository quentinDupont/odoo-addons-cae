# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def _create_account_move_line(self, session=None, move_id=None):
        """Disable bad force_company, present in the function
        _confirm_orders function
        """
        if len(self):
            res = super(PosOrder, self.with_context(
                force_company=self[0].company_id.id)).\
                _create_account_move_line(
                    session=session, move_id=move_id)
        else:
            res = super(PosOrder, self)._create_account_move_line(
                session=session, move_id=move_id)
        return res
