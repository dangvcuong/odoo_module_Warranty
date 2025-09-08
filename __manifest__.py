{
    'name': 'Warranty Management',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Custom',
    'summary': 'Quản lý bảo hành sản phẩm',
    'depends': ['base', 'stock', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/warranty_views.xml',
        'views/inherit_product_template_view.xml',
        'views/inherit_stock_picking_view.xml',
        'data/ir_sequence.xml',
        'data/data_cron.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
