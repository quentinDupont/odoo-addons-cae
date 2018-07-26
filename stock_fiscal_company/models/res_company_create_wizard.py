# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Stock Module for Odoo
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
from openerp.tools.translate import _


class res_company_create_wizard(TransientModel):
    _inherit = 'res.company.create.wizard'

    _columns = {
        'physical_location_parent_id': fields.many2one(
            'stock.location', 'Parent Physical Locations', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'customer_location_parent_id': fields.many2one(
            'stock.location', 'Parent Customers Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'supplier_location_parent_id': fields.many2one(
            'stock.location', 'Parent Suppliers Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'inventory_location_parent_id': fields.many2one(
            'stock.location', 'Parent Inventory Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'procurement_location_parent_id': fields.many2one(
            'stock.location', 'Parent Procurement Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'production_location_parent_id': fields.many2one(
            'stock.location', 'Parent Production Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
        'scrapped_location_parent_id': fields.many2one(
            'stock.location', 'Parent Scrapped Location', required=True,
            domain="[('company_id', '=', mother_company)]"),
    }

    # Overload Section
    def begin(self, cr, uid, id, context=None):
        sl_obj = self.pool['stock.location']
        ip_obj = self.pool['ir.property']
        sw_obj = self.pool['stock.warehouse']
        imd_obj = self.pool['ir.model.data']
        res = super(res_company_create_wizard, self).begin(
            cr, uid, id, context=context)
        rccw = self.browse(cr, uid, id, context=context)

        # Create Stock Locations
        sl_physical_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Physical Locations') % (rccw.code),
            'usage': 'view',
            'location_id': rccw.physical_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        # TODO Set default value to
        # location_id   stock.change.product.qty
        # location_id   stock.fill.inventory
        # location_id   stock.inventory.line
        sl_stock_id = sl_obj.create(cr, uid, {
            'name': _('%s - Stock') % (rccw.code),
            'usage': 'internal',
            'location_id': sl_physical_location_id,
            'company_id': rccw.company_id.id,
        }, context=context)

        # TODO Check if it's necessary ?!?
        sl_output_id = sl_obj.create(cr, uid, {
            'name': _('%s - Output') % (rccw.code),
            'usage': 'internal',
            'location_id': sl_physical_location_id,
            'company_id': rccw.company_id.id,
        }, context=context)

        sl_customer_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Customers') % (rccw.code),
            'usage': 'customer',
            'location_id': rccw.customer_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        sl_supplier_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Suppliers') % (rccw.code),
            'usage': 'supplier',
            'location_id': rccw.supplier_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        sl_inventory_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Inventory loss') % (rccw.code),
            'usage': 'inventory',
            'location_id': rccw.inventory_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        sl_procurement_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Procurements') % (rccw.code),
            'usage': 'procurement',
            'location_id': rccw.procurement_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        sl_production_location_id = sl_obj.create(cr, uid, {
            'name': _('%s - Production') % (rccw.code),
            'usage': 'production',
            'location_id': rccw.production_location_parent_id.id,
            'company_id': rccw.company_id.id,
        }, context=context)

        # TODO Check if it is necessary
#        sl_obj.create(cr, uid, {
#            'name': _('%s - Scrapped') % (rccw.code),
#            'usage': 'inventory',
#            'location_id': rccw.scrapped_location_parent_id.id,
#            'company_id': rccw.company_id.id,
#            }, context=context)

        # Create WareHouse
        sw_id = sw_obj.create(cr, uid, {
            'name': _('%s - Warehouse') % (rccw.code),
            'lot_input_id': sl_stock_id,
            'lot_stock_id': sl_stock_id,
            'lot_output_id': sl_output_id,
            'company_id': rccw.company_id.id,
        }, context=context)

        # Create Default Properties
        ip_obj.create(cr, uid, {
            'name': 'property_stock_supplier',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'stock',
                'field_res_partner_property_stock_supplier')[1],
            'type': 'many2one',
            'value_reference': 'stock.location,%s' % (sl_supplier_location_id),
        }, context=context)

        ip_obj.create(cr, uid, {
            'name': 'property_stock_customer',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'stock',
                'field_res_partner_property_stock_customer')[1],
            'type': 'many2one',
            'value_reference': 'stock.location,%s' % (sl_customer_location_id),
        }, context=context)

        # TODO Check if it is necessary
#        ip_obj.create(cr, uid, {
#            'name': 'property_stock_customer',
#            'company_id': rccw.company_id.id,
#            'fields_id': imd_obj.get_object_reference(
#                cr,uid, 'stock', 'field_res_partner_property_stock_customer')
#            'type': 'many2one',
#            'value_reference':
#                 'stock.location,%s' % (sl_customer_location_id),
#            'res_id': res['partner_id']
#            }, context=context)

        ip_obj.create(cr, uid, {
            'name': 'property_stock_procurement',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'stock',
                'field_product_template_property_stock_procurement')[1],
            'type': 'many2one',
            'value_reference':
            'stock.location,%s' % (sl_procurement_location_id),
        }, context=context)

        ip_obj.create(cr, uid, {
            'name': 'property_stock_inventory',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'stock',
                'field_product_template_property_stock_inventory')[1],
            'type': 'many2one',
            'value_reference':
            'stock.location,%s' % (sl_inventory_location_id),
        }, context=context)

        ip_obj.create(cr, uid, {
            'name': 'property_stock_production',
            'company_id': rccw.company_id.id,
            'fields_id': imd_obj.get_object_reference(
                cr, uid, 'stock',
                'field_product_template_property_stock_production')[1],
            'type': 'many2one',
            'value_reference':
            'stock.location,%s' % (sl_production_location_id),
        }, context=context)

        res.update({
            'warehouse_id': sw_id,
        })
        return res
