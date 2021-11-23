import datetime

from odoo import models, fields, api


class Catering(models.Model):
    _name = 'catering'
    _description = 'Catering'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.depends('welcome_drink_ids.sub_total', 'break_fast_ids.sub_total', 'lunch_ids.sub_total',
                 'dinner_ids.sub_total', 'drinks_ids.sub_total', 'beverages_ids.sub_total')
    def _compute_welcome_total(self):
        for order in self:
            total = 0.00
            total1 = 0.00
            total_2 = 0.00
            total_d = 0.00
            total_dr = 0.00
            total_b = 0.00
            for line in order.welcome_drink_ids:
                total = total + line.sub_total
            for line in order.break_fast_ids:
                total1 = total1 + line.sub_total
            for line in order.lunch_ids:
                total_2 = total_2 + line.sub_total
            for line in order.dinner_ids:
                total_d = total_d + line.sub_total
            for line in order.drinks_ids:
                total_dr = total_dr + line.sub_total
            for line in order.beverages_ids:
                total_b = total_b + line.sub_total
            order.update({
                'welcome_total': total,
                'break_total': total1,
                'lunch_total': total_2,
                'dinner_total': total_d,
                'drinks_total': total_dr,
                'beverages_total': total_b
            })

    @api.depends('break_total', 'break_total', 'lunch_total', 'dinner_total', 'drinks_total', 'beverages_total')
    def _compute_total(self):
        for rec in self:
            tota = float(self.welcome_total) + float(self.break_total) + float(self.lunch_total) + \
                   float(self.dinner_total) + float(self.drinks_total) + float(self.beverages_total)
        rec.update({
            'total': tota
        })

    name = fields.Char(string='Reference', required=True, readonly=True, copy=False, default='New')
    event_name = fields.Many2one("event_booking", string="Event", required=True)
    date = fields.Date("Date")
    start = fields.Datetime("Start Date")
    end = fields.Datetime("End Date")
    guests = fields.Integer("Guests")
    welcome_drink = fields.Boolean("Welcome Drink", default=False)
    break_fast = fields.Boolean("Break Fast", default=False)
    lunch = fields.Boolean("Lunch", default=False)
    dinner = fields.Boolean("Dinner", default=False)
    snacks_drinks = fields.Boolean("Snacks and Drinks", default=False)
    beverages = fields.Boolean("Beverages", default=False)

    partner_ids = fields.One2many('catering_dish_line', 'beverages_id')
    welcome_drink_ids = fields.One2many("dishline.welcome", "welcome_drink_id")
    break_fast_ids = fields.One2many("dishline.break", "break_fast_id")
    lunch_ids = fields.One2many("dishline.lunch", "lunch_id")
    dinner_ids = fields.One2many("dishline.dinner", "dinner_id")
    drinks_ids = fields.One2many("dishline.snacks", "drinks_id")
    beverages_ids = fields.One2many("dishline.beverages", "beverages_id")

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered'),
                              ('invoiced', 'Invoiced'), ('expired', 'Expired'), ('paid', 'Paid')], default="draft")

    total = fields.Float(string="Total Price", compute='_compute_total', store=True)
    welcome_total = fields.Float(string="Welcome Drink Price", compute='_compute_welcome_total', store=True)
    break_total = fields.Float(string="Break fast Price", compute='_compute_welcome_total', store=True)
    lunch_total = fields.Float(string="Lunch Price", compute='_compute_welcome_total', store=True)
    dinner_total = fields.Float(string="Dinner Price", compute='_compute_welcome_total', store=True)
    drinks_total = fields.Float(string="Drinks Price", compute='_compute_welcome_total', store=True)
    beverages_total = fields.Float(string="Beverages Price", compute='_compute_welcome_total', store=True)

    @api.onchange("event_name")
    def onchange_event(self):
        if self.event_name:
            if self.event_name.start_date:
                self.start = self.event_name.start_date
            if self.event_name.end_date:
                self.end = self.event_name.start_date
            if self.event_name.date:
                self.date = self.event_name.date
        else:
            self.start = ''
            self.end = ''
            self.date = ''

    @api.onchange('event_name')
    def onchange_event_name(self):
        if self.event_name:
            if self.event_name.state == 'confirmed':
                self.state = 'confirmed'

    @api.onchange("start")
    def onchange_start(self):
        if self.start:
            if self.start.date() < datetime.date.today():
                self.state = 'expired'

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('self.service') or 'New'
        result = super(Catering, self).create(vals)
        return result

    def button_confirm(self):
        for rec in self:
            rec.write({'state': 'confirmed'})

    def button_delivered(self):
        for rec in self:
            rec.write({'state': 'delivered'})

    def action_booking(self):
        return {
            'name': 'Event Booking',
            'view_mode': 'tree,form',
            'res_model': 'event_booking',
            'type': 'ir.actions.act_window',
            'domain': []
        }

    def compute_data(self, line):
        return {
            "name": line.dish.name,
            'quantity': line.qty,
            'price_unit': line.dish_price
        }

    def data_line(self):
        order_lines = [(5, 0, 0)]
        for line in self.welcome_drink_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        for line in self.break_fast_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        for line in self.lunch_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        for line in self.dinner_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        for line in self.drinks_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        for line in self.beverages_ids:
            data = self.compute_data(line)
            order_lines.append(data)
        return order_lines

    def button_invoice(self):
        data = self.data_line()

        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.event_name.customer,
            'ref': self.name,
            'state': 'draft',
            'invoice_date': datetime.datetime.today(),
            'date': datetime.datetime.today(),
            'invoice_line_ids': data

        })


class Confirm(models.Model):
    _inherit = 'event_booking'

    def button_confirm(self):
        self.state = 'confirmed'
        confirm = self.env['catering'].search([('event_name', '=', self.namee)])
        if confirm:
            confirm.state = 'confirmed'
        return super(Confirm, self).button_confirm


class Invoice(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        invoice = self.env['catering'].search([('name', '=', self.ref)])
        if invoice:
            invoice.state = 'invoiced'
        return super(Invoice, self).action_post()

    def action_register_payment(self):
        invoice = self.env['catering'].search([('name', '=', self.ref)])
        if invoice:
            invoice.state = 'paid'
        return super(Invoice, self).action_register_payment()


class Paid(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        self.env['catering'].write({'state': 'paid'})
        return super(Paid, self).action_post()