from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_ids = fields.One2many('property', 'sale_id', domain="[('state','=','draft')]")



    def action_confirm(self):
        res = super().action_confirm()
        print("action confirmed")
        return res