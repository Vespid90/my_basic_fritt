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
    planned_lesson_ids = fields.One2many(comodel_name="fritt.group.lesson", inverse_name="trainer_id", string="Planned Lessons")
    planned_lesson_count = fields.Integer(string="Planned Lessons", compute="_compute_planned_lesson")



    @api.depends('planned_lesson_ids')
    def _compute_planned_lesson(self):
        for record in self:
            record.planned_lesson_count= len(record.planned_lesson_ids)

    def open_planned_lesson(self):
        action = {
            'name': 'open_planned_lesson',
            'type': 'ir.actions.act_window',
            'res_model': 'fritt.group.lesson',
            'view_mode': 'kanban,list,form',
            'domain': [('trainer_id', '=', self.name)]
        }

        return action