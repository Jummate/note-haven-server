# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.exceptions import APIException as DRFAPIException


# class APIException(DRFAPIException):
#     def __init__(self, code: str, message: str, status_code=400):
#         self.code = code
#         self.message = message
#         self.status_code = status_code
#         super().__init__(message)


# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)

#     if isinstance(exc, APIException):
#         return Response(
#             {
#                 "code": exc.code,
#                 "message": exc.message
#             },
#             status=exc.status_code
#         )

#     if response is None:
#         return Response({
#             "code": "SERVER_ERROR",
#             "message": "Something went wrong. Please try again."
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     detail = response.data.get("detail")

#     normalized = {
#         "code": "UNKNOWN_ERROR",
#         "message": str(detail) if detail else "An error occurred"
#     }

#     if "Invalid credentials" in str(detail):
#         normalized = {
#             "code": "INVALID_CREDENTIALS",
#             "message": "Invalid credentials"
#         }

#     if "Too many failed attempts" in str(detail):
#         normalized = {
#             "code": "ACCOUNT_LOCKED",
#             "message": "Too many failed attempts. Please try again later."
#         }

#     if response.status_code == 401:
#         normalized = {
#             "code": "UNAUTHORIZED",
#             "message": "Authentication required"
#         }

#     if response.status_code == 403:
#         normalized = {
#             "code": "FORBIDDEN",
#             "message": "Access denied"
#         }

#     if response.status_code == 400 and isinstance(response.data, dict):
#         normalized = {
#             "code": "VALIDATION_ERROR",
#             "message": "Invalid input",
#             "fields": response.data
#         }

#     return Response(normalized, status=response.status_code)




# common/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, ValidationError, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist


from rest_framework.exceptions import APIException as DRFAPIException


class APIException(DRFAPIException):
    def __init__(self, code: str, message: str, status_code=400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def custom_exception_handler(exc, context):
    """
    Handles exceptions and returns a normalized JSON response:
    {
        "code": "...",
        "message": "...",
        "fields": {...}   # only for validation errors
    }
    """
    # 1. Handle our custom APIException
    if isinstance(exc, APIException):
        return Response(
            {"code": exc.code, "message": exc.message},
            status=getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST)
        )

    # 2. Handle DRF built-in exceptions
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {"code": "INVALID_CREDENTIALS", "message": str(exc)},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if isinstance(exc, PermissionDenied):
        return Response(
            {"code": "FORBIDDEN", "message": str(exc)},
            status=status.HTTP_403_FORBIDDEN
        )

    if isinstance(exc, ValidationError):
        return Response(
            {"code": "VALIDATION_ERROR", "message": "Invalid input", "fields": exc.detail},
            status=status.HTTP_400_BAD_REQUEST
        )

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"code": "NOT_FOUND", "message": str(exc)},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. Handle other DRF exceptions
    response = exception_handler(exc, context)
    if response is not None:
        # Normalize response
        detail = response.data.get("detail") if isinstance(response.data, dict) else None
        code = "UNKNOWN_ERROR"
        message = str(detail) if detail else "An error occurred"
        return Response({"code": code, "message": message}, status=response.status_code)

    # 4. Unexpected errors fallback (500)
    return Response(
        {"code": "SERVER_ERROR", "message": "Something went wrong. Please try again."},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

