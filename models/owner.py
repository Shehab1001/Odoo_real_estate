from odoo import models, fields

class Owner(models.Model):
    _name = "owner"
    _description = "Owner"
    name = fields.Char(required=1)
    address = fields.Char()
    phone = fields.Char(required=1)
    property_ids = fields.One2many('property', 'owner_id')

