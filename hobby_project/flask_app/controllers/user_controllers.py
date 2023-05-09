from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():  
    if 'user_id' not in session:
        flash('Please login before accesing this page')
        return redirect('/login')
    users = User.get_all()
    return render_template('success.html', all_users = users)

@app.route('/create_user', methods = ['post'])
def create_user():
    print(request.form)
    if not User.user_validator(request.form):
        return redirect('/')
    if User.get_user_by_email(request.form):
        flash('email is already in use or your password and confirm password do not match')
        return redirect('/')
    data = {
        'name': request.form['name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    print(data['password'])
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/login', methods = ['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Email/ Password is invalid')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Email/ Password is invalid')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/clear_session')
def clear():
    session.clear()
    return redirect('/')

@app.route("/get_one_user/<int:id>")
def show_one_user(id):
    data = {
        'id' :  id
    }
    return render_template("show_user.html", one_user = User.get_single_user(data))

@app.route("/show_user_edit/<int:id>")
def show_user_edit(id):
    data = {
        'id' :  id
    }
    return render_template("edit_user.html", one_user = User.get_single_user(data))

@app.route('/update_user/<int:id>', methods = ['post'])
def update_user(id):
    print(request.form)
    User.update_user(request.form, id)
    return redirect('/success')

@app.route('/delete/<int:id>')
def delete_user(id):
    User.delete_user(id)
    return redirect('/success')

if __name__ =='__main__':
    app.run(debug=True)
