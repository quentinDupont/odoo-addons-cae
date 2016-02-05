# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _


class ProductTemplate(Model):
    _inherit = 'product.template'

    # Columns Section
    _columns = {
        'administrative_ok': fields.boolean(
            string='Is Administrative', select=True,
            help="If checked, this product will be readonly for users and"
            " updatable only by specific group"
        ),
    }

    # Constraint Section
    def _check_administrative_access(self, cr, uid, ids, context=None):
        ru_obj = self.pool['res.users']
        if not ru_obj.has_group(
                cr, uid,
                'base_fiscal_company.res_group_administrative_manager'):
            template_vals = self.read(
                cr, uid, ids, ['administrative_ok'], context=context)
            return any(x['administrative_ok'] for x in template_vals)
        return True

    _constraints = [
        (
            _check_administrative_access,
            "Error: You have no right to create or update an"
            " administrative product", []),
    ]

    # Overload Section
    def unlink(self, cr, uid, ids, context=None):
        if self._check_administrative_access(cr, uid, ids, context=context):
            return super(ProductTemplate, self).unlink(
                cr, uid, ids, context=context)
        else:
            raise osv.except_osv(_('Error !'), _(
                "Error: You have no right to delete an administrative"
                " product"))
