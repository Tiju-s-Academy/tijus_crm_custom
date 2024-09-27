from odoo import models, fields

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    x_dob = fields.Date(string="Date of Birth")
    x_age = fields.Integer(string="Age")
    x_father_guardian = fields.Text(string="Father / Guardian")
    x_qualification = fields.Text(string="Qualification")
    x_course = fields.Many2one('product.product', string="Course")
    x_permanent_address = fields.Text(string="Permanent Address")
    x_city_town = fields.Char(string="City / Town")
    x_state = fields.Char(string="State")
    x_district = fields.Char(string="District")
    x_mobile_alt = fields.Char(string="Mobile (Alt)")
    x_enrollment_no = fields.Char(string="Enrollment No")
    x_receipt_no = fields.Char(string="Receipt No")
    x_fees_paid = fields.Monetary(string="Fees Paid", currency_field='currency_id')
    x_balance_due = fields.Monetary(string="Balance Due", currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
