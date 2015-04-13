# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
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

from openerp.osv import fields
from openerp.osv.orm import TransientModel


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    def _get_journal_ids(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        aj_obj = self.pool['account.journal']
        for rccw in self.browse(cr, uid, ids, context=context):
            if rccw.company_id and rccw.type in ['associated']:
                res[rccw.id] = aj_obj.search(cr, uid, [
                    ('company_id', '=', rccw.company_id.id)], context=context)
            else:
                res[rccw.id] = []
        return res

    # Columns Section
    _columns = {
        'chart_template_id': fields.many2one(
            'account.chart.template', 'Account Template',
            domain="[('visible', '=', True)]"),
        'journal_ids': fields.function(
            _get_journal_ids, 'Journals', type='one2many',
            relation='account.journal'),
        'code_digits': fields.integer(
            '# of Digits',
            help="No. of digits to use for account code"),
        'complete_tax_set': fields.boolean('Complete set of taxes'),
        'sale_tax': fields.many2one(
            'account.tax.template', 'Default sale tax'),
        'purchase_tax': fields.many2one(
            'account.tax.template', 'Default purchase tax'),
        'sale_tax_rate': fields.float(
            'Sales tax (%)'),
        'purchase_tax_rate': fields.float(
            'Purchase tax (%)'),
        'account_receivable_id': fields.many2one(
            'account.account', 'Account Receivable',
            domain="[('company_id', '=', fiscal_company),"
            "('type', '=', 'receivable')]"),
        'account_payable_id': fields.many2one(
            'account.account', 'Account Payable',
            domain="[('company_id', '=', fiscal_company),"
            "('type', '=', 'payable')]"),
    }

    # account_payable
    # account_expense_categ
    # account_income_categ
    # stock_account_input
    # stock_account_output
    # stock_account_input_categ
    # stock_account_output_categ
    # property_stock_journal

    # Constraint Section
    def _check_account_setting(self, cr, uid, ids, context=None):
        for rccw in self.browse(cr, uid, ids, context=context):
            if rccw.type == 'associated':
                if not rccw.chart_template_id:
                    return False
        return True

    _constraints = [
        (
            _check_account_setting,
            """You have to set a chart template if you try to create an"""
            """ associated company""",
            ['type', 'chart_template_id']),
    ]

    # Overload Section
    def res_groups_values(self, cr, uid, context=None):
        res = super(res_company_create_wizard, self).res_groups_values(
            cr, uid, context=context)
        res.append('account.group_account_user')
        return res

    def res_company_values(self, cr, uid, id, context=None):
        res = super(res_company_create_wizard, self).res_company_values(
            cr, uid, id, context=context)
        rccw = self.browse(cr, uid, id, context=context)
        res.update({
            'expects_chart_of_accounts': rccw.type in ['associated'],
        })
        return res

    def begin(self, cr, uid, id, context=None):
        imd_obj = self.pool['ir.model.data']
        res = super(res_company_create_wizard, self).begin(
            cr, uid, id, context=context)
        rccw = self.browse(cr, uid, id, context=context)

        # Define Payment Term. (Static for the moment)
        payment_term_id = imd_obj.get_object_reference(
            cr, uid, 'account', 'account_payment_term_immediate')[1]

        # Install Chart of Accounts
        if rccw.type in ('associated'):
            wmca_obj = self.pool['wizard.multi.charts.accounts']
            wmca_id = wmca_obj.create(cr, uid, {
                'company_id': rccw.company_id.id,
                'chart_template_id': rccw.chart_template_id.id,
                'code_digits': rccw.code_digits,
                'sale_tax': rccw.sale_tax.id,
                'sale_tax_rate': rccw.sale_tax_rate,
                'purchase_tax': rccw.purchase_tax.id,
                'purchase_tax_rate': rccw.purchase_tax_rate,
                'complete_tax_set': rccw.chart_template_id.complete_tax_set,
                'currency_id': rccw.company_id.currency_id.id,
            }, context)
            wmca_obj.execute(cr, uid, [wmca_id], context)

#                name = code = config.date_start[:4]
#                if int(name) != int(config.date_stop[:4]):
#                    name = config.date_start[:4] +'-'+ config.date_stop[:4]
#                    code = config.date_start[2:4] +'-'+ config.date_stop[2:4]
#                vals = {
#                    'name': name,
#                    'code': code,
#                    'date_start': config.date_start,
#                    'date_stop': config.date_stop,
#                    'company_id': config.company_id.id,
#                }
#                fiscalyear_id = fiscalyear.create(
# cr, uid, vals, context=context)
#                if config.period == 'month':
#                    fiscalyear.create_period(cr, uid, [fiscalyear_id])
#                elif config.period == '3months':
#                    fiscalyear.create_period3(cr, uid, [fiscalyear_id])

        res.update({
            'payment_term_id': payment_term_id,
        })
        return res

    def finish(self, cr, uid, id, context=None):
        ip_obj = self.pool['ir.property']
        imd_obj = self.pool['ir.model.data']
        rccw = self.browse(cr, uid, id, context=context)

        res = super(res_company_create_wizard, self).finish(
            cr, uid, id, context=context)

        # Create Default Properties
        ip_obj.create(cr, uid, {
            'name': 'property_account_receivable',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'account',
                'field_res_partner_property_account_receivable')[1],
            'type': 'many2one',
            'value_reference': 'account.account,%s' % (
                rccw.account_receivable_id.id),
        }, context=context)

        ip_obj.create(cr, uid, {
            'name': 'property_account_payable',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'account',
                'field_res_partner_property_account_payable')[1],
            'type': 'many2one',
            'value_reference': 'account.account,%s' % (
                rccw.account_payable_id.id),
        }, context=context)
        # Create Account Property based on
        # account_receivable
        # account_payable
        # account_expense_categ
        # account_income_categ
        # stock_account_input
        # stock_account_output
        # stock_account_input_categ
        # stock_account_output_categ
        # property_stock_journal

        return res

    # View Section
    def onchange_chart_template_id(
            self, cr, uid, ids, chart_template_id, context=None):
        tax_templ_obj = self.pool['account.tax.template']
        res = {'value': {
            'complete_tax_set': False,
            'sale_tax': False,
            'purchase_tax': False,
            'sale_tax_rate': 0,
            'purchase_tax_rate': 0,
        }}
        if chart_template_id:
            # update complete_tax_set, sale_tax and purchase_tax
            chart_template = self.pool['account.chart.template'].browse(
                cr, uid, chart_template_id, context=context)
            res['value'].update(
                {'complete_tax_set': chart_template.complete_tax_set})
            if chart_template.complete_tax_set:
                sale_tax_ids = tax_templ_obj.search(
                    cr, uid, [
                        ("chart_template_id", "=", chart_template_id),
                        ('type_tax_use', 'in', ('sale', 'all'))],
                    order="sequence, id desc")
                purchase_tax_ids = tax_templ_obj.search(
                    cr, uid, [
                        ("chart_template_id", "=", chart_template_id),
                        ('type_tax_use', 'in', ('purchase', 'all'))],
                    order="sequence, id desc")
                res['value']['sale_tax'] = \
                    sale_tax_ids and sale_tax_ids[0] or False
                res['value']['purchase_tax'] = \
                    purchase_tax_ids and purchase_tax_ids[0] or False
            if chart_template.code_digits:
                res['value']['code_digits'] = chart_template.code_digits
        return res
