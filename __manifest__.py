{
    'name': 'Tijus CRM Custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom fields for CRM Lead',
    'depends': ['crm', 'sale', 'sale_crm'],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/functions.xml',
        'views/res_partner.xml',
        'views/crm_views.xml',
    ],
    'application': False,
}
