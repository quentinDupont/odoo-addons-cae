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

import string
from random import *

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class res_company_create_wizard(TransientModel):
    _name = 'res.company.create.wizard'

    _PASSWORD_SIZE = 8

    _COMPANY_TYPE = [
        ('integrated', 'Integrated Company'),
        ('associated', 'Associated Company'),
    ]

    _columns = {
        'state': fields.selection(
            [('init', 'init'), ('done', 'done')], 'Status', readonly=True),
        'name': fields.char('Name', required=True, size=128),
        'mother_company': fields.many2one(
            'res.company', 'Mother Company', required=True,
            domain="[('fiscal_type', '!=', 'fiscal_child')]"),
        'vat': fields.char(
            'Tax ID', size=32),
        'type': fields.selection(
            _COMPANY_TYPE, 'Type', required=True),
        'code': fields.char(
            'Code', size=3, required=True,
            help="""This field is used as a prefix to generate automatic and"""
            """ unique reference for items (product, ...)."""
            """Warning, changing this value will change the reference of all"""
            """ items of this company.""",
        ),
        'password': fields.char(
            'Password', size=_PASSWORD_SIZE, readonly=True),
    }

    # Default Section
    _defaults = {
        'state': 'init',
    }

    # Constraint Section
    def _check_mother_company(self, cr, uid, ids, context=None):
        for rccw in self.browse(cr, uid, ids, context=context):
            if rccw.type == 'integrated':
                if rccw.mother_company.fiscal_type != 'fiscal_mother':
                    return False
            if rccw.type == 'associated':
                if (rccw.mother_company.fiscal_type != 'normal'
                        or rccw.mother_company.parent_id):
                    return False
        return True

    _constraints = [
        (
            _check_mother_company,
            """Error on Mother Company: Please select a normal Parent"""
            """ Company if the company is 'associated' and and a Fiscal"""
            """ Mother Company, if the company is 'integrated'""",
            ['type', 'mother_company']),
    ]

    # View Section
    def validate(self, cr, uid, ids, context=None):
        rccw = self.browse(cr, uid, ids, context=context)[0]
        rc_obj = self.pool['res.company']
        ru_obj = self.pool['res.users']
        # Create Company
        vals = {
            'name': rccw.name,
            'code': rccw.code,
            'parent_id': rccw.mother_company.id,
            }
        if rccw.type == 'integrated':
            vals['vat'] = rccw.mother_company.vat
            vals['fiscal_type'] = 'fiscal_child'
            vals['fiscal_company'] = rccw.mother_company.id
            vals['rml_header'] = rccw.mother_company.rml_header
        else:
            vals['vat'] = rccw.vat
            vals['fiscal_type'] = 'normal'
            vals['fiscal_company'] = False
        rc_id = rc_obj.create(cr, uid, vals, context=context)

        characters = string.ascii_letters + string.digits
        password = "".join(choice(characters) for x in range(8))
        # Create Generic User
        ru_obj.create(cr, uid, {
            'name': rccw.name,
            'login': rccw.code,
            'new_password': password,
            'company_id': rc_id,
            'company_ids': [(4, rc_id)],
        }, context=context)

        self.write(cr, uid, ids, {
            'state': 'done',
            'password': password}, context=context)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.company.create.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': rccw.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
