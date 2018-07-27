# coding: utf-8
# Copyright (C) 2014 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import _, api, fields, models


class ResCompanyCreateWizard(models.TransientModel):
    _inherit = 'res.company.create.wizard'

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse', string='Warehouse', readonly=True)

    # Overload Section
    @api.multi
    def begin(self):
        self.ensure_one()
        warehouse_obj = self.env['stock.warehouse']
        location_obj = self.env['stock.location']
        property_obj = self.env['ir.property']
        ir_values_obj = self.env['ir.values']

        res = super(ResCompanyCreateWizard, self).begin()

        # Create WareHouse
        warehouse = warehouse_obj.create({
            'name': _('%s - Warehouse') % (self.code),
            'code': _('WH%s') % (self.code),
            'company_id': self.company_id.id,
        })
        self.warehouse_id = warehouse.id

        # Remove Parent location for the New view that belong Internal Location
        warehouse.wh_input_stock_loc_id.location_id.location_id = False

        # Create Customer Location
        customer_location = location_obj.create({
            'name': _('%s - Customers') % (self.code),
            'usage': 'customer',
            'company_id': self.company_id.id,
        })

        # Use this location for the 'Out' picking.type
        warehouse.out_type_id.default_location_dest_id = customer_location.id

        # Create Supplier Location
        supplier_location = location_obj.create({
            'name': _('%s - Suppliers') % (self.code),
            'usage': 'supplier',
            'company_id': self.company_id.id,
        })

        # Use this location for the 'In' picking.type
        warehouse.in_type_id.default_location_src_id = supplier_location.id

        # Create Inventory Location
        inventory_location = location_obj.create({
            'name': _('%s - Inventory Loss') % (self.code),
            'usage': 'inventory',
            'company_id': self.company_id.id,
        })

        # Create Procurement Location
        procurement_location = location_obj.create({
            'name': _('%s - Procurements') % (self.code),
            'usage': 'procurement',
            'company_id': self.company_id.id,
        })

        # Create Production Location
        production_location = location_obj.create({
            'name': _('%s - Production') % (self.code),
            'usage': 'production',
            'company_id': self.company_id.id,
        })

        # Create Default Properties
        property_list = [{
            'name': 'property_stock_supplier',
            'field': 'stock.field_res_partner_property_stock_supplier',
            'location_id': supplier_location.id,
        }, {
            'name': 'property_stock_customer',
            'field': 'stock.field_res_partner_property_stock_customer',
            'location_id': customer_location.id,
        }, {
            'name': 'property_stock_inventory',
            'field': 'stock.field_product_template_property_stock_inventory',
            'location_id': inventory_location.id,
        }, {
            'name': 'property_stock_procurement',
            'field': 'stock.field_product_template_property_stock_procurement',
            'location_id': procurement_location.id,
        }, {
            'name': 'property_stock_production',
            'field': 'stock.field_product_template_property_stock_production',
            'location_id': production_location.id,
        }]

        for item in property_list:
            property_obj.create({
                'name': item['name'],
                'fields_id': self.env.ref(item['field']).id,
                'value_reference': 'stock.location,%s' % (item['location_id']),
                'company_id': self.company_id.id,
                'type': 'many2one',
            })

        # Create Default Values
        model_list = [
            'stock.inventory.line', 'stock.fill.inventory',
            'stock.change.product.qty',
        ]

        for model_name in model_list:
            ir_values_obj.set_default(
                model_name, 'location_id', warehouse.lot_stock_id.id,
                company_id=self.company_id.id)

        return res
