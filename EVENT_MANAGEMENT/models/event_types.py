
from odoo import fields, models


class Event(models.Model):

    _name = 'event_types'
    _description = 'event management'

    name = fields.Char('Event Type', required=True)
    code = fields.Char('Event Code', copy=False)
    image = fields.Binary('Image')
