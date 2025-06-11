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
    subscription_date = fields.Date(string="Subscription Date")
    is_show_vip = fields.Boolean(compute='_is_show_vip')
    subscription_id = fields.Many2one(
        comodel_name='fritt.subscription',
        string='Subscription'
    )
    group_lesson_ids = fields.Many2many(
        comodel_name='fritt.group.lesson',
        string='Courses'
    )
    lesson_count = fields.Integer(string="Lesson count", compute='_compute_lesson_count')

    @api.depends('subscription_id')
    def _is_show_vip(self):
        """This compute method is used to define if the ribbon VIP will be visible"""
        for record in self:
            record.is_show_vip = False if record.subscription_id.type == 'vip' else True

    @api.depends('group_lesson_ids')
    def _compute_lesson_count(self):
        """This compute method is used to count the number of lessons per member"""
        self.lesson_count = len(self.group_lesson_ids)

    @api.model
    def default_get(self, fields_list):

        defaults = super().default_get(fields_list)
        if 'subscription_date' in fields_list:
            defaults['subscription_date'] = fields.Date.today()

        return defaults

    def open_view_list_lessons(self):
        return {
            'name': 'Lessons',
            'view_mode': 'list',
            'views': [[False, 'list']],
            'domain': [('member_registered.id','=',self.id)],
            'res_model': 'fritt.group.lesson',
            'type': 'ir.actions.act_window',
            'context': {'create': False},
        }
