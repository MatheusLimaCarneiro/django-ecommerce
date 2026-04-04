from rest_framework.exceptions import APIException


class BusinessLogicException(APIException):
    status_code = 400
    default_detail = "Business rule violation."
    default_code = "business_error"


class NotFoundException(APIException):
    status_code = 404
    default_detail = "Resource not found."
    default_code = "not_found"


class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"