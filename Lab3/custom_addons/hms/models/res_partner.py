from odoo.tools.translate import _
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")

    @api.constrains('related_patient_id', 'email')
    def _check_patient_email_uniqueness(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email and partner.email:
                other_partners = self.env['res.partner'].search([
                    ('email', '=', partner.related_patient_id.email),
                    ('id', '!=', partner.id),
                ])
                if other_partners:
                    raise ValidationError(
                        _("The email %s is already assigned to another customer (%s).") % (
                            partner.related_patient_id.email,
                            other_partners[0].name
                        )
                    )

    @api.constrains('vat')
    def _check_vat_mandatory(self):
        for record in self:
            if record.is_company == False and record.customer_rank > 0 and not record.vat:
                raise ValidationError("Tax ID (VAT) is mandatory for customers.")

    def unlink(self):
        for partner in self:
            if partner.related_patient_id:
                patient_name = partner.related_patient_id.name or _("Unnamed Patient")
                raise ValidationError(
                    _("You cannot delete a customer linked to a patient (%s).") % patient_name
                )
        return super().unlink()
