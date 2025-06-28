import boto3
import hashlib
import hmac
import base64
from botocore.exceptions import ClientError
from config import Config

class CognitoClient:
    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=Config.COGNITO_REGION)
        self.user_pool_id = Config.COGNITO_USER_POOL_ID
        self.client_id = Config.COGNITO_CLIENT_ID
        self.client_secret = Config.COGNITO_CLIENT_SECRET
    
    def _calculate_secret_hash(self, username):
        """Calculate the secret hash for Cognito client authentication"""
        if not self.client_secret:
            return None
        
        message = username + self.client_id
        dig = hmac.new(
            str(self.client_secret).encode('utf-8'),
            msg=str(message).encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(dig).decode()
    
    def sign_up(self, email, password, first_name, last_name):
        """Register a new user"""
        try:
            secret_hash = self._calculate_secret_hash(email)
            
            params = {
                'ClientId': self.client_id,
                'Username': email,
                'Password': password,
                'UserAttributes': [
                    {'Name': 'email', 'Value': email},
                    {'Name': 'given_name', 'Value': first_name},
                    {'Name': 'family_name', 'Value': last_name}
                ]
            }
            
            if secret_hash:
                params['SecretHash'] = secret_hash
            
            response = self.client.sign_up(**params)
            return {'success': True, 'data': response}
            
        except ClientError as e:
            return {'success': False, 'error': e.response['Error']['Message']}
    
    def confirm_sign_up(self, email, confirmation_code):
        """Confirm user registration with verification code"""
        try:
            secret_hash = self._calculate_secret_hash(email)
            
            params = {
                'ClientId': self.client_id,
                'Username': email,
                'ConfirmationCode': confirmation_code
            }
            
            if secret_hash:
                params['SecretHash'] = secret_hash
            
            response = self.client.confirm_sign_up(**params)
            return {'success': True, 'data': response}
            
        except ClientError as e:
            return {'success': False, 'error': e.response['Error']['Message']}
    
    def sign_in(self, email, password):
        """Authenticate user"""
        try:
            secret_hash = self._calculate_secret_hash(email)
            
            params = {
                'ClientId': self.client_id,
                'AuthFlow': 'USER_PASSWORD_AUTH',
                'AuthParameters': {
                    'USERNAME': email,
                    'PASSWORD': password
                }
            }
            
            if secret_hash:
                params['AuthParameters']['SECRET_HASH'] = secret_hash
            
            response = self.client.initiate_auth(**params)
            return {'success': True, 'data': response}
            
        except ClientError as e:
            return {'success': False, 'error': e.response['Error']['Message']}
    
    def get_user(self, access_token):
        """Get user information using access token"""
        try:
            response = self.client.get_user(AccessToken=access_token)
            return {'success': True, 'data': response}
        except ClientError as e:
            return {'success': False, 'error': e.response['Error']['Message']}
    
    def resend_confirmation_code(self, email):
        """Resend confirmation code"""
        try:
            secret_hash = self._calculate_secret_hash(email)
            
            params = {
                'ClientId': self.client_id,
                'Username': email
            }
            
            if secret_hash:
                params['SecretHash'] = secret_hash
            
            response = self.client.resend_confirmation_code(**params)
            return {'success': True, 'data': response}
            
        except ClientError as e:
            return {'success': False, 'error': e.response['Error']['Message']}