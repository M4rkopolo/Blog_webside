from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class NoteForm(FlaskForm):
    # note_name = StringField("Note_Name", validators=[DataRequired()])
    note_content = StringField("Card content", validators=[DataRequired()])
    submit = SubmitField("+ Add another card")


class KanbanStageForm(FlaskForm):
    stage_name = StringField("List name", validators=[DataRequired()])
    submit = SubmitField("+ Add a list")


class KanbanForm(FlaskForm):
    kanban_table_name = StringField("Enter board name", validators=[DataRequired()])
    kanban_table_descripton = StringField("Write description")
    # kanban_access_users = StringField("Accesed_Users", validators=[DataRequired()])
    submit = SubmitField("+ Add Kanban Table")
