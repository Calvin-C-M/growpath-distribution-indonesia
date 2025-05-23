# -*- coding: utf-8 -*-
{
    'name': 'GDI Base',
    'version': '18.1.0',
    'author': 'Calvin',
    'category': 'Accounting',
    'website': 'https://example.com',
    'summary': 'Base Customization for Growpath Distribution Indonesia',
    'license': 'LGPL-3',
    'description': """
    """,
    'depends': [
        'base',
        'purchase',
        'stock',
        'purchase_request',
        'purchase_request_tier_validation',
    ],
    'data': [
        'data/ir_sequence.xml',
        'views/purchase_order_views_inherit.xml',
        'views/stock_picking_views_inherit.xml',
        # 'views/res_company_views_inherit.xml',
    ],
    'installable': True,
    'application': False,
    "assets": {

    }
}
