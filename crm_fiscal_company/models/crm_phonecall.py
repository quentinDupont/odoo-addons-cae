# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp.osv.orm import Model


class crm_phonecall(Model):
    _inherit = 'crm.phonecall'

    _defaults = {
        'company_id': lambda s, cr, uid, c: (
            s.pool.get('res.users')._get_company(cr, uid, context=c)),
    }
