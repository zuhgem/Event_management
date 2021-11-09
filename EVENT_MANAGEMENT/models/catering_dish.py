

from odoo import models, fields


class CateringDish(models.Model):
    _name = "catering_dish"
    _description = "catering"

    name = fields.Char("Dish Name", required='True')
    image = fields.Binary("Image")
    unit = fields.Many2one('uom.uom', string='Unit of Measure')

    category = fields.Selection([('welcome_drink', 'Welcome Drink'), ('Break_fast', 'Break Fast'), ('lunch', 'Lunch'),
                                 ('dinner', 'Dinner'), ('snacks_drinks', 'Snacks and Drinks'),
                                 ('beverages', 'Beverages')], string="Category")
    unit_price = fields.Float("Unit Price", required=True)






