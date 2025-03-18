# -*- coding: utf-8 -*-
{
    'name': 'Sudo Purchasing Template',
    'version': '1.0',
    'author': 'Tilabs',
    'category': 'Inventory/Purchase',
    'website': 'http://tilabs.id',
    'summary': 'Extension Addons for purchasing in Odoo v17',
    'license': 'LGPL-3',
    'description': """
        * Create template model for purhase request & purchase order
    """,
    'depends': [
        'base',
        'purchase',
        # 'purchase_request',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_template_views.xml',
        'views/purchase_order_views_inherit.xml',
        # 'views/purchase_request_views_inherit.xml',
    ],
    'installable': True,
    'application': False,
}
