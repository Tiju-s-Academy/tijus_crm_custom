from odoo import models,fields,api

class MailMessage(models.Model):
    _inherit = "mail.message"
    _order = "create_date desc"