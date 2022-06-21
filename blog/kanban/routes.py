from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, Blueprint
from blog.kanban.forms import KanbanForm, NoteForm, KanbanStageForm
from blog.kanban.db_model import Kanban_Table, Stage, Note
from blog.users.db_model import User
from blog import db

kanban = Blueprint("kanban", __name__)

@kanban.route("/kanban_tables", methods=["GET", "POST"])
@login_required
def kanban_tables_overview():
    form = KanbanForm()
    tables = Kanban_Table.query.filter_by(owner_user_name=current_user.user_name).all()
    if form.validate_on_submit():
        new_kanban_table = Kanban_Table(name=form.kanban_table_name.data,
                                        description=form.kanban_table_descripton.data)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.kanban_table_own.append(new_kanban_table)
        db.session.add(new_kanban_table)
        db.session.commit()
        first_stage = Stage(
            name="to do")
        new_kanban_table.stages.append(first_stage)
        db.session.add(first_stage)
        db.session.commit()
        return redirect(url_for('kanban.kanban_tables_overview'))
    return render_template("kanban_table_overview.html", form=form, tables=tables, logged_in=current_user.is_authenticated)

@kanban.route("/kanban_table/<int:id>", methods=["GET", "POST"])
@login_required
def kanban_table(id):
    note_form = NoteForm()
    stage_form = KanbanStageForm()
    exist_stages = Stage.query.filter_by(inside_kanban_table=id).all()
    notes = Note.query.filter_by(kanban_table=id).first()
    if note_form.validate_on_submit():
        new_note = Note(
            content=note_form.note_content.data,
            stage_name=exist_stages[0].name)
        table = Kanban_Table.query.filter_by(id=id).first()
        table.notes.append(new_note)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.kanban_table_note.append(new_note)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('kanban.kanban_table', id=id))
    if stage_form.validate_on_submit():
        new_stage = Stage(name = stage_form.stage_name.data,
                          inside_kanban_table = id)
        table = Kanban_Table.query.filter_by(id=id).first()
        table.stages.append(new_stage)
        db.session.add(new_stage)
        db.session.commit()
        return redirect(url_for('kanban.kanban_table', id=id))
    return render_template("kanban_table.html", note_form=note_form, stage_form=stage_form, stages=exist_stages,
                           notes=notes, logged_in=current_user.is_authenticated)

@kanban.route("/move_note", methods=["GET"])
def move_note():
    id = request.args.get('id')
    id_table = request.args.get("id_table")
    note_id = Note.query.filter_by(id=id).first()
    note_id.stage_name = request.args.get('stage')
    db.session.commit()
    return redirect(url_for('kanban.kanban_table', id=id_table))

@kanban.route("/delete_note", methods=["GET"])
def delete_note():
    id = request.args.get('id')
    id_table = request.args.get("id_table")
    note_id = Note.query.filter_by(id=id).first()
    db.session.delete(note_id)
    db.session.commit()
    return redirect(url_for('kanban.kanban_table', id=id_table))
