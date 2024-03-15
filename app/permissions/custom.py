from django.utils.translation import gettext as _
from rest_framework import (
    exceptions
)
from app.utils import get_env
from django.http import (
    HttpResponseForbidden,
)
from rest_framework.authentication import (
    TokenAuthentication,
)
from rest_framework.permissions import (
    IsAuthenticated,
    SAFE_METHODS,
    BasePermission,
)
# TODO IMPLEMENTAR AL FINAL
from app.models import (
    DeviceTokenGsoft,
    TokenGsoft,
)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsSelf(IsAuthenticated):
    """
        Permission class to check if the object is the
        same as the requester is
    """

    def has_permission(self, request, view):
        return (
            super().has_permission(request, view)
            and view.is_self
        )


class HasModelPermission(IsAuthenticated):

    ALLOWED_METHODS = [
        'ALL',
        'GET',
        'PUT',
        'PATCH',
        'OPTIONS',
        'HEAD',
        'DELETE',
        'POST'
    ]

    def set_permissions(self, permissions={}):
        if not(permissions):
            permissions = {}

        for method in self.ALLOWED_METHODS:
            value = permissions.get(method)
            if not(isinstance(value, list)):
                permissions[method] = list()

        for method in [
                'GET',
                'PUT',
                'PATCH',
                'OPTIONS',
                'HEAD',
                'DELETE',
                'POST'
        ]:
            permissions[method] = permissions.get(method, []) + permissions.get('ALL', [])  # noqa E501

        self.model_permissions = permissions

    def has_permission(self, request, view):
        self.set_permissions(getattr(view, 'model_permissions', {}))
        return (
            super().has_permission(request, view)
            and (
                request.user.has_perms(self.model_permissions.get(request.method, []))  # noqa E501
            )
        )


def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator

class TokenAuthGsoft(TokenAuthentication):
    model = TokenGsoft
    
    def authenticate(self, request):
        # lista de token que no hace falta validar en el modelo "DeviceTokenGsoft"
        DEVICE_WHITE_LIST = get_env('TOKEN_BANKS').split(',')
        print(DEVICE_WHITE_LIST)
        
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token = str(token[6:])
        except:
            return super().authenticate(request)

        try:
            browser = request.META.get('HTTP_USER_AGENT')
            ip = request.META.get('REMOTE_ADDR')
            user_token = TokenGsoft.objects.get(key=token)
            
            if user_token.key not in DEVICE_WHITE_LIST:
                try:
                    DeviceTokenGsoft.objects.get(
                        token=user_token,
                        ip=ip,
                        browser=browser,
                    )
                except DeviceTokenGsoft.DoesNotExist:
                    return None,HttpResponseForbidden("Forbidden")

        except TokenGsoft.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))
        
        return super().authenticate(request)
