# -*- coding: utf-8 -*-
{
    'name': 'Sudo Account Update Analytic',
    'version': '18.1.0',
    'author': 'Tilabs',
    'category': 'Accounting/Accounting',
    'website': 'http://tilabs.id',
    'summary': 'Update Analytic Account on Account Move',
    'license': 'LGPL-3',
    'description': """
        * Add bulk action to update analytic account for accout moves 
    """,
    'depends': [
        'base',
        'account',
        'analytic',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/update_analytic_wizard_views.xml',
        'wizard/confirm_update_analytic_wizard_views.xml',
        'views/account_move_views_inherit.xml',
    ],
    'installable': True,
    'application': False,
}
