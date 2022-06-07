from flask import Blueprint
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm

class NoteForm(FlaskForm):
    # note_name = StringField("Note_Name", validators=[DataRequired()])
    note_content = StringField("Note_Content", validators=[DataRequired()])
    submit = SubmitField("Add Note")


class KanbanStageForm(FlaskForm):
    stage_name = StringField("Stage_Name", validators=[DataRequired()])
    submit = SubmitField("Add stage")


class KanbanForm(FlaskForm):
    kanban_table_name = StringField("Table_Name", validators=[DataRequired()])
    kanban_table_descripton = StringField("Table_Descripton")
    # kanban_access_users = StringField("Accesed_Users", validators=[DataRequired()])
    submit = SubmitField("Add Kanban Table")
