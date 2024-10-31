from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Plant, Garden
from app import db

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/plants')
def plants():
    
    category = request.args.get('category', 'Ayurveda')
    plants = Plant.query.filter_by(category=category).all()
    return render_template('plants.html', plants=plants)

@main.route('/virtual-garden')
@login_required
def virtual_garden():
    gardens = Garden.query.filter_by(user_id=current_user.id).all()
    return render_template('virtual_garden.html', gardens=gardens)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.home'))
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))