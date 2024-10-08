from rest_framework import serializers
from onboard.models import BusinessDetails, DirectorIds
from onboard.models_existing import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class BusinessDetailsSerializer(serializers.ModelSerializer):
    created_by = UsersSerializer()
    class Meta:
        model = BusinessDetails
        fields = '__all__'

class BusinessDetailsCustomSerializer(serializers.Serializer):
    userid = serializers.IntegerField()
    companyName = serializers.CharField(max_length=255)
    businessRegistrationNumber = serializers.CharField(max_length=255)
    natureOfBusiness=serializers.CharField(max_length=255)
    phoneNumber=serializers.CharField(max_length=255)
    streetAddress=serializers.CharField(max_length=255)
    postalAddress=serializers.CharField(max_length=255)
    alternatePhoneNumber=serializers.CharField(max_length=255)
    numberOfDirectors=serializers.CharField(max_length=255)

class BusinessDetailsAuthorizeSerializer(serializers.Serializer):
    businessId = serializers.CharField(max_length=255)
    command = serializers.CharField(max_length=255)

class BusinessDetailsResponseSerializer(serializers.Serializer):
    StatusDesc = serializers.CharField(max_length=255)
    StatusCode = serializers.IntegerField()
    Result = BusinessDetailsSerializer()

class DownloadFileSerializer(serializers.Serializer):
    requestId = serializers.IntegerField()
    fileType = serializers.CharField(max_length=100)

class DirectorImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorIds
        fields = '__all__'

class DirectorImagesRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class DirectorImagesResponseSerializer(serializers.Serializer):
    StatusDesc = serializers.CharField(max_length=255)
    StatusCode = serializers.IntegerField()
    Result = DirectorImagesSerializer(many=True)