

from odoo import fields, models, api


class DishLine(models.Model):
    _name = 'catering_dish_line'

    dish = fields.Many2one('catering_dish', string='Name', required="True")
    dish_price = fields.Float("Unit Price")
    uom = fields.Many2one('uom.uom', string="UOM")
    category = fields.Selection([('welcome_drink', 'Welcome Drink'), ('Break_fast', 'Break Fast'), ('lunch', 'Lunch'),
                                 ('dinner', 'Dinner'), ('snacks_drinks', 'Snacks and Drinks'),('beverages', 'Beverages')],
                                string="Category")
    welcome_drink_id = fields.Many2one('catering', string='catering', domain="[('category', '=', 'welcome_drink')]")
    break_fast_id = fields.Many2one('catering', string='catering', domain="['|',('category', '=', 'Break_fast')]")
    lunch_id = fields.Many2one('catering', string='catering', domain="[('category', 'in', 'lunch')]")
    dinner_id = fields.Many2one('catering', string='catering', domain="[('category', '=', 'dinner')]")
    drinks_id = fields.Many2one('catering', string='catering', domain="[('category', '=', 'snacks_drinks')]")
    beverages_id = fields.Many2one('catering', string='catering', domain="[('category', '=', 'beverages')]")

    description = fields.Text('Description')
    qty = fields.Integer('Quantity')
    sub_total = fields.Float(string="Sub Total", compute='compute_price', store=True)

    @api.onchange("dish")
    def onchange_dish(self):
        for rec in self:
            if rec.dish:
                if rec.dish.unit_price:
                    rec.dish_price = rec.dish.unit_price
                if rec.dish.unit:
                    rec.uom = rec.dish.unit
                if rec.dish.category:
                    rec.category = rec.dish.category

            else:
                rec.dish_price = ''
                rec.uom = ''
                rec.category = ''

    @api.depends('qty', 'dish_price')
    def compute_price(self):
        for rec in self:
            if rec.qty and rec.dish_price:
                rec.sub_total = rec.dish_price * rec.qty
