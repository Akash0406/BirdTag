# 🐦 BirdTag - AI-Powered Bird Media Organizer

BirdTag is a modern, serverless application that helps bird researchers and enthusiasts organize, tag, and discover their bird media collection using AI-powered species detection.

## 🌟 Features

- **🔐 Secure Authentication** - AWS Cognito integration with email verification
- **🤖 AI Species Detection** - Automatic bird identification in photos, videos, and audio
- **☁️ Cloud Storage** - Secure media storage with AWS S3
- **🔍 Advanced Search** - Find media by species, tags, or metadata
- **👥 Social Features** - Community feed and researcher collaboration
- **📊 Analytics** - Track your discoveries and research progress
- **🔔 Notifications** - Stay updated on new discoveries and research
- **📱 Responsive Design** - Beautiful, mobile-friendly interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- AWS Account with Academy access
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd birdtag
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` file with your AWS Cognito credentials:

   ```bash
   # Required: Update these with your AWS Cognito details
   COGNITO_USER_POOL_ID=your-user-pool-id
   COGNITO_CLIENT_ID=your-client-id
   COGNITO_CLIENT_SECRET=your-client-secret

   # Generate a secure secret key
   FLASK_SECRET_KEY=your-super-secret-key-here
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser to `http://localhost:5000`
   - Sign up with your email address
   - Check your email for the confirmation code
   - Complete verification and start using BirdTag!

## 🏗️ Architecture

BirdTag follows a serverless architecture pattern:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   AWS Services  │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Authentication│◄──►│ • Cognito       │
│ • TailwindCSS   │    │ • File Upload   │    │ • S3            │
│ • Responsive    │    │ • Search API    │    │ • Lambda        │
│ • Modern UI     │    │ • User Mgmt     │    │ • DynamoDB      │
└─────────────────┘    └─────────────────┘    │ • SNS           │
                                              └─────────────────┘
```

## 📁 Project Structure

```
birdtag/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in git)
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── auth/                    # Authentication module
│   ├── __init__.py
│   ├── cognito_client.py    # AWS Cognito integration
│   └── decorators.py        # Route protection
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── dashboard.html      # User dashboard
│   ├── profile.html        # User profile management
│   ├── feed.html          # Community feed
│   ├── upload.html        # File upload interface
│   ├── search.html        # Search functionality
│   ├── subscribe.html     # Notification settings
│   └── auth/              # Authentication templates
│       ├── login.html
│       ├── signup.html
│       └── confirm.html
└── logs/                  # Application logs
```

## 🛠️ Environment Variables

### Required Variables

```bash
# AWS Cognito (Required)
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-client-id
COGNITO_CLIENT_SECRET=your-client-secret

# Flask Security (Required)
FLASK_SECRET_KEY=your-super-secret-key
```

### Optional Variables

```bash
# AWS Services
S3_BUCKET_NAME=birdtag-media-bucket
DYNAMODB_TABLE_NAME=BirdTagFiles
LAMBDA_FUNCTION_NAME=BirdTagAnalyzer

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
MAX_FILE_SIZE=104857600  # 100MB
MAX_FILES_PER_UPLOAD=10

# Feature Flags
ENABLE_SOCIAL_FEATURES=true
ENABLE_NOTIFICATIONS=true
ENABLE_ANALYTICS=true
```

## 🔧 AWS Setup Guide

### 1. AWS Cognito User Pool

1. **Create User Pool**

   - Go to AWS Cognito Console
   - Create a new User Pool
   - Configure sign-in options (email)
   - Set password policy
   - Enable email verification

2. **Create App Client**

   - Add an app client to your user pool
   - Generate client secret
   - Configure OAuth flows
   - Set callback URLs

3. **Update .env file**
   ```bash
   COGNITO_USER_POOL_ID=us-east-1_xxxxxxxxx
   COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
   COGNITO_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 2. Future AWS Services Setup

For full functionality, you'll need to set up:

- **S3 Buckets** - Media storage and thumbnails
- **Lambda Functions** - AI processing and thumbnails
- **DynamoDB Tables** - Metadata and search indices
- **SNS Topics** - Notifications
- **API Gateway** - REST API endpoints

## 🎨 UI/UX Features

### Design System

- **Color Palette**: Bird-themed blues and nature greens
- **Typography**: Inter font for clean readability
- **Animations**: Smooth transitions and hover effects
- **Glass Morphism**: Modern translucent card designs
- **Responsive**: Mobile-first approach

### Key UI Components

- **Navigation**: Fixed header with user profile
- **Dashboard**: Stats, recent uploads, activity feed
- **Upload**: Drag & drop with progress tracking
- **Search**: Advanced filtering and results display
- **Feed**: Social posts with species tagging
- **Profile**: Comprehensive user management

## 🔒 Security Features

- **Authentication**: AWS Cognito with MFA support
- **Session Management**: Secure server-side sessions
- **Input Validation**: Form validation and sanitization
- **File Upload**: Type and size restrictions
- **CORS**: Configured for secure API access
- **Environment Variables**: Sensitive data protection

## 🚀 Deployment

### Development

```bash
python app.py
```

### Production

```bash
# Set production environment
export FLASK_ENV=production
export FLASK_DEBUG=False

# Use a WSGI server like Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker (Optional)

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📊 Monitoring & Logging

- **Application Logs**: Configured in `logs/birdtag.log`
- **Error Handling**: Custom error pages and logging
- **Health Check**: `/health` endpoint for monitoring
- **Performance**: Request timing and metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

### Phase 1 (Current) ✅

- [x] Authentication system
- [x] Modern UI/UX design
- [x] Basic file upload interface
- [x] User profile management
- [x] Community feed mockup

### Phase 2 (Next)

- [ ] S3 integration for file storage
- [ ] Lambda functions for AI processing
- [ ] DynamoDB for metadata storage
- [ ] Real-time search functionality
- [ ] Thumbnail generation

### Phase 3 (Future)

- [ ] Advanced AI models
- [ ] Real-time notifications
- [ ] Mobile app
- [ ] Advanced analytics
- [ ] API for third-party integrations

## 🐛 Troubleshooting

### Common Issues

1. **Cognito Authentication Errors**

   ```bash
   # Check your credentials in .env
   # Ensure user pool and client are configured correctly
   # Verify email verification is enabled
   ```

2. **Import Errors**

   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Environment Variables Not Loading**
   ```bash
   # Ensure .env file exists and is properly formatted
   # Check that python-dotenv is installed
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Development Team**: Monash University FIT5225 Students
- **Project Advisor**: Course Instructors
- **Special Thanks**: Monash Birdy Buddies (MBB) for inspiration

## 📞 Support

- **Documentation**: Check this README and code comments
- **Issues**: Open a GitHub issue
- **Questions**: Contact the development team

---

**Happy Bird Watching! 🐦✨**
