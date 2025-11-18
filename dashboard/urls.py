"""work_cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from .views import AjaxPostView, OrganizationCreateView, HomePageView, ProfileUpdateView, OrganizationListView, OrganizationUpdateView,\
                    OrganizationDeleteView, OrganizationDetailView, OrganizationConatactPersonCreateView, OrganizationConatactPersonListView,\
                    OrganizationConatactPersonDeleteView, OrganizationConatactPersonUpdateView, OrganizationDeviceListView, OrganizationDeviceCreateView,\
                    OrganizationDeviceUpdateView, OrganizationDeviceDeleteView, OrganizationDeviceDetailView, VendorAutoComplete, VerifyOTPView, VpnListView,\
                    VpnCreateView,OrganizationDocumentListView
urlpatterns = [
    path('', HomePageView.as_view(), name='dashboard'),
    path('organization', OrganizationListView.as_view(), name='organization_list'),
    path('organization/<int:pk>/', OrganizationDetailView.as_view(), name='organization_detail'),
    path('organization/create/', OrganizationCreateView.as_view(), name='organization_create'),
    path('organization/<int:pk>/edit/', OrganizationUpdateView.as_view(), name='organization_edit'),
    path('organization/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization_delete'),
    # organization contact person
    path('organization/<int:pk>/contact_person/create', OrganizationConatactPersonCreateView.as_view(), name='contact_person_create'),
    path('organization/<int:pk>/contact_person_list', OrganizationConatactPersonListView.as_view(), name='contact_person_list'),
    path('organization/<int:pk>/contact_person/delete/', OrganizationConatactPersonDeleteView.as_view(), name='contact_person_delete'),
    path('organization/<int:pk>/contact_person/edit/', OrganizationConatactPersonUpdateView.as_view(), name='contact_person_edit'),
    # organizarion devices
    path('organization/<int:pk>/device_list', OrganizationDeviceListView.as_view(), name='device_list'),
    path('organization/<int:pk>/device/create/', OrganizationDeviceCreateView.as_view(), name='device_create'),
    path('organization/<int:pk>/device/edit/', OrganizationDeviceUpdateView.as_view(), name='device_edit'),
    path('organization/<int:pk>/device/delete/', OrganizationDeviceDeleteView.as_view(), name='device_delete'),
    path('organization/<int:pk>/device/', OrganizationDeviceDetailView.as_view(), name='device_detail'),
    path('ajax/post/', AjaxPostView.as_view(), name='ajax-post'),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    # organizarion document
    path('organization/<int:pk>/document_list', OrganizationDocumentListView.as_view(), name='document_list'),

    # vpn routes
    path('vpn', VpnListView.as_view(), name='vpn_list'),
    path('vpn/<int:pk>/', OrganizationDetailView.as_view(), name='vpn_detail'),
    path('vpn/create/', VpnCreateView.as_view(), name='vpn_create'),
    path('vpn/<int:pk>/edit/', OrganizationUpdateView.as_view(), name='vpn_edit'),
    path('vpn/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='vpn_delete'),


     # vpn routes
    path('vpn', VpnListView.as_view(), name='vpn_list'),
    path('vpn/<int:pk>/', OrganizationDetailView.as_view(), name='vpn_detail'),
    path('vpn/create/', VpnCreateView.as_view(), name='vpn_create'),
    path('vpn/<int:pk>/edit/', OrganizationUpdateView.as_view(), name='vpn_edit'),
    path('vpn/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='vpn_delete'),


    # autocomplete
    path('vendor-autocomplete/', VendorAutoComplete.as_view(create_field='name'), name='vendor-autocomplete'),

    path('profile/', ProfileUpdateView.as_view(), name='profile'),

    # path('admin/', admin.site.urls),
    # path('dashboard/', include('dashboard.urls')),
    
]
