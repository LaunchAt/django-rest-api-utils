from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'COGNITO_AUTH_USER_MODEL', settings.AUTH_USER_MODEL)

AWS_COGNITO_CLIENT_ID = getattr(settings, 'AWS_COGNITO_CLIENT_ID', '')

AWS_COGNITO_ENDPOINT = getattr(settings, 'AWS_COGNITO_ENDPOINT', '')

AWS_COGNITO_JWKS = getattr(settings, 'AWS_COGNITO_JWKS', {})
