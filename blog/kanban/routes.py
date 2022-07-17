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
    tables = Kanban_Table.query.filter_by(owner_user_id=current_user.id).all()
    if form.validate_on_submit():
        new_kanban_table = Kanban_Table(name=form.kanban_table_name.data,
                                        description=form.kanban_table_descripton.data)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.kanban_table_own.append(new_kanban_table)
        db.session.add(new_kanban_table)
        db.session.commit()
        return redirect(url_for('kanban.kanban_tables_overview'))
    return render_template("kanban_table_overview.html", form=form, tables=tables, logged_in=current_user.is_authenticated)

@kanban.route("/kanban_table/<int:id>", methods=["GET", "POST"])
@login_required
def kanban_table(id):
    note_form = NoteForm()
    stage_form = KanbanStageForm()
    notes = []
    exist_stages = Stage.query.filter_by(inside_kanban_table=id).all()
    notes = Note.query.filter_by(kanban_table=id).all()
    return render_template("kanban_table.html", note_form=note_form, stage_form=stage_form, stages=exist_stages,
                           notes=notes,table_id=id, logged_in=current_user.is_authenticated)
    # return render_template("for_tests.html", note_form=note_form, stage_form=stage_form, stages=exist_stages,
    #                        notes=notes, table_id=id, logged_in=current_user.is_authenticated)


@kanban.route("/kanban_table/new_stage", methods=["GET", "POST"])
@login_required
def new_stages():
    stage_form = KanbanStageForm()
    table_id = request.args.get("table_id")
    if stage_form.validate_on_submit():
        new_stage = Stage(
            name=stage_form.stage_name.data)
        table = Kanban_Table.query.filter_by(id=table_id).first()
        table.stages_id.append(new_stage)
        db.session.add(new_stage)
        db.session.commit()
        return redirect(url_for('kanban.kanban_table', id=table_id))
    return redirect(url_for('kanban.kanban_table', id=table_id))


@kanban.route("/kanban_table/new_notes", methods=["GET", "POST"])
@login_required
def new_notes():
    note_form = NoteForm()
    stage_id = request.args.get("stage_id")
    table_id = request.args.get("table_id")
    if note_form.validate_on_submit():
        new_note = Note(
            content=note_form.note_content.data)
        table = Kanban_Table.query.filter_by(id=table_id).first()
        table.notes_id.append(new_note)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user.kanban_table_note.append(new_note)
        stage = Stage.query.filter_by(id=stage_id).first()
        stage.notes.append(new_note)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('kanban.kanban_table', id=table_id))
    return redirect(url_for('kanban.kanban_table', id=table_id))

@kanban.route("/move_note", methods=["GET"])
def move_note():
    note_id = request.args.get('note_id')
    table_id = request.args.get("id_table")
    next_stage = request.args.get("next_stage")
    note = Note.query.filter_by(id=note_id).first()
    move_note_to_stage = Stage.query.filter_by(name=next_stage).first()
    move_note_to_stage.notes.append(note)
    db.session.commit()
    return redirect(url_for('kanban.kanban_table', id=table_id))

@kanban.route("/delete_note", methods=["GET"])
def delete_note():
    id = request.args.get('id')
    id_table = request.args.get("id_table")
    note_id = Note.query.filter_by(id=id).first()
    db.session.delete(note_id)
    db.session.commit()
    return redirect(url_for('kanban.kanban_table', id=id_table))
