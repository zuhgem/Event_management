

from odoo import fields, models, api


class EventBooking(models.Model):
    _name = "event_booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "event booking"
    _rec_name = 'namee'

    namee = fields.Char(string="name", compute="onchange_namee", store=True)
    type = fields.Many2one('event_types', string='Event type', required=True)
    date = fields.Date('Booking date',  default=fields.Datetime.now)
    start_date = fields.Datetime('Starting Date', required=True)
    end_date = fields.Datetime('Ending Date', required=True)

    customer = fields.Many2one('res.partner', string="Customer" )
    duration = fields.Integer(string="Duration", compute="day_rec", store=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')],
                             default="draft")

    @api.depends("type", "start_date")
    def onchange_namee(self):
        if self.type and self.customer and self.start_date and self.end_date:
            start_d = self.start_date.date()
            end_d = self.end_date.date()
            self.namee = str(self.type.name) + ':' + str(self.customer.name) + '/' + str(start_d) + ':'\
                             + str(end_d)

    @api.depends("start_date", "end_date")
    def day_rec(self):
        if self.start_date:
            if self.end_date:
                self.duration = (self.end_date - self.start_date).days
        else:
            self.duration = 0

    def button_confirm(self):
        self.state = 'confirmed'

    def action_catering(self):
        return {
            'name': 'Catering',
            'view_mode': 'tree,form',
            'res_model': 'catering',
            'type': 'ir.actions.act_window',
            'domain': []
        }

