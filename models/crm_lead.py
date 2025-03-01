from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean(
        string='Date Closed Editable',
        default=False,
        tracking=True
    )

    def toggle_date_closed_edit(self):
        """Toggle editability of date_closed field"""
        for record in self:
            record.date_closed_editable = not record.date_closed_editable
