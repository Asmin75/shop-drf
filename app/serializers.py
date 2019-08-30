from rest_framework import serializers
from .models import User,Post


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

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
                address=self.validated_data['address'],
                phone_number=self.validated_data['phone_number']
            )
            password = self.validated_data['password']
            password2 = self.validated_data['password2']

            if password != password2:
                raise serializers.ValidationError({'password': 'Passwords must match.'})
            user.set_password(password)
            user.save()


class POstSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ('description', 'preffered_location', 'owner', 'delivery_location')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'user_type', 'posts')