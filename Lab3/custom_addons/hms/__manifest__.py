{
    'name': 'Hospital Management System',
    'author': 'Esraa Anwer',
    'depends': ['base', 'mail','crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctor_views.xml',
        'views/res_partner_views.xml',
        'views/base_menu.xml'
    ],


        "demo": [],
        "installable": True,
        "application": True,
        "auto_install": False,
        }