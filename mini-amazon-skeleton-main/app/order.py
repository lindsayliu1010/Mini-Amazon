from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import current_user
import datetime
from humanize import naturaldate

from .models.product import Product
from .models.purchase import Purchase
from .models.cart import Cart
from .models.order import Order

from flask import Blueprint
from flask_paginate import Pagination, get_page_parameter

bp = Blueprint('order', __name__)

def humanize_time(dt):
    return naturaldate(dt)

@bp.route('/order/<int:oid>')
def get_order(oid):
    # find all the products from all the current user's orders:
    if current_user.is_authenticated:
        order_info = Order.get_order_info(current_user.id, oid)
        purchases_in_order = Order.get_items_in_order(current_user.id, oid)
    else:
        order_info=None
        purchases_in_order = None
        
    search = False
    q = request.args.get('q')
    if q:
        search = True
    
    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 10
    offset = (page - 1) * per_page

    sliced_items = purchases_in_order[offset: offset + per_page]

    pagination = Pagination(page=page, per_page = per_page, offset = offset, total= len(purchases_in_order), search=search, record_name='Items')

    # render the page by adding information to the order.html file
    return render_template('order.html',
                           order_info=order_info,
                           num_items_in_order=len(purchases_in_order),
                           purchases_in_order=sliced_items,
                           humanize_time=humanize_time,
                           pagination=pagination)