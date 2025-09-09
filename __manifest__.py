{
    'name': 'Warranty Management',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Custom',
    'summary': 'Quản lý bảo hành sản phẩm',
    'depends': ['base', 'stock', 'sale', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'report/warranty_report.xml',
        'report/warranty_templates.xml',
        'views/warranty_views.xml',
        'views/inherit_product_template_view.xml',
        'views/inherit_stock_picking_view.xml',
        'views/mail_template_warranty_expiring.xml',
        'data/ir_sequence.xml',
        'data/data_cron.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'warranty_management/static/src/js/warranty_dashboard.js',
            # 'warranty_management/static/src/views/warranty_dashboard_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
