from odoo import models ,fields,api
from datetime import date
from odoo.exceptions import ValidationError



class Patient (models.Model) :
    _name = 'hms.patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
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
    department_capacity = fields.Integer(related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string="State", default='undetermined')

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
                raise ValidationError("CR Ratio is required when PCR is checked.")

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 50:
            self.history = False

