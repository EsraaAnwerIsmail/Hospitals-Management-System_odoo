from odoo.tools.translate import _
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError




class Patient (models.Model) :
    _name = 'hms.patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    email = fields.Char(string='Email', required=True, index=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="_compute_age", store=True)

    department_id = fields.Many2one("hms.department", string="Department", domain=[('is_opened', '=', True)])
    department_capacity = fields.Integer(related='department_id.capacity')
    doctor_ids = fields.Many2many('hms.doctor')

    levels = fields.Selection([('level1','Level1'),('level2','Level2'),('level3' ,'Level3')])
    level_logs = fields.One2many('hms.patient.log','patient_id')


    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="State", default='undetermined')

    def approve_action(self):
        for rec in self:
            if rec.level == 'level1':
                rec.level = 'level2'
            elif rec.level == 'level2':
                rec.level = 'level3'

    # log
    def create_level_log(self):
        for record in self:
            vals = {
                'description': "Level changed to %s" % (record.levels),
                'patient_id': self.id
            }
            self.env['hms.patient.log'].create(vals)

    def write(self, vals):
        for rec in self:
            old_state = rec.state
            res = super(Patient, rec).write(vals)
            new_state = rec.state
            if 'state' in vals and new_state != old_state:
                self.env['hms.patient.log'].create({
                    'patient_id': rec.id,
                    'description': f"State changed to {new_state}"
                })
            return res


    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                birthdate = rec.birth_date
                rec.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            else:
                rec.age = 0


    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required_if_pcr(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("The email address must contain an '@' symbol.")
                # raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 50:
            self.history = ""

    @api.onchange('age')
    def _onchange_age(self):
        for record in self:
            if record.age < 30:
                record.pcr = True
                return {
                    'warning': {
                        'title': 'PCR Checked',
                        'message': 'PCR has been automatically checked as age is below 30.'
                    }
                }
            else:
                record.pcr = False


    # Constraint to ensure unique email
    _sql_constraints = [
        ('unique_patient_email', 'UNIQUE(email)', 'Email must be unique across all patients.')
    ]

    # Validate email format
    @api.constrains('email')
    def _check_email(self):
        for patient in self:
            if patient.email and '@' not in patient.email:
                raise ValidationError(_("The email address must contain an '@' symbol."))

