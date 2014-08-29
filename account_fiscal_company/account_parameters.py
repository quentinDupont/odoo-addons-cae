# -*- encoding: utf-8 -*-
##############################################################################
#
#    Fiscal Company for Account Module for Odoo
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

from openerp import SUPERUSER_ID


def propagate_properties_to_fiscal_childs(
        pool, cr, uid, ids, mother_company_id, model_name, property_name,
        property_value, context=None):
    """
        Propagate a property of objects of the same type for all fiscal
        child of mother company
        @param ids : ids of the objects ;
        @param mother_company_id : mother company into propagate property ;
        @param model_name : model name of the object ;
        @param property_name : name of the property ;
        @param property_value : value of the property ;
    """

    ip_obj = pool.get('ir.property')
    rc_obj = pool.get('res.company')
    imf_obj = pool.get('ir.model.fields')

    # Get fields information
    domain = [('model', '=', model_name), ('name', '=', property_name)]
    imf_id = imf_obj.search(cr, uid, domain, context=context)[0]
    imf = imf_obj.browse(cr, uid, imf_id, context=context)

    # Get company's information
    mother_rc = rc_obj.browse(cr, uid, mother_company_id, context=context)
    rc_ids = [x.id for x in mother_rc.fiscal_childs]

    for id in ids:
        # Delete all property
        domain = [
            ('res_id', '=', '%s,%s' % (model_name, id)),
            ('name', '=', property_name),
            ('company_id', 'in', rc_ids)]
        ip_ids = ip_obj.search(cr, SUPERUSER_ID, domain, context=context)
        ip_obj.unlink(cr, SUPERUSER_ID, ip_ids, context=context)

        # Create property for all fiscal childs
        if property_value:
            for rc_id in rc_ids:
                ip_vals = {
                    'name': property_name,
                    'res_id': '%s,%s' % (model_name, id),
                    'value': property_value,
                    'fields_id': imf.id,
                    'type': imf.ttype,
                    'company_id': rc_id,
                }
                ip_obj.create(cr, SUPERUSER_ID, ip_vals, context=context)
