# app/routes/admin.py
from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/render_admin_login')
def render_admin_login():
    return render_template('admin_login.html')