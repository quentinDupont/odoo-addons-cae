# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for l10n_fr Module for Odoo
#    Copyright (C) 2015-Today GRAP (http://www.grap.coop)
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
from openerp.osv.orm import TransientModel


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    # Columns Section
    _columns = {
        'siret': fields.char(
            'SIRET', size=64),
    }

    # View Section
    def onchange_type_mother_company(
            self, cr, uid, ids, type, mother_company, context=None):
        rc_obj = self.pool['res.company']
        res = super(
            res_company_create_wizard, self).onchange_type_mother_company(
            cr, uid, ids, type, mother_company, context=context)
        if type and mother_company and type == 'integrated':
            rc = rc_obj.browse(cr, uid, mother_company, context=context)
            if rc.siret:
                res['value']['siret'] = rc.siret + ' XX'
        else:
            res['value']['siret'] = ''
        return res

    # Overload Section
    def res_company_values(self, cr, uid, id, context=None):
        res = super(res_company_create_wizard, self).res_company_values(
            cr, uid, id, context=context)
        rccw = self.browse(cr, uid, id, context=context)
        res.update({
            'siret': rccw.siret,
        })
        return res
