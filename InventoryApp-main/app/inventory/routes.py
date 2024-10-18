from flask import render_template, request, redirect, url_for, flash, current_app, jsonify, send_file
from flask_login import login_required, current_user
from app.models import Item, Vendor
from app.extensions import db
from . import inventory
from flask import current_app
from sqlalchemy import inspect
from sqlalchemy import func
import traceback
from sqlalchemy import inspect
from datetime import datetime
import qrcode
from app.decorators import role_required
import os
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
import io
from flask import session
from sqlalchemy import func

@inventory.route('/items')
@login_required
@role_required('manager', 'admin')
def item_list():
    # Get the current page number from query parameters, default is 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of items per page
    search_query = request.args.get('search', '')
    stock_status = request.args.get('stock_status', '')
    vendor_id = request.args.get('vendor_id', '')
    last_order_date = request.args.get('last_order_date', '')

    # Query items with filters and paginate
    query = Item.query

    filters = []
    if search_query:
        filters.append(Item.description.ilike(f'%{search_query}%'))
    if stock_status:
        filters.append(db.func.lower(Item.stock_status) == stock_status.lower())
    if vendor_id:
        filters.append(Item.vendor_id == vendor_id)
    if last_order_date:
        filters.append(Item.last_order_date >= datetime.strptime(last_order_date, '%Y-%m-%d'))

    sort_column = Item.code  # Default sort by item code

    items = query.filter(*filters).order_by(sort_column).paginate(page=page, per_page=per_page)
    
    current_app.logger.info(f"Fetched {items.total} items")
    current_app.logger.info(f"Applied filters: {filters}")
    for item in items.items:
        current_app.logger.info(f"Item {item.code}: quantity = {item.quantity}, stock_status = {item.stock_status}")

    vendors = Vendor.query.all()
    total_items = items.total
    items_start = (page - 1) * per_page + 1
    items_end = min(page * per_page, total_items)

    # Pass the necessary pagination and filter variables to the template
    return render_template(
        'inventory/index.html',
        items=items,
        page=page,
        total_pages=items.pages,
        search_query=search_query,
        stock_status=stock_status,
        vendor_id=vendor_id,
        last_order_date=last_order_date,
        vendors=vendors,
        total_items=total_items,
        items_start=items_start,
        items_end=items_end
    )

@inventory.route('/items/add', methods=['GET', 'POST'])
@login_required
@role_required('manager', 'admin')
def add_item():
    vendors = Vendor.query.all()
    if request.method == 'POST':
        # Handle form submission
        # Add new item to database
        flash('Item added successfully', 'success')
        return redirect(url_for('inventory.item_list'))
    return render_template('inventory/add_item.html', vendors=vendors)

@inventory.route('/update_quantity/<item_code>', methods=['GET', 'POST'])
@login_required
@role_required('manager', 'admin', 'staff')
def update_quantity(item_code):
    item = Item.query.filter_by(code=item_code).first_or_404()
    if request.method == 'POST':
        new_quantity = request.form.get('new_quantity', type=int)
        if new_quantity is not None:
            item.quantity = new_quantity
            item.quantity_updated_at = datetime.utcnow()
            item.quantity_updater = current_user
            db.session.commit()
            session.pop('_flashes', None)  # Clear all existing flash messages
            flash('Quantity updated successfully.', 'success')
            if current_user.role == 'staff':
                return redirect(url_for('main.staff_home'))
            else:
                return redirect(url_for('inventory.item_list'))
    return render_template('inventory/update_quantity.html', item=item)

@inventory.route('/reset_inventory', methods=['POST'])
@login_required
@role_required('admin')
def reset_inventory():
    try:
        # Reset all quantities to 0 and remove QR codes
        Item.query.update({Item.quantity: 0, Item.qr_code: None})
        db.session.commit()
        flash('All item quantities have been reset to 0 and QR codes removed.', 'success')
    except Exception as e:
        current_app.logger.error(f"Error resetting inventory: {str(e)}")
        db.session.rollback()
        flash('An error occurred while resetting the inventory.', 'error')
    
    return redirect(url_for('inventory.item_list'))

