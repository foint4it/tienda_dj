#
from rest_framework import serializers

class LoginSocialSerializer(serializers.Serializer):
    """ serializador para recuperar password de acceso """

    token_id = serializers.CharField(required=True)