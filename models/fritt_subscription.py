from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class FrittSubscription (models.Model):
    _name = 'fritt.subscription'
    _description = 'Subscription'
    _inherit = 'mail.thread'

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Subscription name')
    time = fields.Integer(string='Subscription time remaining')
    type = fields.Selection(selection=[('basic', 'Basic'), ('premium','Premium'), ('vip', 'Vip')], string='Subscription type')
    price = fields.Float(string='Price', store=True)
    time_access = fields.Selection(selection=[('10', '10 days'),('30','30 days'), ('illimited', 'Illimited')], string="Time's access", store=True)
    description = fields.Char(string="Member's subscription")
    sequence = fields.Integer(default=10)
    color = fields.Integer(string="Color")
    date_today = fields.Datetime()
    currency_id = fields.Many2one(comodel_name='res.currency', string='Devise',
                                  default=lambda self: self.env.company.currency_id)
    # member_ids = fields.One2many(comodel_name='fritt.member', inverse_name='subscription_id', string='Members name')



#faire un create
    @api.onchange('type')
    def _onchange_type(self):
        match self.type:
            case 'basic':
                self.time_access = '10'
                self.price = 10
            case 'premium':
                self.time_access = '30'
                self.price = 30
            case 'vip':
                self.time_access = 'illimited'
                self.price = 60


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('type'):
                raise ValidationError("Please choose an subscription type")

        for res in vals_list:
            match res.get('type'):
                case 'basic':
                    res['time_access'] = '10'
                    res['price'] = 10
                case 'premium':
                    res['time_access'] = '30'
                    res['price'] = 30
                case 'vip':
                    res['time_access'] = 'illimited'
                    res['price'] = 60
        results = super().create(vals_list)
        return results

    def write(self, vals):
        match vals.get('type'):
            case 'basic':
                vals['time_access'] = '10'
                vals['price'] = 10
            case 'premium':
                vals['time_access'] = '30'
                vals['price'] = 30
            case 'vip':
                vals['time_access'] = 'illimited'
                vals['price'] = 60
        return super().write(vals)

    # def _action_share_sub(self):
    #     for record in self:
    #         sub_info = f"Subscription type: {record.type}, subscription time: {record.time_access}, price: {record.price}"
    #         record.message_post(body=sub_info)
