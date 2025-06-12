from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class FrittSubscription (models.Model):
    _name = 'fritt.subscription'
    _description = 'Subscription'
    _inherit = 'mail.thread'
    # rajouter mail.activity.mixin sinon le chatter n'aura pas toutes ses fonctionnalités
    # => _inherit = ['mail.thread', 'mail.activity.mixin']

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string='Subscription name')
    time = fields.Integer(string='Subscription time remaining')
    type = fields.Selection(selection=[('basic', 'Basic'), ('premium','Premium'), ('vip', 'Vip')], string='Subscription type')
    price = fields.Float(string='Price', store=True)
    # le store = true n'est pas nécessaire, un champ de type float est storé par défaut
    time_access = fields.Selection(selection=[('10', '10 days per month'),('30','30 days per month'), ('illimited', 'Illimited')], string="Time's access", store=True)
    # Bonne pratique python : on essaye de ne pas faire des lignes trop longues
    # Préférez cette écriture :
    # time_access = fields.Selection(
    #     selection=[('10', '10 days per month'),
    #                ('30', '30 days per month'),
    #                ('illimited', 'Illimited')],
    #     string="Time's access", store=True)
    # Aussi le store=True est par défault pour un champ selection, pas nécessaire de le rajouter
    description = fields.Char(string="Member's subscription")
    sequence = fields.Integer(default=10)
    date_today = fields.Datetime()

    #relations
    currency_id = fields.Many2one(comodel_name='res.currency', string='Devise',
                                  default=lambda self: self.env.company.currency_id)
    # très bien d'avoir géré la devise !
    member_ids = fields.One2many(comodel_name='fritt.member', inverse_name='subscription_id', string='Members name')


    #logique
    @api.onchange('type')#changement visuel lors de la creation d'abonnements
    # pour les commentaires sur les méthodes, écrivez cela en docstring :https://www.geeksforgeeks.org/python-docstrings/
    def _onchange_type(self):
        # n'oubliez pas de gérer l'absence de type aussi
        # que se passe-t-il si type = False/None ?
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
    def create(self, vals_list):#méthode create pour enregistrer les abonnements dans la db => remettre en docstring
        for vals in vals_list:
            if not vals.get('type'):
                raise ValidationError("Please choose an subscription type")

        for res in vals_list:
            match res.get('type'):#match/case pour faire concorder les données de chaque abonnements
                case 'basic':
                    res['time_access'] = '10'
                    res['price'] = 10
                case 'premium':
                    res['time_access'] = '30'
                    res['price'] = 30
                case 'vip':
                    res['time_access'] = 'illimited'
                    res['price'] = 60
        # 1. ne pas écrire for res in vals_list mais plutôt for vals in vals_list (bonne pratique
        # 2. Le onchange et ce bout de code est identique, on aime pas ça du tout en programmation
        # si je rajoute un type, vous devez apporter la même amélioration 2x
        # donc ici vous avez 2 façon de faire :
            # - appeller l'onchange dans le create (ce qui remplace la logique)
            # - faire de time_acces et de price un compute (si la situation s'y prête)
        results = super().create(vals_list)
        return results

    def write(self, vals):#méthode write pour enregistrer les éditions d'abonnements dans la db
        # même remarque ici : doublon de code à éviter
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
