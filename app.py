from flask import Flask, render_template, request, redirect, url_for
from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
db = SQLAlchemy(app)


class People(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    surname = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)


class Phones(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    phone_number = db.Column(db.String(length=14), nullable=True)
    phone_number1 = db.Column(db.String(length=14), nullable=True)
    person_id = db.Column(db.Integer(), db.ForeignKey('people.id'))


class Create_User(FlaskForm):
    name = StringField(label='Email:', validators=[DataRequired()])
    surname = StringField(label='Email:', validators=[DataRequired()])
    email = StringField(label='Email:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class Add_Edit_phone(FlaskForm):
    phone = StringField(label='Email:')
    phone1 = StringField(label='Email:')
    submit = SubmitField(label='Save')


with app.app_context():
    db.create_all()

#root to different page - home page
@app.route('/', methods=['POST', 'GET'])
def homepage():
    all_users = People.query.filter().all()
    #all_pnone = Phones.query.filter().all()
    form = Create_User()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        exist = True
        for user in all_users:
            if name == user.name and surname == user.surname:
                exist = False
            elif email == user.email_address:
                exist = False
        if exist:
            person = People(name=name, surname=surname,
                            email_address=email)
            db.session.add(person)
            db.session.commit()
    all_users = People.query.filter().order_by(People.name).all()
    return render_template('home.html', all_users=all_users, form=form)

# root to add phone number
@app.route('/phone/<int:id>', methods=['POST', 'GET'])
def add_phone_number(id):
    form = Add_Edit_phone()
    if form.validate_on_submit():
        person_found = Phones.query.filter(Phones.person_id == id).first()
        if person_found:
            return redirect(url_for('homepage'))
        else:
            phone = form.phone.data
            phone1 = form.phone1.data
            phone_to_add = Phones(phone_number=phone,
                                  phone_number1=phone1, person_id=id)
            db.session.add(phone_to_add)
            db.session.commit()
            return redirect(url_for('homepage'))
    return render_template('add_number.html', form=form, id=id)

# root to edit phone number
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_number(id):
    #
    numbers = Phones.query.filter(Phones.person_id == id).first()
    form = Add_Edit_phone()
    if form.validate_on_submit():
        numbers.phone_number = form.phone.data
        numbers.phone_number1 = form.phone1.data
        db.session.commit()
        db.session.close()
        return redirect(url_for('homepage'))
    if numbers == None:
        form.phone.data = ''
        form.phone1.data = ''
    else:
        form.phone.data = numbers.phone_number
        form.phone1.data = numbers.phone_number1

    return render_template('edit_number.html', id=id, form=form)

# code to run the programmes
if __name__ == '__main__':
    app.run(debug=True)
