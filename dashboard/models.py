from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.timezone import now
from django.utils import timezone

class Directory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def document_upload_path(instance, filename):
    org_name = instance.organization.name.replace(" ", "_")
    folder_path = os.path.join("directory", org_name)
    print(folder_path)
    if instance.dir:
        folder_path = folder_path+f'\{instance.dir.name}'
        print(folder_path)

    # Ensure the folder exists
    os.makedirs(os.path.join("media", folder_path), exist_ok=True)

    # Check if file already exists and rename if needed
    file_path = os.path.join(folder_path, filename)
    base, ext = os.path.splitext(filename)
    
    # Rename if file exists
    counter = 1
    while os.path.exists(os.path.join("media", file_path)):
        file_path = os.path.join(folder_path, f"{base}_{counter}{ext}")
        counter += 1

    return file_path


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organizations_created', null=True)

    def __str__(self):
        return self.name
        

class OrganizationDocument(models.Model):
    organization = models.ForeignKey(Organization, related_name='documents', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    dir = models.ForeignKey(Directory, related_name='directory_name', on_delete=models.CASCADE)
    file = models.FileField(upload_to=document_upload_path, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents_created', null=True)

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.organization.name}"
# class ContactPerson(models.Model):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='contact_people')
#     # testname = models.CharField(max_length=255)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()

#     def __str__(self):
#         # return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Device(models.Model):
    name = models.CharField(max_length=255)
    #ip_address = models.GenericIPAddressField()
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name='devices', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='devices', on_delete=models.SET_NULL, null=True, blank=True)
    firmware_version = models.CharField(max_length=255, default='1.1.1')

    def __str__(self):
        return self.name

class DevicePassword(models.Model):
    device = models.OneToOneField(Device, related_name='password', on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.password}'
    
class PasswordOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_password = models.ForeignKey(DevicePassword, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        self.expires_at = timezone.now() + timedelta(minutes=1)

    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code}"

class DeviceConfig(models.Model):
    device = models.OneToOneField(Device, related_name='config', on_delete=models.CASCADE)
    config_file = models.FileField(upload_to='device_configs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Config for {self.device.name}'

class ContactPerson(models.Model):
    organization = models.ForeignKey(Organization, related_name='contact_people', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.organization.name}'

class Vpn(models.Model):
    ip_address = models.GenericIPAddressField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name='vpn', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='vpn_device', on_delete=models.SET_NULL, null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vpn_user', null=True)

