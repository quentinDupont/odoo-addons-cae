# -*- coding: utf-8 -*-
# Copyright (C) 2014-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    _DEFAULT_COMPANY_CODE = 'ZZZ'
    _DEFAULT_CATEGORY_CODE = 'ZZZ'
    _CODE_TEMPLATE = '%(company_prefix)s-%(category_prefix)s-'
    _SUFFIX_LENGTH = 4

    @api.model
    def _get_default_code_by_company_categ(self, company_id, category_id):
        """Return unique reference for a Product depending of company and
         category"""
        company_obj = self.env['res.company']
        category_obj = self.env['product.category']

        # Compute Prefix
        company_prefix = self._DEFAULT_COMPANY_CODE
        if company_id:
            company = company_obj.browse(company_id)
            company_prefix = company.code and company.code or company_prefix

        category_prefix = self._DEFAULT_CATEGORY_CODE
        category = category_obj.browse(category_id)
        category_prefix = category.code and category.code or category_prefix

        prefix = self._CODE_TEMPLATE % ({
            'company_prefix': company_prefix,
            'category_prefix': category_prefix})

        # Compute Suffix
        max_code = 0
        product_ids = self.env['product.product'].search([
            ('default_code', 'like', prefix),
            ('active', '=', 0),
        ], limit=1, order='default_code desc').ids + \
            self.search([
                ('default_code', 'like', prefix),
            ], limit=1, order='default_code desc').ids

        import pdb; pdb.set_trace()
        default_codes = [x.default_code for x in
            self.env['product.product'].browse(product_ids)]
        for default_code in default_codes:
            max_code = max(max_code, int(default_code[-self._SUFFIX_LENGTH:]))

        return {'prefix': prefix, 'max_code': max_code + 1}

    # Field Function Section
    @api.multi
    @api.depends('company_id.code', 'categ_id.code')
    def _compute_default_code(self):
        """Return unique reference for products, depending of company and
        category"""
        prefixes = {}

        for product in self:
            tmp = self._get_default_code_by_company_categ(
                product.company_id.id, product.categ_id.id)
            if not tmp["prefix"] in prefixes:
                prefixes[tmp["prefix"]] = tmp["max_code"]
            else:
                prefixes[tmp["prefix"]] += 1
            product.default_code = tmp["prefix"] +\
                str(prefixes[tmp["prefix"]]).zfill(self._SUFFIX_LENGTH)

    # Overload Section
    @api.model
    def create(self, vals):
        """ special case where product is created by data.xml file and where
        no 'categ_id' is defined."""

        if not vals.get('categ_id', False):
            vals['categ_id'] = self.env.ref('product.product_category_all').id
        tmp = self._get_default_code_by_company_categ(
            vals.get('company_id', False), vals['categ_id'])
        vals['default_code'] = tmp["prefix"] +\
            str(tmp["max_code"]).zfill(self._SUFFIX_LENGTH)
        return super(ProductProduct, self).create(vals)

    # Overload Columns Section
    default_code = fields.Char(compute='_compute_default_code', store=True)

#    # Default Section
#    _defaults = {
#        'default_code': None,
#        'categ_id': None,
#    }
