# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Base Module for Odoo
#    Copyright (C) 2013-2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv import fields
from openerp.osv.orm import Model

_RES_COMPANY_FISCAL_TYPE = [
    ('normal', 'Normal'),
    ('fiscal_mother', 'Fiscal Mother Company'),
    ('fiscal_child', 'Fiscal Child Company'),
]


class res_company(Model):
    _inherit = 'res.company'

    # Private function section
    def _propagate_access_right(self, cr, uid, ids, context=None):
        args = [('id', 'in', ids), ('fiscal_type', '=', 'fiscal_child')]
        rc_ids = self.search(cr, uid, args, context=context)
        for rc in self.browse(cr, uid, rc_ids, context=context):
            ru_ids = [ru.id for ru in rc.fiscal_company.user_ids]
            ru_new_ids = list(set(ru_ids) - set(rc.user_ids))
            self.write(cr, uid, [rc.id], {
                'user_ids': [(4, id) for id in list(set(ru_new_ids))]},
                context=context)

    # Columns Section
    _columns = {
        'fiscal_type': fields.selection(
            _RES_COMPANY_FISCAL_TYPE, 'Fiscal Type', required=True),
        'fiscal_company': fields.many2one(
            'res.company', 'Fiscal Company'),
        'fiscal_childs': fields.one2many(
            'res.company', 'fiscal_company', 'Fiscal Childs', readonly=True),
    }

    _defaults = {
        'fiscal_type': 'normal',
    }

    # Constraint Function Section
    def _check_non_fiscal_child_company(self, cr, uid, ids, context=None):
        for rc in self.browse(cr, uid, ids, context=context):
            # skip special case of creation
            if rc.fiscal_company:
                if (rc.fiscal_type in ('normal', 'fiscal_mother')
                        and rc.id != rc.fiscal_company.id):
                    return False
        return True

    def _check_fiscal_mother_company(self, cr, uid, ids, context=None):
        for rc in self.browse(cr, uid, ids, context=context):
            # skip special case of creation
            if rc.fiscal_company is not None:
                if (rc.fiscal_type == 'fiscal_child'
                        and rc.fiscal_company.fiscal_type != 'fiscal_mother'):
                    return False
        return True

    # Constraint Section
    _constraints = [
        (_check_non_fiscal_child_company,
            "You can't select an other company for a Non Fiscal Child Company",
            ['fiscal_company', 'fiscal_type']),
        (_check_fiscal_mother_company,
            "Please select a Fiscal Mother Company for a Fiscal Child Company",
            ['fiscal_company', 'fiscal_type']),
    ]

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        company_id = super(res_company, self).create(
            cr, uid, vals, context=context)
        if not vals.get('fiscal_company', False):
            self.write(cr, uid, [company_id], {
                'fiscal_company': company_id}, context=context)
        elif vals.get('fiscal_type', False) == 'fiscal_child':
            self._propagate_access_right(
                cr, uid, [company_id], context=context)
        return company_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(res_company, self).write(
            cr, uid, ids, vals, context=context)
        if vals.get('fiscal_company', False):
            self._propagate_access_right(cr, uid, ids, context=context)
        return res
