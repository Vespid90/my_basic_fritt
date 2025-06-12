from odoo import models, fields, api
from odoo.exceptions import ValidationError



review_max_note = 10
review_list_note = [("null", "Pas de note")]
for i in range(0, review_max_note + 1):
    review_list_note.append((str(i), str(i)))
# on ne le fait pas comme ça, si vous souhaitez faire une sélecion intelligente
# utiliser selection_add (<= rechercher ça dans le code)
# mais ceci n'est pas correct

class GroupeLesson(models.Model):
    _name = 'fritt.group.lesson'
    _description = 'GroupeLesson'
    _rec_name = "name"
    #bonne pratique : mettez une ligne vide
    name = fields.Char(string="Name")
    cover = fields.Binary(string='cover')
    # Coach = fields.Selection(selection=[("olivier", "Olivier Harven"), ("jean", "Jean Letor"), ("rudi", "Rudis Hanuise")])
    date_lesson = fields.Date(string="Date")
    dur = fields.Float(string="duration") # pas de raison de l'appeler "dur" et non "duration"
    start_lesson = fields.Float(string="start lesson")
    end_lesson = fields.Float(string="end lesson")
    member_max = fields.Integer(string="member max")
    room = fields.Selection(selection=[("parquet", "Parquet"), ("mini_football", "Mini football"), ("dojo", "Dojo")])
    note = fields.Selection(selection=review_list_note, default='null', string="Note") # utilisez selection_add
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
            #Ici vous avez un gros soucis de performance, vous bouclez dans tous les records
            # imaginez si vous avez 1000000 group lessons, ce n'est pas possible de tout regarder à chaque nouvelle création
            # je vous propose une autre façon de faire en dessous
            for vals in vals_list:
                # ici vous faites une boucle dans une boucle, ce n'est pas du tout bon niveau performance, on essaye d'éviter si possible
                if fields.Date.from_string(record.date_lesson) == fields.Date.from_string(vals.get('date_lesson')) and record.trainer_id.id == vals.get('trainer_id'):
                    # ligne trop longue (bonne pratique python) :
                    # if fields.Date.from_string(record.date_lesson) == fields.Date.from_string(
                    #         vals.get('date_lesson')) and record.trainer_id.id == vals.get('trainer_id'):
                    raise ValidationError('Ce coach est déjà pris. Veuillez sélectionner un autre coach.')
                    # EN ANGLAIS !
        results = super().create(vals_list)
        return results
        # vous pouvez return direct => return super().create(vals_list)

        # # ici cette méthode, je la réécrirai de cette façon :
        # for vals in vals_list:
        #     if vals.get('trainer_id') and vals.get('date_lesson'):
        #         same_date_trainer_lesson = self.env['group.lesson'].search(
        #             [('trainer_id', '=', vals.get('trainer_id')),
        #              ('date_lesson', '=', fields.Date.from_string(record.date_lesson))])
        #         if same_date_trainer_lesson:
        #             raise ValidationError('This coach isn\'t available on the date selected. Please choose another or change the date.')
        #     return super().create(vals_list)

        # Vous pouvez également contracter un peu ce qui donnerait :
        # for vals in vals_list:
        #     if vals.get('trainer_id') and vals.get('date_lesson'):
        #         if same_date_trainer_lesson := self.env['group.lesson'].search(
        #                 [('trainer_id', '=', vals.get('trainer_id')),
        #                  ('date_lesson', '=', fields.Date.from_string(record.date_lesson))]):
        #             raise ValidationError(
        #                 'This coach isn\'t available on the date selected. Please choose another or change the date.')
        #     return super().create(vals_list)



    def cancel(self):
        self.active=False

        print(self.name)
        print(self.trainer_id)
        # attention ne laissez pas de print dans la version finale du code
        if self.trainer_id:
            self.trainer_id.message_post(
                body=f"lesson cancel is : {self.name} , the date is :{self.date_lesson} and is start in {self.start_lesson}")


        return True


    def cal_duration(self):
        self.dur=self.end_lesson-self.start_lesson
        # êtes vous sûrs de toujours avoir un integer correct pour end_lesson et start lesson ?
        # n'hésitez pas à faire des "if" pour checker les données
        if self.dur<0:
            self.dur=0
        print(self.dur)
        # attention au print()

    @api.onchange('end_lesson')
    def _quantity_pc(self):
            self.cal_duration()
            # pourquoi ne pas avoir mis le calcul directement dans le onchange ?
            # + ne faut-il pas start_lesson dans le onchange également ? => @api.onchange('end_lesson', 'start_lesson')