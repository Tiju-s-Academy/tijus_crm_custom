from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean(string='Date Closed Editable', default=False)

    def toggle_date_closed_edit(self):
        """Toggle the editability of date_closed field"""
        self.ensure_one()
        self.date_closed_editable = not self.date_closed_editable
        return True
