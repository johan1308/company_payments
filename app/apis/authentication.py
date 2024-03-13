from django.utils.translation import gettext as _
from datetime import datetime
from rest_framework import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.sessions.models import Session
from app.serializers import UserTokenSerializer
from rest_framework.response import Response
from rest_framework import (
    status,
    generics,
    serializers
)
from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)
from app.models.authentication import (
    TokenGsoft,
    DeviceTokenGsoft,
)

class Login(ObtainAuthToken):
    """
    Iniciar session, no hace falta tener permisos o esta logueado.
    """

    @extend_schema(
        tags=["Authentication"],
        request=inline_serializer(
            name='Login',
            fields={
                'email': serializers.CharField(),
                'password': serializers.CharField(),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        if 'email' in request.data:
            request.data['username'] = request.data['email']
        
        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})

        if login_serializer.is_valid():
            # login serializer retorna user en validated_data
            user = login_serializer.validated_data['user']
            if user:
                token, created = TokenGsoft.objects.get_or_create(user=user)
                user_serializer = UserTokenSerializer(user)
                if not created:
                    token.delete()  
                    token = TokenGsoft.objects.create(user=user)

                browser = request.META.get('HTTP_USER_AGENT')
                ip = request.META.get('REMOTE_ADDR')
                DeviceTokenGsoft.objects.create(
                    token=token,
                    ip=ip,
                    browser=browser,
                )
                return Response({
                    'token': token.key,
                    'user': user_serializer.data,
                    'message': _('Successful login.')
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': _('This user is not active!')},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': _('Incorrect email or password!')},
                            status=status.HTTP_400_BAD_REQUEST)


class Logout(generics.GenericAPIView):
    """
    Cerrar session, consultar la ruta con el token en el header.
    """

    @extend_schema(tags=["Authentication"])
    def get(self, request, *args, **kwargs):
        try:
            token = str(request.headers['Authorization'])[6:]
            token = Token.objects.filter(key=token).first()
            print(token)

            if token:
                user = token.user
                # eliminar todas las sesiones para el usuario
                all_sessions = Session.objects.filter()
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == session_data.get('_auth_user_id'):
                            session.delete()
                token.delete()

                session_message = _('Session deleted successfully!')
                token_message = _('Token removed.')
                return Response({
                    'token_message': token_message,
                    'session_message': session_message
                    }, status=status.HTTP_200_OK
                )

            return Response({
                'message': _('A user with these credentials could not be found.')
            }, status=status.HTTP_400_BAD_REQUEST)

        except LookupError:
            return Response({
                'messager': _('No token was found in the request.')},
                status=status.HTTP_409_CONFLICT
            )