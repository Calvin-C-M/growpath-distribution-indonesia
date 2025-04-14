# -*- coding: utf-8 -*-
{
    "name": "GDI Reports",
    "author": "Calvin C M",
    "category": "Purchase",
    "summary": """

    """,
    "description": """ """,
    "version": "18.0.0.1",
    "depends": ['sale_management', 'stock_account', 'account'],
    "application": True,
    "data": [
        # "data/paperformate_edit.xml",
        # "views/layout.xml",
        # "report/sale_quotation.xml",
        "report/sale_order_quotation.xml",
        "report/sales_invoice.xml",
        "report/purchase_order.xml",
        "report/delivery_order.xml",
        
    ],
    "images": ["static/description/background.jpg", ],
    "auto_install": False,
    "installable": True,
}
