from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class FrittSubscription(models.Model):
    _name = 'fritt.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #Boolean
    active = fields.Boolean(string='Active', default=True)

    #Char
    name = fields.Char(string='Subscription name', required=True, translate=True)
    description = fields.Char(string="Member's subscription")

    #Datetime
    date_today = fields.Datetime()

    #Monetary
    price = fields.Monetary(string='Price', currency_field='currency_id', compute="_compute_price_access")

    #Integer
    time = fields.Integer(string='Subscription time remaining')
    sequence = fields.Integer(default=10)

    #Selection
    type = fields.Selection(
        selection=[('basic', 'Basic'),
                   ('premium', 'Premium'),
                   ('vip', 'Vip')],
        string='Subscription type')
    time_access = fields.Selection(
        selection=[('10', '10 days per month'),
                   ('30', '30 days per month'),
                   ('illimited', 'Illimited')],
        string="Time's access", compute="_compute_price_access")

    #relations
    currency_id = fields.Many2one(comodel_name='res.currency', string='Devise',
                                  default=lambda self: self.env.company.currency_id)
    member_ids = fields.One2many(comodel_name='fritt.member', inverse_name='subscription_id', string='Members name')

    #logique
    @api.depends('type')
    def _compute_price_access(self):
        for rec in self:
            match rec.type:
                case 'basic':
                    rec.time_access = '10'
                    rec.price = 10
                case 'premium':
                    rec.time_access = '30'
                    rec.price = 30
                case 'vip':
                    rec.time_access = 'illimited'
                    rec.price = 60
                case _:
                    rec.time_access = ''
                    rec.price = 0
