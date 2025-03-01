{
    'name': 'Tijus CRM Custom',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Custom fields for CRM Lead',
    'depends': [
        'base',
        'crm',
        'sale',
        'sale_crm',
        'hr',  # for employee reference
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/res_partner.xml',
        'models/crm_lead.py',  # Add this line
        'views/crm_lead_views.xml',
        'views/crm_views.xml',
    ],
    'installable': True,
    'application': False,
}
