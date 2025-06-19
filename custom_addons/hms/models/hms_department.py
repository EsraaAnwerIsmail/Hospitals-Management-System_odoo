from odoo import models, fields

class Department(models.Model):
    _name = 'hms.department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")

    doctor_ids = fields.Many2many(
        comodel_name="hms.doctor",
        relation="hms_doctor_department_rel",
        column1="department_id",
        column2="doctor_id",
        string="Doctors"
    )
