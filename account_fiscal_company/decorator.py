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

import functools


def replace_company_id_tuple(self, cr, uid, a):
    if a[0] == 'company_id':
        return ('company_id', a[1], self.pool.get("res.company").browse(
            cr, uid, a[2]).fiscal_company.id)
    else:
        return tuple(
            replace_company_id(self, cr, uid, a[x]) for x in range(0, len(a)))


def replace_company_id_dict(self, cr, uid, a):
    if a.get('company_id', False):
        a['company_id'] = self.pool.get("res.company").browse(
            cr, uid, a['company_id']).fiscal_company.id
    else:
        for key in a.keys():
            a[key] = replace_company_id(self, cr, uid, a[key])


def replace_company_id_list(self, cr, uid, a):
    return list(
        replace_company_id(self, cr, uid, a[x]) for x in range(0, len(a)))


def replace_company_id(self, cr, uid, a):
    if 'company_id' in str(a):
        if isinstance(a, tuple):
            return replace_company_id_tuple(self, cr, uid, a)
        elif isinstance(a, dict):
            return replace_company_id_dict(self, cr, uid, a)
        elif isinstance(a, list):
            return replace_company_id_list(self, cr, uid, a)
        else:
            return a
    else:
        return a


def switch_company(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        rc_obj = self.pool.get("res.company")
        args2 = replace_company_id(self, cr, uid, args)
        context = kwargs.get('context', {})
        if context is None:
            context = {}
        c = context.copy()
        if context.get('company_id', False):
            try:
                c['company_id'] = rc_obj.browse(
                    cr, uid, context['company_id']).fiscal_company.id
            except:
                rc_id = rc_obj.search(
                    cr, uid, [('name', '=', context['company_id'])])
                try:
                    c['company_id'] = rc_obj.browse(
                        cr, uid, rc_id).fiscal_company.id
                except:
                    pass
            kwargs['context'] = c
        response = func(self, cr, uid, *args2, **kwargs)
        return response
    return wrapper


def switch_company_period(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        context = kwargs.get('context', {})
        if context is None:
            context = {}
        c = context.copy()
        if context.get('company_id', False):
            c['company_id'] = self.pool.get("res.company").browse(
                cr, uid, context['company_id']).fiscal_company.id
        else:
            c['company_id'] = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.fiscal_company.id
        kwargs['context'] = c
        response = func(self, cr, uid, *args, **kwargs)
        return response
    return wrapper


def add_user_company(func):
    @functools.wraps(func)
    def wrapper(self, cr, uid, *args, **kwargs):
        context = kwargs.get('context', {})
        c = context.copy()
        if not context.get('company_id', False):
            c['company_id'] = self.pool.get('res.users').browse(
                cr, uid, uid, context=context).company_id.id
        kwargs['context'] = c
        response = func(self, cr, uid, *args, **kwargs)
        return response
    return wrapper
