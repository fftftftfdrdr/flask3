from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from models import User, db, bcrypt

app = Flask(name)
app.config.from_object('config.Config')

db.init_app(app)
bcrypt.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created for {}!'.format(form.first_name.data), 'success')
        return redirect(url_for('register'))
    return render_template('register.html', form=form)

if name == 'main':
    app.run(debug=True)