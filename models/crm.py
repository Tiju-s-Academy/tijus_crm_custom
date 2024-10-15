from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
class CrmStage(models.Model):
    _inherit = "crm.stage"
    probability = fields.Float(string="Probability")

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    # Selection field for Mode of Study
    mode_of_study = fields.Selection([
        ('offline', 'Offline'),
        ('online', 'Online')
    ], string="Mode of Study", default='offline')

    whatsapp_number = fields.Char(string="WhatsApp Number", related="partner_id.whatsapp_number", store=True, readonly=False)
    date_of_birth = fields.Date(string="Date of Birth", related="partner_id.date_of_birth", store=True, readonly=False)
    age = fields.Integer(string="Age", related="partner_id.age", store=True, readonly=False)
    father_guardian = fields.Char(string="Father/Guardian", related="partner_id.father_guardian", store=True, readonly=False)
    qualification = fields.Char(string="Qualification", related="partner_id.qualification", store=True, readonly=False)
    street = fields.Char(string="Address 1", related='partner_id.street', store=True, readonly=False)
    street2 = fields.Char(string="Address 2", related='partner_id.street2', store=True, readonly=False)
    city = fields.Char(string="City/Town", related='partner_id.city', store=True, readonly=False)
    district = fields.Char(string="District", store=True, readonly=False)
    country_id = fields.Many2one('res.country',string="Country", related='partner_id.country_id', store=True, readonly=False, default=lambda self: self.env.company.country_id.id)
    state_id = fields.Many2one('res.country.state',string="State", related='partner_id.state_id', store=True, readonly=False, default=lambda self: self.env.company.state_id.id)
    mobile_alt = fields.Char(string="Mobile (Alt)", related='partner_id.mobile_alt', store=True, readonly=False)

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    course_id = fields.Many2one('product.product', string="Course", )
    enrollment_number = fields.Char(string="Enrollment No", )

    expected_revenue = fields.Monetary(compute="_compute_expected_revenue", store=True, readonly=False)
    
    @api.depends('course_id')
    def _compute_expected_revenue(self):
        for record in self:
            if record.course_id:
                record.expected_revenue = record.course_id.list_price

    # Override the built-in probability compute method
    probability = fields.Float(compute="_compute_probability")

    @api.depends('stage_id')
    def _compute_probabilities(self):
        for lead in self:
            if lead.stage_id:
                lead.probability = lead.stage_id.probability

    invoice_status = fields.Selection(
        selection=lambda self: self.env["sale.order"]._fields["invoice_status"].selection,
        related="sale_order_id.invoice_status",
        string="Invoice Status",
        readonly=True, copy=False,
        )
    
    is_won = fields.Boolean(related='stage_id.is_won')
    sale_order_id = fields.Many2one('sale.order', string="Sale Order")

    def action_create_sale_order(self):
        if not self.partner_id:
            raise ValidationError(f'You need to set a Customer before confirming the Sale!')
        if not self.course_id:
            raise ValidationError(f'You need to selecte a Course before confirming the Sale!')

        sale_order_data = {
            'opportunity_id': self.id,
            'partner_id': self.partner_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'origin': self.name,
            'source_id': self.source_id.id,
            'company_id': self.company_id.id or self.env.company.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'order_line': [
                (0,0, {
                    'product_id': self.course_id.id,
                })
                ]
        }
        if self.team_id:
            sale_order_data['team_id'] = self.team_id.id
        if self.user_id:
            sale_order_data['user_id'] = self.user_id.id

        sale_order = self.env['sale.order'].create(sale_order_data)
        sale_order.action_confirm()
        self.sale_order_id = sale_order.id

    def action_create_invoice(self):
        if self.sale_order_id:
            return {
                'name': _('Create Invoice'),
                'res_model': 'sale.advance.payment.inv',
                'view_mode': 'form',
                'context': {
                    'active_model': 'sale.order',
                    'active_ids': [self.sale_order_id.id],
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
    invoice_count = fields.Integer(related="sale_order_id.invoice_count")
        
    def action_view_invoice(self):
        if self.sale_order_id:
            if self.invoice_count > 0:
                return self.sale_order_id.action_view_invoice()