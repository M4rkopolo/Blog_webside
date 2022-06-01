import datetime

def now():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

def astimezone(d, offset):
    return d.astimezone(datetime.timezone(datetime.timedelta(hours=offset)))

def PDTNow():
    return str(astimezone(now(), -7))

def PSTNow():
    return str(astimezone(now(), -8))
	
class Note(UserMixin, db.Model):
	__tablename__ = "kanban_note"
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(100), nullable=False)
	stage_name = db.Column(db.String(30), db.ForgeinKey(stage.name))
	user_id = db.Column(db.Integer, db.ForgeinKey(users.id))
	date = db.Column(db.String, default=PSTNow)
	kanban_table = db.Column(db.Integer, db.ForgeinKey(kanban_table.id))
	
	
	def __init__(self, content, stage_name, user_id)
		self.content = content
		self.stage_name = stage_name
		self.user_id = user_id
	
class Stage(userMixin, db.Model):
	__tablename__ = "kanban_stage"
	id = db.Column(db.Integer, primary_key=True)
	notes = db.relationship("Note", backref="stage")
	name = db.Column(db.String(30), nullable=False)
	inside_kanban_table = db.Column(db.Integer, db.ForgeinKey(kanban_table.id))
	#user_name = db.Column(db.String, db.ForeignKey(user_name))

class Kanban_Table(userMixin, db.Model):
	__tablename__ = "kanban_table"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	description = db.Column(db.String )
	stages = db.relationship("Stage", backref="kanban_table")
	owner_user_name = db.Column(db.String, db.ForeignKey(users.name))
	access_users_name = db.Column(db.String, db.ForeignKey(users.name))
	notes = db.relationship("Note", backref="kanban_notes")
	
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_name = db.Column(db.String(1000))
    image_file = db.Column(db.String(30), nullable=False, default="default.jpg")
    posts = db.relationship("BlogPost", backref="user")
    comments = db.relationship("CommentDB", backref="post")
	kanban_table_own = db.relationship("Kanban_Table", backref="table_owner_user") ##################
	kanban_table_note = db.relationship("Note", backref="note_owner_user")     ##################
	kanban_table_access = db.relationship("NotKanban_Table", backref="table_access_user") ##########
	
    def __init__(self, email, password, user_name):
        self.email = email.lower()
        self.user_name = user_name
        self.password = generate_password_hash(password,
                                               method='pbkdf2:sha256',
                                               salt_length=5)

    def __repr__(self):
        return f"List(id: {self.id}, email: {self.email}, posts: {self.posts}, user_name:{self.user_name})"
		
class NoteForm(FlaskForm):
	note_name = StringField("Note_Name", validators=[DataRequired()])
	note_content = StringField("Note_Content", validators=[DataRequired()])
	submit = SubmitField("Add Note")

class KanbanStageForm(FlaskForm):
	stage_name = StringField("Stage_Name", validators=[DataRequired()])
	submit = SubmitField("Add Note")
	
class KanbanForm(FlaskForm):
	kanban_table_name = StringField("Table_Name", validators=[DataRequired()])
	kanban_table_descripton = StringField("Table_Descripton",validators=[InputRequired(),Length(max=200)])
	kanban_access_users = StringField("Accesed_Users", validators=[DataRequired()])
	submit = SubmitField("Add Kanban Table")
	
class NewUser(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Create new Account")
	
	def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")
		
	
@app.reute("/kanban_tables", methods=["GET","POST"])
@login_required
def kanban_tables_overview():
	form = KanbanForm()
	tables = Kanban_Table.query.filtered_by(owner_user_name=current_user.user_name).all()
	if form.validate_on_submit:
		new_kanban_table = Kanban_Table(
								name=name.form.data,
								description= form.kanban_table_descripton.data,
								owner_user_name = current_user.name)
		 db.session.add(new_kanban_table)
		db.session.commit()
		return 	render_template("kanban_table_overview", form=form, tables=tables)						
	return render_template("kanban_table_overview", form=form, tables=tables)
	
@app.reute("/kanban_table/<int:id>", methods=["GET","POST"])
@login_required
def kanben_table(id)
	note_form = NoteForm()
	stage_form = KanbanStageForm()
	exist_stages = Stage.query.filtered_by(inside_kanban_table=id).all()
	notes = Notes.query.filtered_by(kanban_table=id)
	if note_form.validate_on_submit:
		new_note=Note(
						content = note_form.content.data,
						stage_name = ,
						user_id = current_user.id,
						kanban_table = id)
	return render_template("kanban_table", note_form=note_form, stage_form=stage_form,stages = exist_stages, notes=notes)
	
	
	