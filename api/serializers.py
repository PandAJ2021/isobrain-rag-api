from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type':'password', 'place_holder':'Password'}
    )
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)
            