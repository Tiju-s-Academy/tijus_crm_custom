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

    whatsapp_number = fields.Char(string="WhatsApp Number", related="partner_id.whatsapp_number", store=True)
    date_of_birth = fields.Date(string="Date of Birth", related="partner_id.date_of_birth", store=True)
    age = fields.Integer(string="Age", related="partner_id.age", store=True)
    father_guardian = fields.Char(string="Father/Guardian", related="partner_id.father_guardian", store=True)
    qualification = fields.Char(string="Qualification", related="partner_id.qualification", store=True)
    street = fields.Char(string="Address 1", related='partner_id.street', store=True, readonly=True )
    street2 = fields.Char(string="Address 2", related='partner_id.street2', store=True, readonly=True)
    city = fields.Char(string="City/Town", related='partner_id.city', readonly=True)
    district = fields.Char(string="District", readonly=True)
    country_id = fields.Many2one('res.country',string="Country", related='partner_id.country_id', readonly=True)
    state_id = fields.Many2one('res.country.state',string="State", related='partner_id.state_id', readonly=True)
    mobile_alt = fields.Char(string="Mobile (Alt)", related='partner_id.mobile_alt')

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