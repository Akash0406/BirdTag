from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_cors import CORS
from config import config
from auth.cognito_client import CognitoClient
from auth.decorators import login_required, anonymous_required
import os

def create_app(config_name=None):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app)
    
    return app

# Create the Flask application
app = create_app()

# Initialize Cognito client
cognito_client = CognitoClient()

# Auth Routes
@app.route('/signup', methods=['GET', 'POST'])
@anonymous_required
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        
        if not all([email, password, first_name, last_name]):
            return jsonify({'success': False, 'error': 'All fields are required'})
        
        result = cognito_client.sign_up(email, password, first_name, last_name)
        
        if result['success']:
            return jsonify({
                'success': True, 
                'message': 'Registration successful. Please check your email for confirmation code.'
            })
        else:
            return jsonify({'success': False, 'error': result['error']})
    
    return render_template('auth/signup.html')

@app.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password are required'})
        
        result = cognito_client.sign_in(email, password)
        
        if result['success']:
            # Store user session
            auth_result = result['data']['AuthenticationResult']
            access_token = auth_result['AccessToken']
            
            # Get user info
            user_result = cognito_client.get_user(access_token)
            if user_result['success']:
                user_attributes = {}
                for attr in user_result['data']['UserAttributes']:
                    user_attributes[attr['Name']] = attr['Value']
                
                session['user'] = {
                    'email': user_attributes.get('email'),
                    'given_name': user_attributes.get('given_name'),
                    'family_name': user_attributes.get('family_name'),
                    'access_token': access_token,
                    'refresh_token': auth_result.get('RefreshToken'),
                    'id_token': auth_result.get('IdToken')
                }
                
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'error': 'Failed to get user information'})
        else:
            return jsonify({'success': False, 'error': result['error']})
    
    return render_template('auth/login.html')

@app.route('/confirm', methods=['GET', 'POST'])
@anonymous_required
def confirm():
    if request.method == 'POST':
        email = request.form.get('email')
        confirmation_code = request.form.get('confirmationCode')
        
        if not email or not confirmation_code:
            return jsonify({'success': False, 'error': 'Email and confirmation code are required'})
        
        result = cognito_client.confirm_sign_up(email, confirmation_code)
        
        if result['success']:
            return jsonify({'success': True, 'message': 'Account confirmed successfully'})
        else:
            return jsonify({'success': False, 'error': result['error']})
    
    return render_template('auth/confirm.html')

@app.route('/resend-code', methods=['POST'])
@anonymous_required
def resend_code():
    email = request.form.get('email')
    
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'})
    
    result = cognito_client.resend_confirmation_code(email)
    
    if result['success']:
        return jsonify({'success': True, 'message': 'Confirmation code resent successfully'})
    else:
        return jsonify({'success': False, 'error': result['error']})

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('login'))

# Main Application Routes
@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/feed')
@login_required
def feed():
    return render_template('feed.html')

@app.route('/upload')
@login_required
def upload():
    return render_template('upload.html')

@app.route('/search')
@login_required
def search():
    return render_template('search.html')

@app.route('/subscribe')
@login_required
def subscribe():
    return render_template('subscribe.html')

# API Routes (for later implementation)
@app.route('/api/upload', methods=['POST'])
@login_required
def api_upload():
    # This will be implemented later for S3 uploads
    return jsonify({'success': True, 'message': 'Upload endpoint ready'})

@app.route('/api/search', methods=['GET', 'POST'])
@login_required
def api_search():
    # This will be implemented later for DynamoDB searches
    return jsonify({'success': True, 'message': 'Search endpoint ready'})

@app.route('/api/tags', methods=['POST', 'DELETE'])
@login_required
def api_tags():
    # This will be implemented later for tag management
    return jsonify({'success': True, 'message': 'Tags endpoint ready'})

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'environment': app.config['ENV'],
        'debug': app.config['DEBUG']
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    
    app.run(
        debug=app.config['DEBUG'], 
        host=host, 
        port=port
    )