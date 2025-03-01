from odoo import models, fields, api

class CrmLeadDateClosed(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean(
        string='Date Closed Editable',
        default=False,
        copy=False
    )

    def toggle_closed_date(self):
        """Toggle editability of date_closed field"""
        self.ensure_one()
        self.date_closed_editable = not self.date_closed_editable
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
