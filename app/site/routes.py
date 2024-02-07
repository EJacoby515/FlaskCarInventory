from flask import Blueprint, render_template, url_for, redirect, flash, request
from app.forms import UserInventoryForm, AddInventory, UpdateCar
from app.models import Inventory, db
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField

site = Blueprint('site',  __name__, template_folder='site_templates')


@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile.html')
def profile():
    return render_template('profile.html')


@site.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = AddInventory()

    if form.validate_on_submit():
        make = form.make.data
        model = form.model.data
        year = form.year.data
        color = form.color.data

        user_token = current_user.token

        inventory_item = Inventory(make=make, model=model, year=year, color=color, user_token=user_token)

        db.session.add(inventory_item)
        db.session.commit()

        return redirect(url_for('site.inventory'))

    return render_template('inventory.html', form=form)

@site.route('/update_inventory/<id>', methods=['GET', 'POST'])
def update_inventory(id):
    inventory_item = Inventory.query.get(id)

    if inventory_item:
        if request.method == 'POST':
            inventory_item.make = request.form['make']
            inventory_item.model = request.form['model']
            inventory_item.year = request.form['year']
            inventory_item.color = request.form['color']

            db.session.commit()


            flash(f'Inventory item {inventory_item.model} updated successfully!', 'success')
            return redirect(url_for('site.inventory'))

        return render_template('update_inventory.html', car=inventory_item, form = UpdateCar())

    else:
        flash(f'Inventory item with ID {id} not found!', 'error')
        return redirect(url_for('site.inventory'))


@site.route('/delete_inventory/<id>')
def delete_inventory(id):
    try:
        inventory_item = Inventory.query.get(id)

        if inventory_item:
            db.session.delete(inventory_item)
            db.session.commit()

            flash(f'Successfully deleted {inventory_item.model} from your inventory', 'delete-success')
        else:
            flash('Inventory item not found', 'delete-error')

    except Exception as e:
        flash(f'Error deleting inventory item: {str(e)}', 'delete-error')

    return redirect(url_for('site.inventory'))
