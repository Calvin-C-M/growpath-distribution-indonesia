# -*- coding: utf-8 -*-
{
    'name': 'GDI Budgeting',
    'version': '18.1.0',
    'author': 'Calvin',
    'category': 'Accounting',
    'website': 'https://example.com',
    'summary': 'Budgeting Module for Growpath Distribution Indonesia',
    'license': 'LGPL-3',
    'description': """
    """,
    'depends': [
        'gdi_base',
        'account_reports',
    ],
    'data': [
        'views/account_report_budget_view_inherit.xml',
        'views/purchase_order_view_inherit.xml',
    ],
    'installable': True,
    'application': False,
    "assets": {

    }
}
