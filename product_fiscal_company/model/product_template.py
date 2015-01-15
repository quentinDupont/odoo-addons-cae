# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Product Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _


class product_template(Model):
    _inherit = 'product.template'

    # Columns Section
    _columns = {
        'administrative_ok': fields.boolean(
            'Is Administrative', select=1,
            help="""If checked, this product will be readonly for users and"""
            """ updatable only by specific group"""
        ),
    }

    def _check_administrative_access(self, cr, uid, ids, context=None):
        ru_obj = self.pool['res.users']
        if not ru_obj.has_group(
                cr, uid,
                'base_fiscal_company.res_group_administrative_manager'):
            for pp in self.browse(cr, uid, ids, context=context):
                if pp.administrative_ok:
                    return False
        return True

    _constraints = [
        (
            _check_administrative_access,
            """Error: You have no right to create or update an"""
            """ administrative product""",
            []),
    ]

    # Overwrite Section
    def unlink(self, cr, uid, ids, context=None):
        if self._check_administrative_access(cr, uid, ids, context=context):
            return super(product_template, self).unlink(
                cr, uid, ids, context=context)
        else:
            raise osv.except_osv(_('Error !'), _(
                """Error: You have no right to delete an administrative"""
                """ product"""))
