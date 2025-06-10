from odoo import models, fields, api

class FrittTrainer(models.Model):
    _name = 'fritt.trainer'
    _description = "My Basic Fritt"

    active = fields.Boolean(string="Active", default='True')
    name = fields.Char(string='Name')
    mail = fields.Char(string='Mail')
    phone = fields.Integer(string='Phone')
    specialty  = fields.Selection([
        ('cardio', "Cardio"),
        ('basketball', "Basketball"),
        ('soccer', "Soccer"),
    ], string="Specialty")
    image = fields.Binary(string="Image")


