import json

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from . import db

from .models import Asset, User

views = Blueprint('views', __name__)

top_assets_cache = {}
def update_top_assets_cache(user_id):
    user = User.query.filter_by(id=user_id).first()
    assets = Asset.query.filter_by(owner_id=user_id).order_by(Asset.price.desc()).limit(5).all()
    list=[]
    for asset in assets:
        list.append([asset.id,  asset.name,  asset.description, asset.price,asset.owner_id])
    top_assets_cache[user.id] =list



@views.route('/')
@login_required
def home():
    user_assets = Asset.query.filter_by(owner_id=current_user.id).all()
    return render_template("home.html", user=current_user, assets=user_assets)


@views.route('/top')
@login_required
def top():
    user_assets = Asset.query.filter_by(owner_id=current_user.id).order_by(Asset.price.desc()).limit(5).all()
    return render_template("top.html", user=current_user, assets=user_assets)


@views.route('/add-asset', methods=['POST'])
@login_required
def add_asset():
    data = request.get_json()
    name = data['name']  # Поле для имени ассета
    description = data['description']  # Поле для описания ассета
    price = data['price']

    update_top_assets_cache(current_user.id)

    if len(name) < 1:
        flash('Asset data is too short!', category='error')
    else:
        new_asset = Asset(name=name, description=description, price=price, owner_id=current_user.id)
        db.session.add(new_asset)
        db.session.commit()
        flash('Asset added!', category='success')

    return redirect(url_for('views.home'))


@views.route('/delete-asset', methods=['POST'])
@login_required
def delete_asset():
    if request.method == 'POST':
        asset_id = json.loads(request.data)['assetId']
        asset = Asset.query.get(asset_id)
        if asset and asset.owner_id == current_user.id:
            db.session.delete(asset)
            db.session.commit()
    update_top_assets_cache(current_user.id)
    return jsonify({})

@views.route('/updating')
@login_required
def updating():
    user_assets = Asset.query.filter_by(owner_id=current_user.id).all()
    return render_template("updating.html", user=current_user, assets=user_assets)
@views.route('/update-asset', methods=['POST'])
@login_required
def update_asset():
    data = request.get_json()
    id = data['id']
    name = data['name']  # Поле для имени ассета
    description = data['description']  # Поле для описания ассета
    price = data['price']
    if len(name) < 1:
        flash('Asset data is too short!', category='error')
    else:
        asset = Asset.query.filter_by(id=id).first()
        asset.name = name
        asset.description = description
        asset.price = price
        db.session.commit()
        flash('Asset updating!', category='success')

    return redirect(url_for('views.updating'))


