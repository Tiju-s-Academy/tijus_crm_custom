from odoo import models, fields, api

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

    # def _prepare_opportunity_quotation_context(self):
    #     """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
    #     self.ensure_one()
    #     quotation_context = {
    #         'default_opportunity_id': self.id,
    #         'default_partner_id': self.partner_id.id,
    #         'default_campaign_id': self.campaign_id.id,
    #         'default_medium_id': self.medium_id.id,
    #         'default_origin': self.name,
    #         'default_source_id': self.source_id.id,
    #         'default_company_id': self.company_id.id or self.env.company.id,
    #         'default_tag_ids': [(6, 0, self.tag_ids.ids)]
    #     }
    #     if self.team_id:
    #         quotation_context['default_team_id'] = self.team_id.id
    #     if self.user_id:
    #         quotation_context['default_user_id'] = self.user_id.id
    #     return quotation_context