{
    'name': "Extract PDF Documents",
	'name_vi_VN': "Trích xuất tài liệu PDF",
    'summary':"""Extract information from PDF document file""",
    'summary_vi_VN': """Trích xuất các thông tin từ tệp tài liệu pdf""",

    'description': """
What it does
============
Module help HR extract information from PDF document file

Key Features
============

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'description_vi_VN': """

===================

Ấn bản được Hỗ trợ
==================
1. Ấn bản Community
2. Ấn bản Enterprise

    """,

    'author': "Viindoo",
    'website': "https://viindoo.com",
    'live_test_url': "https://v15demo-int.erponline.vn",
    'live_test_url_vi_VN': "https://v15demo-vn.erponline.vn",
    'support': "apps.support@viindoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/Viindoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1.0',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/pdf_document_security.xml',
        'security/ir.model.access.csv',
        'wizard/pdf_document_ex_view.xml',
        'views/pdf_document_views.xml',
        'views/pdf_document_data_views.xml',
        'report/pdf_document_active_report_views.xml'
    ],
    'images' : [
        # 'static/description/main_screenshot.png'
        ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
