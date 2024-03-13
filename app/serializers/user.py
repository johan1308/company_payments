from django.contrib.auth.models import Group
from rest_framework import serializers 
from app.models import Users


class UsersSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    groups_permission=serializers.ListField(required=False)
    permissions = serializers.ListField(default=None, read_only=True)
    

    class Meta:
        model = Users
        fields = (
            'id',
            'name',
            'lastname',
            'identification',
            'phone',
            'email',
            'password',
            'is_active',
            'permissions',
            'groups',
            'groups_permission',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
            },
            'created_by': {
                'write_only': True,
                'required': False,
            },
            'updated_by': {
                'write_only': True,
                'required': False,
            },
        }



    def create(self, validated_data):
        # definiendo variables
        password = None

        # obteniendo lista de los roles que me envia el front
        groups_permission = validated_data.pop('groups_permission')

        # agregando a la lista el permiso basico: 'Basic Gsoft'
        groups_permission.append(35)

        # obteniendo contraseña
        if 'password' in validated_data:
            password = validated_data.pop('password')

        # creando usuario
        instance = super().create(validated_data)

        # si la cotraseña no viene vacia, la vuelvo tipo hash
        if password is not None:
            instance.set_password(password)
            instance.save()

        # obteniendo los grupos
        groups = Group.objects.filter(id__in=groups_permission)
        instance.groups.add(*groups)
        return instance


class UserTokenSerializer(UsersSerializer):
    menus = serializers.ReadOnlyField(default=[])
    groups_permission = serializers.ReadOnlyField()
    
    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields + ('menus',)
