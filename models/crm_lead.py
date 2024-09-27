from odoo import models, fields

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    x_date_of_birth = fields.Char(string="Date of Birth", store=True)
    x_age = fields.Char(string="Age", store=True)
    x_father_guardian = fields.Char(string="Father/Guardian", store=True)
    x_qualification = fields.Char(string="Qualification", store=True)
    x_course = fields.Char(string="Course", store=True)
    x_permanent_address = fields.Char(string="Permanent Address", store=True)
    x_city_town = fields.Char(string="City/Town", store=True)
    x_state = fields.Char(string="State", store=True)
    x_district = fields.Char(string="District", store=True)
    x_mobile_alt = fields.Char(string="Mobile (Alt)", store=True)
    x_enrollment_number = fields.Char(string="Enrollment No", store=True)
    x_receipt_number = fields.Char(string="Receipt No", store=True)
    x_fees_paid = fields.Char(string="Fees Paid", store=True)
    x_balance_due = fields.Char(string="Balance Due", store=True)
