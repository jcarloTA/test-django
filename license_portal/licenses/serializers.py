from rest_framework import serializers
from .models import License, Client, LicenseLog, EmailsLog

class LisencesSerializer(serializers.ModelSerializer):
    # client = serializers.IntegerField()

    class Meta:
        model = License
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'

class EmailsLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailsLog
        fields = '__all__'