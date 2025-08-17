from rest_framework import serializers


class SendEmailSerializer(serializers.Serializer):
    email = serializers.CharField()


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()
