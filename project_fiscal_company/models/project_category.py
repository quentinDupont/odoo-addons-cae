# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProjectCategory(models.Model):
    _inherit = 'project.category'

    def _default_company_id(self):
        return self.env.user.company_id

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company',
        default=_default_company_id)
