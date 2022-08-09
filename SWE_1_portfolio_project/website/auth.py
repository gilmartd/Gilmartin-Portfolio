from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Pile, PileUpdate
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import datetime
import pika
import os

auth = Blueprint('auth', __name__)


def julian(std_date):
    """
    takes an input of a datetime class and returns a julian day
    """
    fmt = '%Y-%m-%d'
    sdt_date = datetime.datetime.strptime(std_date, fmt)
    sdt_date = sdt_date.timetuple()
    jdate = sdt_date.tm_yday
    return (jdate)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exist', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists', category='error')
        if len(username) < 2:
            flash('Username must be at least 2 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be at least 2 characters', category='error')
        elif len(lastName) < 2:
            flash('Last name must be at least 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords must match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(username=username, firstName=firstName, lastName=lastName,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        ingredient = request.form.get('ingredient')
        volume = request.form.get('volume')

        if len(volume) <= 0:
            flash('Volume cannot be zero', category='error')
        else:
            new_pile = Pile(ratio=ingredient, volume=volume, user_id=current_user.id)
            eventCreate = PileUpdate(ratio=ingredient, volume=volume, user_id=current_user.id)
            db.session.add(eventCreate)
            db.session.commit()
            db.session.add(new_pile)
            db.session.commit()
            flash('Pile Created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create.html", user=current_user)


@auth.route('/graph', methods=['GET', 'POST'])
@login_required
def graph():
    if request.method == 'POST':
        updates = PileUpdate.query.filter_by(user_id=current_user.id).all()
        updatelist = []
        for i in range(0, len(updates)):
            updatelist.append(updates[i].volume)
            d = str(updates[i].date)
            j = julian(d)
            updatelist.append(j)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        queue = 'filename'
        channel.queue_declare(queue=queue, exclusive=True)
        body = str(updatelist)
        updatelist.clear()
        channel.basic_publish(exchange='', routing_key='data', properties=pika.BasicProperties(reply_to='filename'),
                              body=body)
        print(" [x] Sending data...")
        print(" [x] Waiting for graph filename...")

        # function that runs when a graph is received/consumed
        def on_response(ch, method, properties, body):
            print(" [x] Received '%s'" % body.decode())
            # any image/filename processing can be done here
            global image
            image = body.decode()
            channel.stop_consuming()
            connection.close()

        # start consuming messages
        channel.basic_consume(queue='filename', on_message_callback=on_response, auto_ack=True)
        channel.start_consuming()
        image = 'volume_graph.png'

        return render_template("Graph2.html", user=current_user, image=image)

    return render_template("Graph.html", user=current_user)
