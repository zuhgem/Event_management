
from odoo import fields, models, api


class Service(models.Model):
    _name = 'service'
    _description = 'kk'

    name = fields.Char("Name", required=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible Person')
    line_ids = fields.One2many('service.line', 'line_id')
    total = fields.Float('Total', compute='compute_total', store=True)

    @api.depends('line_ids.sub_total')
    def compute_total(self):
        for order in self:
            total = 0.00
            for line in order.line_ids:
                total = total + line.sub_total

            order.update({
                'total': total
            })


class ServiceLine(models.Model):
    _name = 'service.line'

    quantity = fields.Integer("Quantity", required=True)
    unit_price = fields.Float("Unit Price", required=True)
    description = fields.Char("Description")
    sub_total = fields.Float('Sub Total', compute='compute_price', store=True)

    line_id = fields.Many2one('service')

    @api.depends('quantity', 'unit_price')
    def compute_price(self):
        for rec in self:
            if rec.quantity and rec.unit_price:
                rec.sub_total = rec.unit_price * rec.quantity

