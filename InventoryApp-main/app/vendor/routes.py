from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Vendor
from app.extensions import db
from . import vendor
from app.decorators import role_required
from sqlalchemy import or_
from app.models import Item

vendor = Blueprint('vendor', __name__)

@vendor.route('/vendors')
@login_required
@role_required('manager', 'admin')
def vendor_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '')

    query = Vendor.query

    if search_query:
        query = query.filter(or_(
            Vendor.name.ilike(f'%{search_query}%'),
            Vendor.contact_person.ilike(f'%{search_query}%'),
            Vendor.email.ilike(f'%{search_query}%')
        ))

    vendors = query.paginate(page=page, per_page=per_page, error_out=False)
    total_vendors = query.count()

    return render_template('vendor/index.html', 
                           vendors=vendors.items,
                           page=page,
                           per_page=per_page,
                           total_vendors=total_vendors,
                           search_query=search_query,
                           total_pages=vendors.pages,
                           vendors_start=vendors.first,
                           vendors_end=vendors.last)

@vendor.route('/vendors/add', methods=['GET', 'POST'])
@login_required
@role_required('manager', 'admin')
def add_vendor():
    if request.method == 'POST':
        # Handle form submission
        # Add new vendor to database
        new_vendor = Vendor(name=request.form['name'], contact_person=request.form['contact_person'], phone=request.form['phone'], email=request.form['email'], address=request.form['address'])
        db.session.add(new_vendor)
        db.session.commit()
        flash('Vendor added successfully', 'success')
        return redirect(url_for('vendor.vendor_list'))
    return render_template('vendor/add_vendor.html')

@vendor.route('/edit/<int:vendor_id>', methods=['GET', 'POST'])
@login_required
@role_required('manager', 'admin')
def edit_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    if request.method == 'POST':
        vendor.name = request.form['name']
        vendor.contact_person = request.form['contact_person']
        vendor.phone = request.form['phone']
        vendor.email = request.form['email']
        vendor.address = request.form['address']
        db.session.commit()
        flash('Vendor updated successfully', 'success')
        return redirect(url_for('vendor.vendor_list'))
    return render_template('vendor/edit_vendor.html', vendor=vendor)

@vendor.route('/delete/<int:vendor_id>', methods=['GET'])
@login_required
@role_required('manager', 'admin')
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    flash('Vendor deleted successfully', 'success')
    return redirect(url_for('vendor.vendor_list'))

@vendor.route('/view/<int:vendor_id>')
@login_required
def view_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    items = Item.query.filter_by(vendor_id=vendor_id).all()
    return render_template('vendor/view_vendor.html', vendor=vendor, items=items)
