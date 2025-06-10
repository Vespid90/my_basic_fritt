from odoo import models, fields, api
from datetime import datetime


class FrittSubscription (models.Model):
    _name = 'fritt.subscription'
    _description = 'Subscription'
    _inherit = 'mail.thread'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Subscription')
    time = fields.Integer(string='Subscription time in month')
    type = fields.Selection(selection=[('basic', 'Basic'), ('premium','Premium'), ('vip', 'Vip')], string='Subscription type')
    price = fields.Float(string='Price')
    room_rental_time = fields.Selection(selection=[('10', '10 days'),('30','30 days'), ('illimited', 'Illimited')], string='Room rental time')
    description = fields.Char(string='Member/s subscription')
    sequence = fields.Integer(default=10)
    color = fields.Integer(string="Color")
    date_today = fields.Datetime()
    # date_today = datetime.now()