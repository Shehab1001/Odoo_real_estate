from uaclient.cli.api import action_api

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = "property"
    _description = "Property"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(default="Villa: ", size= 50, required=1, translate=1)
    ref = fields.Char(default = "new", readonly=1)
    description = fields.Text(groups='app_one.property_manager_group')
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
    tag_ids = fields.Many2many('tag', groups='app_one.property_manager_group')
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

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.ref == "new":
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_record(self, old_state, new_state, reason):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or ""
            })

    def action(self):
        print(self.env['property'].search(['|', ('name','=','Villa N-74'), ('postcode', '!=', '4578508')]))


    def set_to_draft(self):
        for rec in self:
            rec.create_history_record(rec.state, 'draft', '')
            rec.state = 'draft'


    def set_to_pending(self):
        for rec in self:
            rec.create_history_record(rec.state, 'pending', '')
            rec.state = 'pending'


    def set_to_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold', '')
            rec.state = 'sold'


    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed', '')
            rec.state = 'closed'


    def open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_window_action')
        action['context'] = {'default_property_id': self.id}
        return action

    def open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action

    # def set_action(self):
    #     print(self.env['owner'].create(
    #         {
    #             'name': 'Mohamed Youssef',
    #             'phone': '0123456789',
    #             'address': '12 Mohamed Youse, Alex, EGY',
    #         }
    #     ))

    # def set_action(self):
    #     print(self.env.company.name)




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



