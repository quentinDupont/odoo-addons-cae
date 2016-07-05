# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class CrmCaseCateg(models.Model):
    _inherit = 'crm.case.categ'

    company_id = fields.Many2one(
        comodel_name='res.company', string='Company', readonly=True,
        related='section_id.company_id', store=True)
