from odoo import models, fields, api
from odoo.exceptions import ValidationError



review_max_note = 10
review_list_note = [("null", "Pas de note")]
for i in range(0, review_max_note + 1):
    review_list_note.append((str(i), str(i)))


class GroupeLesson(models.Model):
    _name = 'fritt.group.lesson'
    _description = 'GroupeLesson'
    _rec_name = "name"
    name = fields.Char(string="Name")
    cover = fields.Binary(string='cover')
    # Coach = fields.Selection(selection=[("olivier", "Olivier Harven"), ("jean", "Jean Letor"), ("rudi", "Rudis Hanuise")])
    date_lesson = fields.Date(string="Date")
    dur = fields.Float(string="duration")
    start_lesson = fields.Float(string="start lesson")
    end_lesson = fields.Float(string="end lesson")
    member_max = fields.Integer(string="member max")
    room = fields.Selection(selection=[("parquet", "Parquet"), ("mini_football", "Mini football"), ("dojo", "Dojo")])
    note = fields.Selection(selection=review_list_note, default='null', string="Note")
    # relation
    comment=fields.Text(string="comment")

    active = fields.Boolean(string="active")

    sequence = fields.Integer(default=10)
    # relation

    member_registered_ids = fields.Many2many(string="member registered", comodel_name="fritt.member")
    member_registered_number = fields.Integer(string="Total member registered", compute="_compute_im_status")
    trainer_id = fields.Many2one(
        comodel_name='fritt.trainer',
        string='Coach'
    )

    @api.depends('member_registered_ids')
    def _compute_im_status(self):
        """Compute the im_status of the users"""

        for record in self:
            # if record.list_id:
            record.member_registered_number = len(record.member_registered_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for record in self.search([]):
            for vals in vals_list:
                if fields.Date.from_string(record.date_lesson) == fields.Date.from_string(vals.get('date_lesson')) and record.trainer_id.id == vals.get('trainer_id'):
                    raise ValidationError('Ce coach est déjà pris. Veuillez sélectionner un autre coach.')
        results = super().create(vals_list)
        return results

    def cancel(self):
        self.active=False

        print(self.name)
        print(self.trainer_id)
        if self.trainer_id:
            self.trainer_id.message_post(
                body=f"lesson cancel is : {self.name} , the date is :{self.date_lesson} and is start in {self.start_lesson}")


        return True


    def cal_duration(self):
        self.dur=self.end_lesson-self.start_lesson
        if self.dur<0:
            self.dur=0
        print(self.dur)

    @api.onchange('end_lesson')
    def _quantity_pc(self):
            self.cal_duration()