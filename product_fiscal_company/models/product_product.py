# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.osv import fields


class ProductProduct(Model):
    _inherit = 'product.product'

    _DEFAULT_COMPANY_CODE = 'ZZZ'
    _DEFAULT_CATEGORY_CODE = 'ZZZ'
    _CODE_TEMPLATE = '%(company_prefix)s-%(category_prefix)s-'
    _SUFFIX_LENGTH = 4

    def _compute_default_code(
            self, cr, uid, company_id, category_id, context=None):
        """Return unique reference for a Product depending of company and
         category"""
        company_obj = self.pool['res.company']
        category_obj = self.pool['product.category']

        # Compute Prefix
        company_prefix = self._DEFAULT_COMPANY_CODE
        if company_id:
            company = company_obj.browse(cr, uid, company_id, context=context)
            company_prefix = company.code and company.code or company_prefix

        category_prefix = self._DEFAULT_CATEGORY_CODE
        category = category_obj.browse(cr, uid, category_id, context=context)
        category_prefix = category.code and category.code or category_prefix

        prefix = self._CODE_TEMPLATE % ({
            'company_prefix': company_prefix,
            'category_prefix': category_prefix})

        # Compute Suffix
        max_code = 0
        product_ids = self.search(cr, uid, [
            ('default_code', 'like', prefix),
            ('active', '=', 0),
        ], limit=1, order='default_code desc', context=None) + \
            self.search(cr, uid, [
                ('default_code', 'like', prefix),
            ], limit=1, order='default_code desc', context=None)

        default_codes = [x['default_code'] for x in self.read(
            cr, uid, product_ids, ['default_code'], context=None)]
        for default_code in default_codes:
            max_code = max(max_code, int(default_code[-self._SUFFIX_LENGTH:]))

        return {'prefix': prefix, 'max_code': max_code + 1}

    # Field Function Section
    def _get_default_code(self, cr, uid, ids, field_name, arg, context=None):
        """Return unique reference for products, depending of company and
        category"""
        res = {}
        prefixes = {}

        for product_vals in self.read(
                cr, uid, ids, ['company_id', 'categ_id'], context=None):
            tmp = self._compute_default_code(
                cr, uid, product_vals['company_id'], product_vals['categ_id'],
                context=context)
            if not tmp["prefix"] in prefixes:
                prefixes[tmp["prefix"]] = tmp["max_code"]
            else:
                prefixes[tmp["prefix"]] += 1
            res[product_vals['id']] = tmp["prefix"] +\
                str(prefixes[tmp["prefix"]]).zfill(self._SUFFIX_LENGTH)
        return res

    # Overload Section
    def create(self, cr, uid, vals, context=None):
        """ special case where product is created by data.xml file and where
        no 'categ_id' is defined."""
        model_obj = self.pool['ir.model.data']

        if not vals.get('categ_id', False):
            vals['categ_id'] = model_obj.get_object(
                cr, uid, 'product', 'product_category_all').id
        tmp = self._compute_default_code(
            cr, uid, vals.get('company_id', False), vals['categ_id'],
            context=context)
        vals['default_code'] = tmp["prefix"] +\
            str(tmp["max_code"]).zfill(self._SUFFIX_LENGTH)
        return super(ProductProduct, self).create(
            cr, uid, vals, context=context)

    # Changing default_code where changing category prefix
    def _get_product_by_category(self, cr, uid, ids, context=None):
        product_obj = self.pool['product.product']

        product_ids = []
        for category_id in ids:
            product_ids += product_obj.search(cr, uid, [
                ('categ_id', '=', category_id),
                ('active', '=', 0),
            ], context=context) +\
                product_obj.search(cr, uid, [
                    ('categ_id', '=', category_id),
                ], context=None)
        return product_ids

    # Changing default_code where changing company prefix
    def _get_product_by_company(self, cr, uid, ids, context=None):
        product_obj = self.pool['product.product']

        product_ids = []
        for company_id in ids:
            product_ids += product_obj.search(cr, uid, [
                ('company_id', '=', company_id),
                ('active', '=', 0),
            ], context=None) +\
                product_obj.search(cr, uid, [
                    ('company_id', '=', company_id),
                ], context=None)
        return product_ids

    # Columns Section
    _columns = {
        'default_code': fields.function(
            _get_default_code, type='char', string='Reference', readonly=True,
            store={
                'res.company': (
                    _get_product_by_company, ['code'], 10),
                'product.category': (
                    _get_product_by_category, ['code'], 10),
                'product.product': (
                    lambda self, cr, uid, ids, context=None: ids, [
                        'company_id',
                        'categ_id',
                    ], 10)
            }
        ),
    }

    # Default Section
    _defaults = {
        'default_code': None,
        'categ_id': None,
    }
