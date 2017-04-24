# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models
from openerp.exceptions import Warning


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _get_domain_locations(self):
        return super(ProductProduct, self.with_context(
            force_company=self.env.user.company_id.id,
            compute_child=False))._get_domain_locations()
