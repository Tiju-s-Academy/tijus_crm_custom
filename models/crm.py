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

    avatar_128 = fields.Binary(string="Avatar 128", related='partner_id.avatar_128', store=True, readonly=False)
    image_1920 = fields.Binary(string="Image", related="partner_id.image_1920", store=True, readonly=False)

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

    aadhaar_no = fields.Char(string="Student Aadhaar No", related='partner_id.aadhaar_no', store=True, readonly=False)
    # Bank Details
    bank_account_name = fields.Char(string="Account Holder Name", related='partner_id.bank_account_name', store=True, readonly=False)
    bank_account_no = fields.Char(string="Account No", related='partner_id.bank_account_no', store=True, readonly=False)
    bank_ifsc_code = fields.Char(string="IFSC Code", related='partner_id.bank_ifsc_code', store=True, readonly=False)
    bank_name = fields.Char(string="Bank Name", related='partner_id.bank_name', store=True, readonly=False)
    relation_with_bank_acc_holder = fields.Selection(
        selection=[('self', 'Self/Own'),('spouse', 'Spouse'),
            ('mother', 'Mother'),('father', 'Father'),('grand_father', 'Grand Father'),
            ('grand_mother', 'Grand Mother'),('uncle', 'Uncle'),
            ('aunt', 'Aunt'),('brother', 'Brother'),
            ('sister', 'Sister'),('son', 'Son'),
            ('daughter', 'Daughter'),('other', 'Other (Specify)')
        ],
        string="Relationship with Account Holder", default="self", related='partner_id.relation_with_bank_acc_holder', store=True, readonly=False
    )
    relation_with_bank_acc_holder_manual = fields.Char(string="Specify Relation", related='partner_id.relation_with_bank_acc_holder_manual', store=True, readonly=False)

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    course_id = fields.Many2one('product.product', string="Course", )
    enrollment_number = fields.Char(string="Enrollment No", )

    expected_revenue = fields.Monetary(compute="_compute_expected_revenue", store=True, readonly=False)
    
    referred_by = fields.Many2one('hr.employee', string="Referred By")
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

        if not self.aadhaar_no or not self.bank_account_name or not self.bank_account_no or not self.bank_ifsc_code or not self.bank_name or not self.relation_with_bank_acc_holder:
            raise ValidationError(f'You have to fill the following fields before confirming Sale:\n Aadhaar No, Account Holder Name, Account No, IFSC Code, Bank Name, Relationship with Account Holder')
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

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        res.set_lead_queue()
        return res
    
    def write(self, vals):
        res = super().write(vals)
        self.set_lead_queue()
        return res

    def set_lead_queue(self):
        for record in self:
            if record.team_id and record.type=='lead' and not record.user_id:
                if record.team_id.queue_line_ids:
                    all_users_assigned_lead = len(record.team_id.queue_line_ids.mapped('current_lead')) == len(record.team_id.queue_line_ids)
                    if all_users_assigned_lead:
                        record.team_id.queue_line_ids[0].write({'current_lead': record.id})
                        record.write({'user_id': record.team_id.queue_line_ids[0].salesperson_id.id})
                        for queue_line in record.team_id.queue_line_ids[1:]:
                            queue_line.write({'current_lead': False})
                    else:
                        for queue_line in record.team_id.queue_line_ids:
                            if not queue_line.current_lead:
                                queue_line.write({'current_lead': record.id})
                                record.write({'user_id': queue_line.salesperson_id.id})
                                break

            
class CrmTeam(models.Model):
    _inherit = "crm.team"
    queue_line_ids = fields.One2many('crm.lead.queueing.line', 'team_id', store=True)

    def create(self, vals):
        res = super().create(vals)
        self.set_queue_line_ids(res)
        return res
    
    def write(self, vals):
        res = super().write(vals)
        self.set_queue_line_ids(self)
        return res
    
    def set_queue_line_ids(self, recs):
        for record in recs:
            queue_line_users = record.queue_line_ids.mapped('salesperson_id.id')
            for member in record.member_ids:
                if member.id not in queue_line_users:
                    self.env['crm.lead.queueing.line'].create({
                        'salesperson_id': member.id,
                        'current_lead': False,
                        'team_id': record.id
                    })

    @api.model
    def action_set_queue_line_ids_for_all_teams(self):
        recs = self.env['crm.team'].search([])
        self.set_queue_line_ids(recs)

class CrmLeadQueueingLine(models.Model):
    _name = "crm.lead.queueing.line"
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    current_lead = fields.Many2one('crm.lead', domain=[('type','=','lead')])
    team_id = fields.Many2one('crm.team', check_company=True)
    