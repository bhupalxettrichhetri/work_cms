from django.contrib import admin
from .models import Organization, PasswordOTP, Vendor, Device, DevicePassword, DeviceConfig, ContactPerson, Profile,Vpn, OrganizationDocument, Directory

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_by')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'organization', 'vendor', 'firmware_version')

@admin.register(DevicePassword)
class DevicePasswordAdmin(admin.ModelAdmin):
    list_display = ('username', 'device', 'created_at', 'updated_at')

@admin.register(DeviceConfig)
class DeviceConfigAdmin(admin.ModelAdmin):
    list_display = ('device', 'uploaded_at')

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'organization')
    

admin.site.register(OrganizationDocument)
admin.site.register(Directory)
admin.site.register(PasswordOTP)


admin.site.register(Profile)
admin.site.register(Vpn)

