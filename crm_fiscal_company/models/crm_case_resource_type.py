# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model
from openerp.osv import fields


class crm_case_resource_type(Model):
    _inherit = 'crm.case.resource.type'

    _columns = {
        'company_id': fields.related(
            'section_id', 'company_id', type='many2one',
            string='Company', relation='res.company'),
    }
