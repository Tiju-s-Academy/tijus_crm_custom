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
        'data/activity_type.xml',  # Added the new activity type data file
        'views/crm_lead_views.xml',
        'views/res_partner.xml',
        'views/crm_views.xml',
        'views/tijus_crm_custom_views.xml',  # Add a line for the new model's access if needed
    ],
    'installable': True,
    'application': False,
}
