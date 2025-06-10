from odoo import models, fields, api

class FrittMember(models.Model):
    _name = 'fritt.member'
    _description = 'Member of the fitness club'

    active = fields.Boolean(string='Active',default=True)
    photo = fields.Binary(string='Photo')
    name = fields.Char(string='Name')
    mail = fields.Char(string="Mail")
    phonenumber = fields.Char(string="Phone")
    birthdate = fields.Date(string="BirthDate")
    subscriptiondate = fields.Date(string="Subscription Date")
    subscription_id = fields.Many2one(
        comodel_name='fritt.subscription',
        string='Subscription'
    )

    group_lesson_ids = fields.Many2many(
        comodel_name='group.lesson',
        string='Courses'
    )
