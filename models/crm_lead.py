from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean(string='Date Closed Editable', default=False)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(CrmLead, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        return result

    def toggle_date_closed_edit(self):
        """Toggle the editability of date_closed field"""
        for record in self:
            record.date_closed_editable = not record.date_closed_editable
            # Return action to reload the view
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
