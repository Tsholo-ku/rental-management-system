from rest_framework import serializers
from apps.users.models import UserAccount
from django.contrib.auth import authenticate

class UserSerializer(serializers.HyperlinkedModelSerializer):

    #use serializers.ChoiceField() to define this field in the serializer to handle the choices properly
    type = serializers.ChoiceField(choices = UserAccount.Types.choices) 
    class Meta:
        model = UserAccount
        fields = ['url', 'username', 'email', 'full_name', 'is_staff', 'password', 'type']

    def validate_type(self, type):
        # custom validation
        if type != "LANDLORD" and type != "TENANT":
            raise serializers.ValidationError("Invalid user type")
        return type

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = {
                    "message":"Access denied wrong email or password.",
                    "data":" ",
                    "status":"Failed"
                }
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = {
                    "message":"Both email and password are required.",
                    "data":" ",
                    "status":"Failed"
                }
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs