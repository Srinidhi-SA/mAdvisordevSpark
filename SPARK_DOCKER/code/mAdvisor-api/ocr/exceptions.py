from builtins import str
from rest_framework.views import exception_handler
from  rest_framework.response import Response


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = errors
        response.data['status'] = False
        response.data['message'] = 'failed'

        response.data['exception'] = str(exc)

    return response


def creation_failed_exception(err):
    response = Response()
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = "Creation failed"
        response.data['status'] = False
        response.data['message'] = 'failed'

        response.data['exception'] = err

    return response

def retrieve_failed_exception(err):
    response = Response()
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = "Retrieve failed"
        response.data['status'] = "Not Found"
        response.data['message'] = 'failed'
        response.data['data'] = 'Requested item not found.'

        response.data['exception'] = err

    return response

def update_failed_exception(err):
    response = Response()
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = "Update failed"
        response.data['status'] = False
        response.data['message'] = 'failed'

        response.data['exception'] = err

    return response

def deleted_failed_exception(err):
    response = Response()
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = "Deleted failed"
        response.data['status'] = False
        response.data['message'] = 'failed'

        response.data['exception'] = err

    return response

def sharing_failed_exception(err):
    response = Response()
    if response is not None:
        response.data = {}
        errors = []
        for field, value in list(response.data.items()):
            errors.append("{} : {}".format(field, " ".join(value)))

        response.data['errors'] = "Sharing failed"
        response.data['status'] = False
        response.data['message'] = 'failed'

        response.data['exception'] = err

    return response