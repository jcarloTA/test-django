""" Data model for licenses application
"""
import enum

from datetime import timedelta, datetime
from typing import Tuple, List

from django.contrib.auth.models import User
from django.db import models

LICENSE_EXPIRATION_DELTA = timedelta(days=90)


class ChoiceEnum(enum.Enum):
    """Enum for choices in a choices field"""
    @classmethod
    def get_choices(cls) -> List[Tuple[str, int]]:
        return [(a.name, a.value) for a in cls]


class Package(ChoiceEnum):
    """A Package accessible to a client with a valid license"""
    javascript_sdk = 0
    ios_sdk = 1
    android_sdk = 2


class LicenseType(ChoiceEnum):
    """A license type"""
    production = 0
    evaluation = 1

class LicenseStatus(ChoiceEnum):
    invalid = 0
    valid = 1
    expired = 2


def get_default_license_expiration() -> datetime:
    """Get the default expiration datetime"""
    return datetime.utcnow() + LICENSE_EXPIRATION_DELTA

class LicenseLog(models.Model):
    """ Data model for a client license allowing access to a package
    """
    license = models.ForeignKey('License', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)

class Client(models.Model):
    """ A client who holds licenses to packages
    """
    client_name = models.CharField(max_length=120, unique=True)
    poc_contact_name = models.CharField(max_length=120)
    poc_contact_email = models.EmailField()

    admin_poc = models.ForeignKey(User, limit_choices_to={'is_staff': True}, on_delete=models.CASCADE)

class License(models.Model):
    """ Data model for a client license allowing access to a package
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    package = models.IntegerField(choices=Package.get_choices())
    license_type = models.IntegerField(choices=LicenseType.get_choices())
    license_status = models.IntegerField(choices=LicenseStatus.get_choices(), default=LicenseStatus.valid.value)

    created_datetime = models.DateTimeField(auto_now=True)
    expiration_datetime = models.DateTimeField(default=get_default_license_expiration)

    
    def get_license_type_display(self):
        # Obtén la representación legible del campo license_type
        if self.license_type == LicenseType.production.value:
            return "Production"
        elif self.license_type == LicenseType.evaluation.value:
            return "Evaluation"
        else:
            return "Desconocido"  # Manejar otros valores si es necesario
        
    def get_license_status_display(self):
        # Obtén la representación legible del campo license_status
        if self.license_status == LicenseStatus.valid.value:
            return "Valid"
        elif self.license_status == LicenseStatus.invalid.value:
            return "Invalid"
        elif self.license_status == LicenseStatus.expired.value:
            return "Expired"
        else:
            return "Desconocido"
    def get_lisense_package_display(self):
        # Obtén la representación legible del campo package
        if self.package == Package.javascript_sdk.value:
            return "Javascript SDK"
        elif self.package == Package.ios_sdk.value:
            return "iOS SDK"
        elif self.package == Package.android_sdk.value:
            return "Android SDK"
        else:
            return "Desconocido"

class EmailsLog(models.Model):
    """ Data model for a client license allowing access to a package
    """
    subject = models.CharField(max_length=120)
    sender = models.CharField(max_length=120)
    recipient = models.CharField(max_length=120)
    sent_datetime = models.DateTimeField(auto_now=True)
    body = models.TextField()
    