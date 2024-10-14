import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.http import FileResponse, Http404
import datetime

from onboard.serializers import BusinessDetailsSerializer, BusinessDetailsCustomSerializer, BusinessDetailsAuthorizeSerializer, BusinessDetailsResponseSerializer, DownloadFileSerializer, DirectorImagesRequestSerializer, DirectorImagesResponseSerializer
from onboard.models import BusinessDetails, DirectorIds
from onboard.models_existing import Users, Shops, Customers

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
        userIdFile_ = request.FILES['userIdFile']
        directorIDs = request.FILES.getlist('directorIDs[]')
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
                officialPhoneNumber = serializer.data['phoneNumber'],
                alternatePhoneNumber = serializer.data['alternatePhoneNumber'],
                created_by=user,
                numberOfDirectors = serializer.data['numberOfDirectors'],
                companyProfileCert = certCompanyProfile,
                certOfCorporation = certOfCorporation,
                commenceBusinessCert = certCommenceBusiness,
                userIdFile = userIdFile_
            )

            # user.phone_number = serializer.data['phoneNumber']

            # user.save(update_fields=['phone_number'])

            saveBusinessDetails.save()

            logger.info("Director IDs are ")
            logger.info(directorIDs)

            for directorId in request.FILES.getlist('directorIDs'):
                logger.info("Each file ...")
                logger.info(directorId)

                images_ = DirectorIds(
                        businessDetailId=saveBusinessDetails,
                        directorIds=directorId
                    )
                images_.save()

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
                businessEnt = Shops(
                     shop_name=business.companyName,
                     shop_description=business.natureOfBusiness,
                     date_created=datetime.datetime.now(),
                     created_by=1,
                     active=1
                )

                businessEnt.save()

                business.active = 1
                user.active = 1
                user.is_verified = 1
                user.save(update_fields=['active','is_verified'])

                customer = Customers(user=user)
                customer.shop = businessEnt
                customer.active = customer.active
                customer.date_created = customer.date_created
                customer.date_modified = datetime.datetime.now(),
                customer.created_by = customer.created_by,
                customer.modified_by = 1

                customer.save()
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
        
class ViewDirectorImages(viewsets.ViewSet):
    def create(self, request):
        serializer = DirectorImagesRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            logger.info("Valid request")
            directorIds = DirectorIds.objects.filter(businessDetailId=serializer.data["id"])

            status_ = 200
            message = "Director ID images found"

            resp = Resp(StatusDesc=message, StatusCode=status_, Result=directorIds)

            return Response(DirectorImagesResponseSerializer(resp).data,status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
         
class DownloadFile(viewsets.ViewSet):
    def create(self, request):
        serializer = DownloadFileSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            logger.info("Valid request")
            business = BusinessDetails.objects.get(businessDetailId=serializer.data["requestId"])

            file = ""
            if serializer.data["fileType"]=="CERT_OF_INCORPORATION":
                 file = business.certOfCorporation
            if serializer.data["fileType"]=="CERT_TO_COMMENCE":
                 file = business.commenceBusinessCert
            if serializer.data["fileType"]=="CERT_COMPANY_PROFILE":
                 file = business.companyProfileCert
            filePath = os.path.join(file.path)

            if os.path.exists(filePath):
                response = FileResponse(open(filePath, 'rb'), as_attachment=True)
                logger.info("File name retrieved is ")
                logger.info(os.path.basename(file.path))
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file.path)}"'
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                return response
            else:
                raise Http404("File does not exist")
        else:
             logger.info("Bad request")
             return Response(status=status.HTTP_400_BAD_REQUEST)