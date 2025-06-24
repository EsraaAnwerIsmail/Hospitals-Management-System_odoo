{
    'name': 'Hospital Management System',
    'author': 'Esraa Anwer',
    'depends': ['base', 'mail','crm'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        'report/report_templates.xml',
        'report/reports.xml',
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