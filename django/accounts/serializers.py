from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Role, UserRoleMapping

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'country', 'roles', 'is_staff', 'is_active')

    def get_roles(self, obj):
        return [mapping.role.slug for mapping in obj.role_mappings.filter(is_active=True)]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'country', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.get('email', '')
        base_username = email.split('@')[0].replace('.', '_') or 'user'
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}{counter}'
            counter += 1

        user = User.objects.create_user(username=username, password=password, **validated_data)
        student_role, _ = Role.objects.get_or_create(
            slug='student',
            defaults={'name': 'Student', 'description': 'Learner'}
        )
        UserRoleMapping.objects.get_or_create(
            user=user,
            role=student_role,
            defaults={'is_primary': True, 'is_active': True}
        )
        return user
