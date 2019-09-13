from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.tokens import TokenGenerator
from .models import User, Post


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['user_type', 'email', 'username', 'password', 'password2', 'address', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def save(self):
            user = User(
                user_type=self.validated_data['user_type'],
                username=self.validated_data['username'],
                email=self.validated_data['email'],
                address=self.validated_data['address'],
                phone_number=self.validated_data['phone_number']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({'password': 'Passwords must match.'})
            user.set_password(password)
            user.save()


class UserPasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
            instance.save()
            return instance


class POstSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    status = Post.status

    class Meta:
        model = Post
        fields = ('url', 'id', 'status', 'description', 'preffered_location', 'owner', 'delivery_location')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'user_type', 'phone_number', 'posts')


class CustomPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomPasswordResetDoneSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()


class CustomPasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password1 = serializers.CharField()