@inventory.route('/edit/<string:item_code>', methods=['GET', 'POST'])
@login_required
@role_required('manager', 'admin')
def edit_item(item_code):
    item = Item.query.get_or_404(item_code)
    vendors = Vendor.query.all()
    if request.method == 'POST':
        item.description = request.form['description']
        item.minimum_quantity = int(request.form['minimum_quantity'])
        item.max_quantity = int(request.form['max_quantity'])
        item.vendor_id = int(request.form['vendor_id'])
        db.session.commit()
        flash('Item updated successfully', 'success')
        return redirect(url_for('inventory.item_list'))
    return render_template('inventory/edit_item.html', item=item, vendors=vendors)

@inventory.route('/generate_qr_code/<item_code>')
def generate_qr_code(item_code):
    item = Item.query.filter_by(code=item_code).first_or_404()
    qr = qrcode.QRCode(version=1, box_size=10, border=0)
    qr.add_data(f"{request.host_url}inventory/update_quantity/{item_code}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return render_template('inventory/qr_code.html', item=item, qr_code=base64.b64encode(img_io.getvalue()).decode())

@inventory.route('/view/<item_code>')
@login_required
def view_item(item_code):
    item = Item.query.get_or_404(item_code)
    return render_template('inventory/view_item.html', item=item)

@inventory.route('/just_ordered/<item_code>', methods=['GET', 'POST'])
@login_required
def just_ordered(item_code):
    item = Item.query.get_or_404(item_code)
    if request.method == 'POST':
        order_quantity = int(request.form['order_quantity'])
        
        
        item.update_order_info(order_quantity)
        db.session.commit()
        
        flash('Order information updated successfully.', 'success')
        return redirect(url_for('inventory.item_list'))
    
    return render_template('inventory/just_ordered.html', item=item)

@inventory.route('/print_inventory')
@login_required
def print_inventory():
    search_query = request.args.get('search', '')
    stock_status = request.args.get('stock_status', '')
    vendor_id = request.args.get('vendor_id', '')
    query = Item.query
    if search_query:
        query = query.filter(Item.description.ilike(f'%{search_query}%') | Item.code.ilike(f'%{search_query}%'))
    if stock_status:
        query = query.filter(func.lower(Item.stock_status) == func.lower(stock_status))
    
    if vendor_id:
        query = query.filter(Item.vendor_id == vendor_id)
    items = query.all()
    return render_template('inventory/print_inventory.html', 
                           items=items, 
                           search_query=search_query, 
                           stock_status=stock_status, 
                           vendor_id=vendor_id)

def get_filtered_items():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    stock_status = request.args.get('stock_status', '')
    vendor_id = request.args.get('vendor_id', '')
    last_order_date = request.args.get('last_order_date', '')

    query = Item.query

    if search_query:
        query = query.filter(Item.code.ilike(f'%{search_query}%') | Item.description.ilike(f'%{search_query}%'))
    if stock_status:
        query = query.filter(Item.stock_status == stock_status)
    if vendor_id:
        query = query.filter(Item.vendor_id == vendor_id)
    if last_order_date:
        query = query.filter(Item.last_order_date >= last_order_date)

    return query.order_by(Item.code).all()

@inventory.route('/select_qr_codes', methods=['GET'])
@login_required
def select_qr_codes():
    items = Item.query.order_by(Item.code).all()
    return render_template('inventory/select_qr_codes.html', items=items)

@inventory.route('/print_qr_codes', methods=['POST'])
@login_required
def print_qr_codes():
    selected_items = request.form.getlist('selected_items')
    items = Item.query.filter(Item.code.in_(selected_items)).all()
    qr_codes = []
    for item in items:
        qr = qrcode.QRCode(version=1, box_size=10, border=0)
        qr.add_data(f"{request.host_url}inventory/update_quantity/{item.code}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qr_code = base64.b64encode(buffered.getvalue()).decode()
        qr_codes.append({'item': item, 'qr_code': qr_code})
    return render_template('inventory/print_qr_codes.html', qr_codes=qr_codes)

@inventory.route('/reorders')
@login_required
def reorders():
    low_stock_items = Item.query.filter(Item.stock_status == 'Low Stock').all()
    return render_template('inventory/reorders.html', items=low_stock_items)
