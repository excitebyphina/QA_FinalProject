from flask import Flask, render_template, flash, redirect, url_for
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
    name = StringField(label='First Name:', validators=[DataRequired()])
    surname = StringField(label='Last Name:', validators=[DataRequired()])
    email = StringField(label='Email:', validators=[DataRequired()])
    phone = StringField(label='Phone:', validators=[DataRequired()])
    phone1 = StringField(label='Phone:', validators=[DataRequired()])
    submit = SubmitField(label='Create User', validators=[DataRequired()])


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def homepage():
    all_users = db.session.query(People, Phones).join(
        Phones).filter().order_by(People.name).all()
    form = Create_User()
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        phone = form.phone.data
        phone1 = form.phone1.data
        exist = True
        for user in all_users:
            if name == user[0].name and surname == user[0].surname:
                flash(f'User already exist {email}', category='danger')
                exist = False
                form.name.data = form.surname.data = form.email.data = form.phone.data = form.phone1.data = ' '
            elif email == user[0].email_address:
                flash(f'There is a User with {email}', category='danger')
                exist = False
                form.name.data = form.surname.data = form.email.data = form.phone.data = form.phone1.data = ' '
        if exist:
            person = People(name=name, surname=surname,
                            email_address=email)
            db.session.add(person)
            db.session.commit()

            phone_to_add = Phones(phone_number=phone,
                                  phone_number1=phone1, person_id=person.id)
            db.session.add(phone_to_add)
            db.session.commit()
            all_users = db.session.query(People, Phones).join(
                Phones).filter().order_by(People.name).all()
            form.name.data = form.surname.data = form.email.data = form.phone.data = form.phone1.data = ' '
    return render_template('home.html', all_users=all_users, form=form)


@app.route('/phone/<int:id>', methods=['POST', 'GET'])
def delete_row(id):
    form = Create_User()
    People.query.filter(People.id == id).delete()
    Phones.query.filter(Phones.person_id == id).delete()
    db.session.commit()
    all_users = db.session.query(People, Phones).join(
        Phones).filter().order_by(People.name).all()
    return render_template('home.html', form=form, all_users=all_users)


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit_number(id):
    edit_person = db.session.query(People, Phones).join(
        Phones).filter(People.id == id).first()
    form = Create_User()
    if form.validate_on_submit():
        edit_person[0].name = form.name.data
        edit_person[0].surname = form.surname.data
        edit_person[0].email_address = form.email.data
        edit_person[1].phone_number = form.phone.data
        edit_person[1].phone_number1 = form.phone1.data
        db.session.commit()
        db.session.close()
        return redirect(url_for('homepage'))
    form.name.data = edit_person[0].name
    form.surname.data = edit_person[0].surname
    form.email.data = edit_person[0].email_address
    form.phone.data = edit_person[1].phone_number
    form.phone1.data = edit_person[1].phone_number1
    return render_template('edit_number.html', id=id, form=form)


if __name__ == '__main__':
    app.run(debug=True)
