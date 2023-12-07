from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import request
from flask import redirect, url_for

from .models.inventory import InventoryItem

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('inventory', __name__)

@bp.route('/inventory/<int:sid>')
def inventory(sid):
    # get products in inventory of one seller
    items = InventoryItem.get_all_by_sid(sid)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    offset = (page - 1) * per_page
    sliced_items = items[offset: offset + per_page]
    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(items), record_name='Entries')
    return render_template('inventory.html',
                           items=sliced_items,
                           items_length=len(items),
                           pagination=pagination)

@bp.route('/inventory/add/<int:product_id>/<int:quantity>', methods=['POST'])
def inventory_add(product_id, quantity):
    if current_user.is_authenticated:
        item = InventoryItem.add_item(current_user.id, product_id, quantity)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))

@bp.route('/inventory/delete/<int:product_id>', methods=['POST'])
def inventory_delete(product_id):
    if current_user.is_authenticated:
        item = InventoryItem.delete_item(current_user.id, product_id)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))

@bp.route('/inventory/update', methods=['POST'])
def inventory_update_quantity():
    if current_user.is_authenticated:
        pid = int(request.form.get('pid'))
        quantity = int(request.form.get('quantity'))
        item = InventoryItem.update_inventory(current_user.id, pid, quantity)
    else:
        item = None
        return jsonify({}), 404
    return redirect(url_for('inventory.inventory', sid=current_user.id))