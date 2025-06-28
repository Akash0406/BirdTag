from functools import wraps
from flask import session, redirect, url_for, request, jsonify

def login_required(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def anonymous_required(f):
    """Decorator to redirect authenticated users away from auth pages"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function