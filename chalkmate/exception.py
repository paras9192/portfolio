from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.conf import settings
import sys
import traceback

LOGGEER = settings.LOGGEER


def my_exception_handler(exc, context):
    response = exception_handler(exc, context)
    custom_response = {
        'error': {'message': str(exc)},
        'status': '0',
        'message': 'failed'
    }
    if response is not None:
        if isinstance(exc, ValidationError):
            for err in response.data:
                response.data[err] = response.data[err][0]
            custom_response['error'] = response.data

    _, _, _ = sys.exc_info()
    LOGGEER.debug(traceback.format_exc())
    return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)
    
