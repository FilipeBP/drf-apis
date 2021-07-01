from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    check_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'check_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        check_password = self.validated_data['check_password']

        if password != check_password:
            raise serializers.ValidationError('Passwords must macth')
        user.set_password(password)
        user.save()
