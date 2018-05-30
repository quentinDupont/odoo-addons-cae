# coding: utf-8
# Copyright (C) 2015 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import TransientModel


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    def res_groups_values(self, cr, uid, context=None):
        res = super(res_company_create_wizard, self).res_groups_values(
            cr, uid, context=context)
        res.append('point_of_sale.group_pos_manager')
        return res
