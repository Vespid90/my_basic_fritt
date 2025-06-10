from odoo import models, fields, api


review_max_note = 10
review_list_note = [("null","Pas de note")]
for i in range(0,review_max_note + 1):
    review_list_note.append((str(i),str(i)))



class GroupeLesson(models.Model):
    _name = 'fritt.group.lesson'
    _description = 'GroupeLesson'
    _rec_name = "name"
    name = fields.Char(string="Name")
    cover = fields.Binary(string='cover')
    Coach = fields.Selection(selection=[("olivier", "Olivier Harven"), ("jean", "Jean Letor"), ("rudi", "Rudis Hanuise")])
    date_lesson=fields.Date(string="Date")
    duration=fields.Selection(selection=[("60", "1h"), ("90", "1h30"), ("120", "2h")])
    start_lesson = fields.Char(string="start lesson")
    end_lesson = fields.Char(string="end lesson")
    member_max=fields.Integer(string="member max")
    roam = fields.Selection(selection=[("parquet", "Parquet"), ("mini_football", "Mini football"), ("dojo", "Dojo")])
    note = fields.Selection(tracking=True,selection=review_list_note,default='null',string="Note")
    # relation
    member_registered_number=fields.Integer(string="member registered number")
    # relation
    member_registered=fields.Integer(string="member registered")
    active = fields.Boolean(string="active")

    sequence = fields.Integer(default=10)



