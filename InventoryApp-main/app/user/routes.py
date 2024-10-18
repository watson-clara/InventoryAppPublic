from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.user import User
from app import db
from app.decorators import role_required
from app.models.item import Item

user = Blueprint('user', __name__)

@user.route('/users')
@login_required
@role_required( 'admin')
def user_list():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    
    query = User.query
    if search_query:
        query = query.filter(User.username.ilike(f'%{search_query}%') | User.email.ilike(f'%{search_query}%'))
    
    users = query.paginate(page=page, per_page=10)
    total_users = query.count()
    users_start = (page - 1) * 10 + 1
    users_end = min(users_start + 9, total_users)
    total_pages = (total_users + 9) // 10

    return render_template('user/index.html', users=users, search_query=search_query,
                           page=page, total_pages=total_pages, users_start=users_start,
                           users_end=users_end, total_users=total_users)

@user.route('/users/add', methods=['GET', 'POST'])
@login_required
@role_required( 'admin')
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        
        flash('User added successfully', 'success')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/add_user.html')

@user.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required( 'admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.role = request.form['role']
        
        if request.form['password']:
            user.set_password(request.form['password'])
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('user.user_list'))
    
    return render_template('user/edit_user.html', user=user)

@user.route('/users/delete/<int:user_id>')
@login_required
@role_required( 'admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('user.user_list'))

@user.route('/view/<int:user_id>')
@login_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    user.updated_items = Item.query.filter_by(quantity_last_updated_by=user_id).all()
    return render_template('user/view_user.html', user=user)
