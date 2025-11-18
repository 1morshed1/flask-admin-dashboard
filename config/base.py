# config/base.py

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:

    """Base configuration"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://localhost/admin_dashboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    )
    # CORS
    CORS_HEADERS = 'Content-Type'
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Frontend URL for SSO redirects
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
    
    # SAML Configuration
    SAML_ENABLED = os.environ.get('SAML_ENABLED', 'False').lower() == 'true'
    SAML_SP_BASE_URL = os.environ.get('SAML_SP_BASE_URL', 'http://localhost:5000')
    SAML_IDP_ENTITY_ID = os.environ.get('SAML_IDP_ENTITY_ID', '')
    SAML_IDP_SSO_URL = os.environ.get('SAML_IDP_SSO_URL', '')
    SAML_IDP_SLO_URL = os.environ.get('SAML_IDP_SLO_URL', '')
    SAML_IDP_X509_CERT = os.environ.get('SAML_IDP_X509_CERT', '')
    SAML_DEBUG = os.environ.get('SAML_DEBUG', 'True').lower() == 'true'
    # Security settings (defaults match settings.json example: wantAssertionsSigned=True)
    SAML_WANT_ASSERTIONS_SIGNED = os.environ.get('SAML_WANT_ASSERTIONS_SIGNED', 'True').lower() == 'true'
    SAML_WANT_MESSAGES_SIGNED = os.environ.get('SAML_WANT_MESSAGES_SIGNED', 'False').lower() == 'true'
    SAML_AUTHN_REQUESTS_SIGNED = os.environ.get('SAML_AUTHN_REQUESTS_SIGNED', 'False').lower() == 'true'
    # Default role for auto-provisioned SSO users
    SAML_DEFAULT_ROLE = os.environ.get('SAML_DEFAULT_ROLE', 'user')

class DevelopmentConfig(Config):

    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):

    """Production configuration"""
    DEBUG = False
    # In production, set SAML strict mode
    SAML_STRICT = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}