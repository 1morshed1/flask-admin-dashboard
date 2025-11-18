# config/saml_settings.py
import os

def get_saml_settings():
    """
    Get SAML configuration settings.
    
    Configure these settings based on your Identity Provider (IdP):
    - For Okta: Get these values from your Okta SAML app settings
    - For Azure AD: Get from Azure portal
    - For other IdPs: Check their SAML documentation
    """
    
    # Your application's URL (Service Provider)
    sp_base_url = os.getenv('SAML_SP_BASE_URL', 'http://localhost:5000')
    
    # Security settings - wantAssertionsSigned should be True in production (as shown in settings.json example)
    want_assertions_signed = os.getenv('SAML_WANT_ASSERTIONS_SIGNED', 'True').lower() == 'true'
    want_messages_signed = os.getenv('SAML_WANT_MESSAGES_SIGNED', 'False').lower() == 'true'
    
    return {
        'strict': False,  # Set to True in production for stricter validation
        'debug': os.getenv('SAML_DEBUG', 'True').lower() == 'true',
        
        # Service Provider (Your Application)
        'sp': {
            'entityId': f"{sp_base_url}/api/auth/saml/metadata",
            'assertionConsumerService': {
                'url': f"{sp_base_url}/api/auth/saml/acs",
                'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
            },
            'singleLogoutService': {
                'url': f"{sp_base_url}/api/auth/saml/sls",
                'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
            },
            'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
        },
        
        # Identity Provider (Okta, Azure AD, etc.)
        'idp': {
            'entityId': os.getenv('SAML_IDP_ENTITY_ID', ''),
            'singleSignOnService': {
                'url': os.getenv('SAML_IDP_SSO_URL', ''),
                'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
            },
            'singleLogoutService': {
                'url': os.getenv('SAML_IDP_SLO_URL', ''),
                'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
            },
            'x509cert': os.getenv('SAML_IDP_X509_CERT', ''),
        },
        
        # Security settings
        'security': {
            'nameIdEncrypted': False,
            'authnRequestsSigned': os.getenv('SAML_AUTHN_REQUESTS_SIGNED', 'False').lower() == 'true',
            'logoutRequestSigned': False,
            'logoutResponseSigned': False,
            'signMetadata': False,
            'wantMessagesSigned': want_messages_signed,
            'wantAssertionsSigned': want_assertions_signed,  # Default True for security (matches settings.json)
            'wantAssertionsEncrypted': False,
            'wantNameId': True,
            'wantNameIdEncrypted': False,
            'requestedAuthnContext': True,
            'signatureAlgorithm': 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256',
            'digestAlgorithm': 'http://www.w3.org/2001/04/xmlenc#sha256',
        }
    }


def prepare_flask_request(request):
    """
    Prepare Flask request for SAML library.
    
    Args:
        request: Flask request object
        
    Returns:
        dict: Formatted request data for python3-saml
    """
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': request.environ.get('SERVER_PORT'),
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

