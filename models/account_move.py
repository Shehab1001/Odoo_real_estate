from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'account.move'


    def action_do_something(self):
        print(self,"do something")
        # when i hit a button Confirm in accounting, it displays that phrase in console:
        # "do something"