from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from . import db
from flask_login import login_required, current_user
from .models import User, Pile, PileUpdate
from sqlalchemy import delete
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    Stats = Pile.query.filter_by(user_id=current_user.id).first()
    if Stats:
        displayRatio = round(Stats.ratio, 2)
        displayRatio = str(displayRatio) + ":1 Carbon:Nitrogen"
    else:
        displayRatio = "0 because you need to Create a Pile!"

    if request.method == 'POST':
        if Stats:
            ingredient = int(request.form.get('ingredient'))
            volumeAdd = request.form.get('volume')
            if len(volumeAdd) <= 0:
                flash('Volume cannot be zero', category='error')
            else:
                eventCreate = PileUpdate(ratio=ingredient, volume=volumeAdd, user_id=current_user.id)
                db.session.add(eventCreate)
                db.session.commit()
                currentPile = Pile.query.filter_by(user_id=current_user.id).first()
                volume = currentPile.volume
                volumeUpdate = volume + int(volumeAdd)
                carbonAdd = int(ingredient) * int(volumeAdd)
                ratio = currentPile.ratio
                carbonTotal = ratio * volume
                carbonTotal += carbonAdd
                ratioNew = carbonTotal / volumeUpdate
                currentPile.volume = volumeUpdate
                currentPile.ratio = ratioNew
                db.session.commit()
                flash('You added to your pile!', category='success')
                return redirect(url_for('views.home'))
        else:
            flash('You do not have a pile yet, please create a pile', category='error')
    return render_template("home.html", user=current_user, ratio=displayRatio)


@views.route('/delete-pile', methods=['POST'])
def delete_pile():
    piles = Pile.query.filter_by(user_id=current_user.id).all()
    for pile in piles:
        if pile.user_id == current_user.id:
            Pile.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()
        flash('Your pile has been deleted!', category='success')
    return jsonify({})
