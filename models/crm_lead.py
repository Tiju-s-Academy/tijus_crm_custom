from odoo import models, fields

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    x_date_of_birth = fields.Char(string="Date of Birth")
    x_age = fields.Char(string="Age")
    x_father_guardian = fields.Char(string="Father/Guardian")
    x_qualification = fields.Char(string="Qualification")
    x_course = fields.Char(string="Course")
    x_permanent_address = fields.Char(string="Permanent Address")
    x_city_town = fields.Char(string="City/Town")
    x_state = fields.Char(string="State")
    x_district = fields.Char(string="District")
    x_mobile_alt = fields.Char(string="Mobile (Alt)")
    x_enrollment_number = fields.Char(string="Enrollment No")
    x_receipt_number = fields.Char(string="Receipt No")
    x_fees_paid = fields.Char(string="Fees Paid")
    x_balance_due = fields.Char(string="Balance Due")
