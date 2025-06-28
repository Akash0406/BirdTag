import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', os.urandom(24))
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'production')
    
    # AWS Cognito Configuration
    COGNITO_REGION = os.getenv('COGNITO_REGION', 'us-east-1')
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID', 'us-east-1_lewa3Lb76')
    COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID', '7q0tnne6pl79p8tkmhvmd17ia7')
    COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET', '')
    COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN', 'https://cognito-idp.us-east-1.amazonaws.com')
    
    # Application URLs
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'https://d84l1y8p4kdic.cloudfront.net')
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # AWS General Configuration
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # S3 Configuration
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'birdtag-media-bucket')
    S3_THUMBNAIL_BUCKET = os.getenv('S3_THUMBNAIL_BUCKET', 'birdtag-thumbnails')
    
    # DynamoDB Configuration
    DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'BirdTagFiles')
    DYNAMODB_USERS_TABLE = os.getenv('DYNAMODB_USERS_TABLE', 'BirdTagUsers')
    
    # Lambda Configuration
    LAMBDA_FUNCTION_NAME = os.getenv('LAMBDA_FUNCTION_NAME', 'BirdTagAnalyzer')
    LAMBDA_THUMBNAIL_FUNCTION = os.getenv('LAMBDA_THUMBNAIL_FUNCTION', 'BirdTagThumbnailGenerator')
    
    # SNS Configuration
    SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', '')
    
    # Database Configuration (fallback to SQLite)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///birdtag.db')
    
    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/birdtag.log')
    
    # Security Configuration
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '104857600'))  # 100MB
    MAX_FILES_PER_UPLOAD = int(os.getenv('MAX_FILES_PER_UPLOAD', '10'))
    
    # AI Model Configuration
    MODEL_ENDPOINT = os.getenv('MODEL_ENDPOINT', '')
    MODEL_CONFIDENCE_THRESHOLD = float(os.getenv('MODEL_CONFIDENCE_THRESHOLD', '0.75'))
    
    # Cache Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
    
    # Feature Flags
    ENABLE_SOCIAL_FEATURES = os.getenv('ENABLE_SOCIAL_FEATURES', 'true').lower() == 'true'
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'true').lower() == 'true'
    ENABLE_ANALYTICS = os.getenv('ENABLE_ANALYTICS', 'true').lower() == 'true'
    ENABLE_FILE_SHARING = os.getenv('ENABLE_FILE_SHARING', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    # Use in-memory database for testing
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}