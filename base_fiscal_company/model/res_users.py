# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Base Module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
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

from openerp.osv.orm import Model


class res_users(Model):
    _inherit = 'res.users'

    # Private function section
    def _propagate_access_right(self, cr, uid, ids, context=None):
        """If a user has access to a fiscal_mother company, so he'll have
        access to all the child_company"""
        rc_new_ids = []
        for ru in self.browse(cr, uid, ids, context=context):
            for rc in ru.company_ids:
                if rc.fiscal_type == 'fiscal_mother':
                    rc_all_ids = [
                        x.id for x in rc.fiscal_company.fiscal_childs]
                    rc_existing_ids = [
                        x.id for x in ru.company_ids]
                    rc_new_ids += (
                        list(set(rc_all_ids) - set(rc_existing_ids)))
            super(res_users, self).write(cr, uid, [ru.id], {
                'company_ids': [(4, id) for id in list(set(rc_new_ids))]},
                context=context)

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        user_id = super(res_users, self).create(cr, uid, vals, context=context)
        if vals.get('company_ids', False):
            self._propagate_access_right(cr, uid, [user_id], context=context)
        return user_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        if vals.get('company_ids', False):
            self._propagate_access_right(cr, uid, ids, context=context)
        return res
