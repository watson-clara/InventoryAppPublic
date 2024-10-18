from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.decorators import role_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    if current_user.role == 'staff':
        return render_template('main/staff_home.html')
    elif current_user.role == 'manager':
        return render_template('main/manager_home.html')
    else:
        return render_template('main/index.html')

@main.route('/staff_home')
@login_required
@role_required('staff')
def staff_home():
    return render_template('main/staff_home.html')
