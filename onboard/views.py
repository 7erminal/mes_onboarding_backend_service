from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets

from onboard.serializers import BusinessDetailsSerializer, BusinessDetailsCustomSerializer, BusinessDetailsAuthorizeSerializer, BusinessDetailsResponseSerializer
from onboard.models import BusinessDetails, DirectorIds
from onboard.models_existing import Users

import logging

logger = logging.getLogger("django")

class Resp:
	def __init__(self, StatusDesc, Result, StatusCode):
		self.StatusDesc=StatusDesc
		self.Result=Result
		self.StatusCode=StatusCode

# Create your views here.
class BusinessDetailsView(viewsets.ViewSet):
    def create(self, request):
        serializer = BusinessDetailsCustomSerializer(data=request.data)

        logger.info(serializer)
        directorIDs = request.FILES.getlist('directorIDs')
        certCompanyProfile = request.FILES['certCompanyProfile'] if 'certCompanyProfile' in request.FILES else False
        certOfCorporation = request.FILES['certOfCorporation']
        certCommenceBusiness = request.FILES['certCommenceBusiness']

        if serializer.is_valid(raise_exception=True):
            user = Users.objects.get(user_id=serializer.data['userid'])
            saveBusinessDetails = BusinessDetails(
                companyName = serializer.data['companyName'],
                businessRegistrationNumber = serializer.data['businessRegistrationNumber'],
                natureOfBusiness = serializer.data['natureOfBusiness'],
                streetAddress = serializer.data['streetAddress'],
                postalAddress = serializer.data['postalAddress'],
                alternatePhoneNumber = serializer.data['alternatePhoneNumber'],
                created_by=user,
                numberOfDirectors = serializer.data['numberOfDirectors'],
                companyProfileCert = certCompanyProfile,
                certOfCorporation = certOfCorporation,
                commenceBusinessCert = certCommenceBusiness
            )

            user.phone_number = serializer.data['phoneNumber']

            user.save(update_fields=['phone_number'])

            saveBusinessDetails.save()

            for directorId in directorIDs:
                logger.info("Each file ...")
                logger.info(directorId)

                images_ = DirectorIds(
                        businessDetailId=saveBusinessDetails,
                        directorIds=directorId
                    )
                DirectorIds.save()

            message = "Details added successfully. You will be notified once your request is approved."
            status_ = 200

            resp = Resp(StatusDesc=message, StatusCode=status_, Result=saveBusinessDetails)
            logger.info("About to send response")

            return Response(BusinessDetailsResponseSerializer(resp).data,status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request):
         logger.info("About to fetch business details")
         saveBusinessDetails = BusinessDetails.objects.all()
         logger.info("Sending response")
         return Response(BusinessDetailsSerializer(saveBusinessDetails, many=True).data,status.HTTP_200_OK)
    
class AuthorizeBusiness(viewsets.ViewSet):
     def create(self, request):
        serializer = BusinessDetailsAuthorizeSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            command = serializer.data['command']
            business = BusinessDetails.objects.get(businessDetailId=serializer.data["businessId"])
            user = Users(user_id=business.created_by.user_id)

            status_ = 200
            message = "AUTHORIZED"
            
            if command=="ACCEPT":
                business.active = 1
                user.active = 1
                user.is_verified = 1
                user.save(update_fields=['active','is_verified'])
            elif command=="REJECT":
                 business.active = 6
                 status_ = 400
                 message = "REJECTED"
            
            business.save(update_fields=['active'])

            resp = Resp(StatusDesc=message, StatusCode=status_, Result=business)
            logger.info("About to send response")

            return Response(BusinessDetailsResponseSerializer(resp).data,status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)