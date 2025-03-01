from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean(
        string='Date Closed Editable',
        default=False,
        copy=False
    )

    def action_toggle_date_closed(self):
        """Toggle editability of date_closed field"""
        for record in self:
            record.date_closed_editable = not record.date_closed_editable
        return True

    def write(self, vals):
        # Override write to handle date_closed field editability
        if 'date_closed' in vals and not self.date_closed_editable:
            vals.pop('date_closed')
        return super(CrmLead, self).write(vals)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        # Override to dynamically set readonly status
        res = super(CrmLead, self).fields_get(allfields, attributes)
        if 'date_closed' in res:
            res['date_closed']['readonly'] = False
        return res

    def toggle_date_edit(self):
        """Enable/disable date_closed field editability"""
        self.ensure_one()
        self.write({
            'date_closed_editable': not self.date_closed_editable
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
