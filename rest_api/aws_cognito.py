import json
import logging

import jwt
from django.apps import apps
from jwt.algorithms import RSAAlgorithm
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from .settings import (
    AUTH_USER_MODEL,
    AWS_COGNITO_CLIENT_ID,
    AWS_COGNITO_ENDPOINT,
    AWS_COGNITO_JWKS,
)

logger = logging.getLogger(__name__)

UserModel = apps.get_model(AUTH_USER_MODEL, require_ready=False)


class AmazonCognitoAuthentication(TokenAuthentication):
    keyword = 'Bearer'
    model = UserModel
    jwks = AWS_COGNITO_JWKS['keys']

    def get_data(self, token):
        header_kid = jwt.get_unverified_header(token).get('kid')
        web_key = next((k for k in self.jwks if k['kid'] == header_kid), None)
        return jwt.decode(
            token,
            key=RSAAlgorithm.from_jwk(json.dumps(web_key)),
            audience=AWS_COGNITO_CLIENT_ID,
            issuer=AWS_COGNITO_ENDPOINT,
            algorithms=['RS256'],
        )

    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            data = self.get_data(key)

        except Exception as error:
            logger.error(f'{type(error)}: {error}')
            raise exceptions.AuthenticationFailed from error

        assert hasattr(model.objects, 'authenticate_user')
        user = model.objects.authenticate_user(data)
        return user, None
