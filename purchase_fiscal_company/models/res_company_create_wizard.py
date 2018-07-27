# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, models


class ResCompanyCreateWizard(models.TransientModel):
    _inherit = 'res.company.create.wizard'

    @api.model
    def res_groups_values(self):
        res = super(ResCompanyCreateWizard, self).res_groups_values()
        res.append('purchase.group_purchase_manager')
        return res

    @api.multi
    def begin(self):
        self.ensure_one()
        property_obj = self.env['ir.property']
        ir_values_obj = self.env['ir.values']
        pricelist_obj = self.env['product.pricelist']
        version_obj = self.env['product.pricelist.version']
        item_obj = self.env['product.pricelist.item']

        res = super(ResCompanyCreateWizard, self).begin()

        # creating Purchase Pricelist
        pricelist = pricelist_obj.create({
            'name': _('%s -  Default Purchase Pricelist') % (self.code),
            'currency_id': self.company_id.currency_id.id,
            'type': 'purchase',
            'company_id': self.company_id.id,
        })
        version = version_obj.create({
            'name': _('%s - Default Purchase Pricelist Version') % (self.code),
            'pricelist_id': pricelist.id,
        })
        item_obj.create({
            'name': _('%s - Default Purchase Pricelist Line') % (self.code),
            'price_version_id': version.id,
            'base': -2,
        })

        # Create Properties for Purchase Pricelist
        field = self.env.ref(
            'purchase.field_res_partner_property_product_pricelist_purchase')
        property_obj.create({
            'name': 'property_product_pricelist_purchase',
            'company_id': self.company_id.id,
            'fields_id': field.id,
            'type': 'many2one',
            'value_reference': 'product.pricelist,%s' % (pricelist.id),
        })

        # Create Default Warehouse for purchase order
        ir_values_obj.set_default(
            'purchase.order', 'warehouse_id', self.warehouse_id.id,
            company_id=self.company_id.id)

        return res
