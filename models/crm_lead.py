from odoo import models, fields, api
from datetime import date

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Personal Details
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    father_guardian = fields.Text(string="Father / Guardian")
    qualification = fields.Text(string="Qualification")
    course = fields.Many2one('product.product', string="Course")

    # Contact Information
    permanent_address = fields.Text(string="Permanent Address")
    city_town = fields.Text(string="City / Town")
    state = fields.Text(string="State")
    district = fields.Text(string="District")
    mobile_alt = fields.Char(string="Mobile (Alt)")

    # Enrollment Details
    enrollment_no = fields.Char(string="Enrollment No")
    receipt_no = fields.Char(string="Receipt No")
    fees_paid = fields.Float(string="Fees Paid", digits=(12, 2))
    balance_due = fields.Float(string="Balance Due", digits=(12, 2))

    # Compute Age from Date of Birth
    @api.depends('date_of_birth')
    def _compute_age(self):
        for lead in self:
            if lead.date_of_birth:
                today = date.today()
                lead.age = today.year - lead.date_of_birth.year - ((today.month, today.day) < (lead.date_of_birth.month, lead.date_of_birth.day))
            else:
                lead.age = 0
