from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, views
from rest_framework.response import Response


def exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}

        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header

        if getattr(exc, 'wait', None):
            headers['Retry-After'] = f'{exc.wait}'

        if isinstance(exc.detail, list):
            data = {
                'code': 'list_error',
                'detail': exc.detail,
                'status_code': exc.status_code,
            }

        if isinstance(exc.detail, dict):
            data = {
                'code': 'dict_error',
                'detail': exc.detail,
                'status_code': exc.status_code,
            }

        else:
            data = {
                'code': exc.detail.code,
                'message': exc.detail,
                'detail': exc.detail,
                'status_code': exc.status_code,
            }

        views.set_rollback()

        return Response(data, status=exc.status_code, headers=headers)

    return None
