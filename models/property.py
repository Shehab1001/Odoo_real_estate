from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"
    _description = "Property"

    _inherit = ["mail.thread", "mail.activity.mixin"]
    name = fields.Char(default="Villa: ", size= 11, required=1)
    description = fields.Text()
    postcode = fields.Char(required=1, tracking=1)
    date_availability = fields.Date()
    expected_selling_date = fields.Date(tracking = 1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=True)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')

    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ], default='draft')

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    sale_id = fields.Many2one('sale.order')

    owner_phone = fields.Char(related='owner_id.phone')
    owner_address = fields.Char(related='owner_id.address')
    line_ids = fields.One2many('property.line', 'property_id')


    _sql_constraints = [
        ('unique_name','unique("name")','Name already exists!')
    ]

    @api.constrains('bedrooms')
    def _bedrooms_greater_than_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Numbers of Bedrooms is Empty')


    def check_expected_selling_date(self):
            property_ids = self.search([])
            for rec in property_ids:
                if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                    rec.is_late = True
                elif rec.expected_selling_date and rec.expected_selling_date >= fields.date.today():
                    rec.is_late = False

    def action_closed(self):
        for rec in self:
            rec.state = 'closed'


    @api.depends('expected_price', 'selling_price')  # depends on simple fields (view fields + model fields) + relation fields + any fields
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.selling_price - rec.expected_price
            print('inside depends decorator')


    @api.onchange('expected_price')  # depends only on simple fields
    def _onchange_price(self):
        for rec in self:
            rec.diff = rec.selling_price - rec.expected_price
            print('inside onchange decorator')
            if rec.expected_price <= 0:
                return {
                'warning': {'title':'Warning', 'message':'negative number','notification':'warning'},
                 }



    def set_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            print("set to draft")

    def set_to_pending(self):
        for rec in self:
            rec.state = 'pending'
            print("set to pending")

    def set_to_sold(self):
        for rec in self:
            rec.state = 'sold'
            print("set to sold")

# CRUD Operations:

    # @api.model_create_multi
    # def create(self, values):
    #     res = super().create(values)
    #     print("inside Create method :)")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=None, limit=None, order=None):
    #     res = super()._search(domain, offset=None, limit=None, order=None)
    #     print("inside Search method :)")
    #     return res
    #
    # def write(self, vals):
    #     res = super().write(vals)
    #     print("inside Write method :)")
    #     return res
    #
    # def unlink(self):
    #     res = super().unlink()
    #     print("inside Unlink method :)")
    #     return res
    #


class PropertyLine(models.Model):
    _name = "property.line"
    _description = "Property Line"
    area = fields.Float()
    description = fields.Char()
    property_id = fields.Many2one('property')



