# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class CrmCaseSection(models.Model):
    _inherit = 'crm.case.section'

    def _default_company_id(self):
        return self.env['res.company'].browse(self.env.user._get_company())

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        default=_default_company_id)
