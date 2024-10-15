from odoo import models,fields,api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp_number = fields.Char(string="WhatsApp Number")
    mobile_alt = fields.Char(string="Mobile (Alt)", )

    date_of_birth = fields.Date(string="Date of Birth", )
    age = fields.Integer(string="Age")
    father_guardian = fields.Char(string="Father/Guardian", )
    qualification = fields.Char(string="Qualification", )
    district = fields.Char(string="District", )
