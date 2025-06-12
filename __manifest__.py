# -*- coding: utf-8 -*-
{
    'name': "basic_fritt",

    'summary': "Gestionnaire de budget pour entreprise",

    'description': """
Gestionnaire de budget pour entreprise
    """,

    'author': "Vespid",
    'license': "LGPL-3",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'My basic fritt',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/fritt_member_views.xml',
        'views/fritt_subscription_view.xml',
        'views/group_lesson_views.xml',
        'views/fritt_trainer_views.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'application': True,
    'sequence': -100,
}
