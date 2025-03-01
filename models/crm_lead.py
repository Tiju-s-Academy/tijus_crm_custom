from odoo import models, fields, api, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    date_closed_editable = fields.Boolean('Date Closed Editable', default=False)

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Override to dynamically set readonly status of date_closed"""
        res = super(CrmLead, self).fields_get(allfields, attributes)
        if 'date_closed' in res:
            res['date_closed']['readonly'] = not self.date_closed_editable
        return res

    def toggle_date_closed_edit(self):
        """Enable/disable date_closed field editability"""
        for record in self:
            record.write({
                'date_closed_editable': not record.date_closed_editable
            })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
