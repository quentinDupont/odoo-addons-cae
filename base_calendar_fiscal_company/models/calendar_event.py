# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model
from openerp.osv import fields


class calendar_event(Model):
    _inherit = 'calendar.event'

    _columns = {
        'company_id': fields.many2one(
            'res.company', string='Company'),
    }

    _defaults = {
        'company_id': lambda s, cr, uid, c: (
            s.pool.get('res.users')._get_company(cr, uid, context=c)),
    }
