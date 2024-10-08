from django.db import models
from django.contrib.auth.models import User
from onboard.models_existing import Users

# Create your models here.
class BusinessDetails(models.Model):
	businessDetailId = models.AutoField(primary_key=True)
	companyName = models.CharField(max_length=200, null=True, blank=True)
	businessRegistrationNumber = models.CharField(max_length=200, null=True, blank=True)
	natureOfBusiness = models.CharField(max_length=200, null=True, blank=True)
	streetAddress = models.CharField(max_length=200, null=True, blank=True)
	postalAddress = models.CharField(max_length=200, null=True, blank=True)
	officialPhoneNumber = models.CharField(max_length=200, null=True, blank=True)
	alternatePhoneNumber = models.CharField(max_length=200, null=True, blank=True)
	active = models.IntegerField(default=0)
	created_by = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='business_owner', null=True)
	updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth_user', null=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, blank=True)
	numberOfDirectors = models.IntegerField(default=0)
	userIdFile = models.FileField(upload_to='user-id-file', null=True, blank=True)
	companyProfileCert = models.FileField(upload_to='company-profile-certs', null=True, blank=True)
	certOfCorporation = models.FileField(upload_to='cert-of-corporation', null=True, blank=True)
	commenceBusinessCert = models.FileField(upload_to='commence-business-certs', null=True, blank=True)

class DirectorIds(models.Model):
	directorIdsId = models.AutoField(primary_key=True)
	businessDetailId = models.ForeignKey(BusinessDetails, on_delete=models.CASCADE, related_name='director_id_business')
	directorIds = models.FileField(upload_to='directors-certs', null=True, blank=True)