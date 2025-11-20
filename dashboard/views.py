# my_app/views.py
# from datetime import timezone
from django.utils import timezone
from datetime import timedelta
import random
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView

from dashboard.task import send_otp_email
from work_cms import settings

from .forms import UserForm, ProfileForm, OrganizationForm, ContactPersonForm, DeviceForm, DevicePasswordForm,\
                    DeviceConfigForm, VpnForm

from .models import DevicePassword, Organization, ContactPerson, Device, PasswordOTP, Vendor, Vpn, OrganizationDocument, Directory
from django.contrib.auth.mixins import LoginRequiredMixin
from .encrypt_utils import decrypt, encrypt
from django.contrib import messages
from dal import autocomplete
from django.core.mail import send_mail


class MainPageView(TemplateView):
    template_name = 'dashboard/main_page.html'


class VendorAutoComplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = Vendor.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs



class ProfileUpdateView(LoginRequiredMixin,View):
    template_name = 'dashboard/profile.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })


class HomePageView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/homepage.html'



class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'organization/list.html'
    context_object_name = 'organizations' 

    def get_queryset(self):
        return Organization.objects.filter(created_by=self.request.user)

class OrganizationCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/create.html'
    success_url = reverse_lazy('dashboard:organization_list')
    success_message = "Organization added successfully"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['contact_persons_formset'] = ContactPersonFormSet(self.request.POST, instance=self.object)
    #     else:
    #         context['contact_persons_formset'] = ContactPersonFormSet(instance=self.object)
    #     return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class OrganizationUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'organization/create.html'
    success_url = reverse_lazy('dashboard:organization_list')
    success_message = "Organization updated successfully"

    def get_object(self, queryset=None):
        print(self.kwargs['pk'])
        obj = Organization.objects.get(pk=self.kwargs['pk'])
        return obj


# class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
#     model = Organization
#     form_class = OrganizationForm
#     template_name = 'organization/create.html'
#     success_url = reverse_lazy('dashboard:organization_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.POST:
#             context['contact_persons_formset'] = ContactPersonFormSet(self.request.POST, instance=self.object)
#         else:
#             context['contact_persons_formset'] = ContactPersonFormSet(instance=self.object)
#         return context

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         formset = ContactPersonFormSet(self.request.POST, instance=self.object)
#         if formset.is_valid():
#             formset.save()
#         return response

class OrganizationDeleteView(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Organization
    template_name = 'organization/delete.html'
    success_message = "Organization deleted successfully"
    success_url = reverse_lazy('dashboard:organization_list')  # Redirect to the organization list view after deletion

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'organization/detail.html'

class OrganizationConatactPersonCreateView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = ContactPerson
    form_class = ContactPersonForm
    template_name = 'contact_person/create.html'
    success_message = "Contact added successfully"
    def get_success_url(self):
        return reverse_lazy('dashboard:contact_person_list', kwargs={'pk': self.kwargs['pk']})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['contact_persons_formset'] = ContactPersonFormSet(self.request.POST, instance=self.object)
    #     else:
    #         context['contact_persons_formset'] = ContactPersonFormSet(instance=self.object)
    #     return context

    def form_valid(self, form):
        o_id = Organization.objects.get(pk=self.kwargs['pk'])
        form.instance.organization_id = o_id.id
        return super().form_valid(form)

class OrganizationConatactPersonListView(LoginRequiredMixin, ListView):
    model = ContactPerson
    template_name = 'contact_person/list.html'
    context_object_name = 'contacts' 

    def get_queryset(self):
        return ContactPerson.objects.filter(organization_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['organization_id'] = self.kwargs['pk']
        # print(context)
        return context

class OrganizationConatactPersonDeleteView(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = ContactPerson
    template_name = 'organization/delete.html'
    success_message = "contact deleted successfully"

    def get_success_url(self):
        print(self.object.organization_id)
        return reverse_lazy('dashboard:contact_person_list', kwargs={'pk': self.object.organization.id})

class OrganizationConatactPersonUpdateView(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = ContactPerson
    form_class = ContactPersonForm
    template_name = 'contact_person/create.html'
    success_message = "Contact Updated successfully"
    def get_success_url(self):
        return reverse_lazy('dashboard:contact_person_list', kwargs={'pk': self.object.organization_id})

    def get_object(self, queryset=None):
        obj = ContactPerson.objects.get(pk=self.kwargs['pk'])
        return obj

class OrganizationDeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'device/list.html'
    context_object_name = 'devices' 

    def get_queryset(self):
        qs = Device.objects.select_related('vendor','password').filter(organization_id=self.kwargs['pk'])
        # print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_id'] = self.kwargs['pk']
        return context
    
class OrganizationDocumentListView(LoginRequiredMixin, ListView):
    model = OrganizationDocument
    template_name = 'document/list.html'
    context_object_name = 'documents' 

    def get_queryset(self):
        qs = Directory.objects.prefetch_related('directory_name')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_id'] = self.kwargs['pk']
        return context

class OrganizationDeviceCreateView(LoginRequiredMixin, SuccessMessageMixin,View):
    template_name = 'device/create.html'
    success_message = "device added successfully"
    success_url = ''

    def get(self, request, *args, **kwargs):
        print('here devices')
        device_form = DeviceForm()
        password_form = DevicePasswordForm()
        config_form = DeviceConfigForm()
        return render(request, self.template_name, {
            'device_form': device_form,
            'password_form': password_form,
            'config_form': config_form,
        })

    def post(self, request,pk):
        organization = get_object_or_404(Organization, pk=pk)
        device_form = DeviceForm(request.POST)
        password_form = DevicePasswordForm(request.POST)
        config_form = DeviceConfigForm(request.POST, request.FILES)

        print(device_form.data, device_form.is_valid())

       
        if device_form.is_valid() and password_form.is_valid() and config_form.is_valid():
            
            password_form.cleaned_data["password"]

            device = device_form.save(commit=False)
            device.organization = organization
            device.save()

            # save device password
            password = password_form.save(commit=False)
            password.device = device
            password.password = encrypt(password_form.cleaned_data["password"])
            password.save()

             # Save device config
            config = config_form.save(commit=False)
            config.device = device
            if request.FILES.get('config_file'):
                config.config_file = request.FILES['config_file']
            config.save()
            messages.success(request, "Device deleted successfully.")
            return redirect(reverse('dashboard:device_list', kwargs={'pk': pk}))
            # return reverse_lazy('dashboard:device_list', kwargs={'pk': pk})
        else:
            print(device_form.errors, password_form.errors, config_form.errors, "here")
            # messages.success(request, "Device deleted successfully.")
            return render(request, self.template_name, {
                'device_form': device_form,
                'password_form': password_form,
                'config_form': config_form
            })


class OrganizationDeviceUpdateView(View):
    template_name = 'device/create.html'

    def get(self, request, pk):
        
        device = get_object_or_404(Device, pk=pk)
        device_form = DeviceForm(instance=device)
        
        
        # Ensure a password exists for the device
        try:
            password = device.password
        except DevicePassword.DoesNotExist:
            password = None
        
        try:
            config = device.config
        except DeviceConfig.DoesNotExist:
            config = None

        password_form = DevicePasswordForm(instance=password)
        config_form = DeviceConfigForm(instance=config)

        return render(request, self.template_name, {
            'device_form': device_form,
            'password_form': password_form,
            'config_form': config_form,
            'device': device,
        })

    def post(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        device_form = DeviceForm(request.POST, instance=device)
        
        # Ensure a password exists for the device
        try:
            password = device.password
        except DevicePassword.DoesNotExist:
            password = DevicePassword(device=device)

        try:
            config = device.config
        except DeviceConfig.DoesNotExist:
            config = None

        config_form = DeviceConfigForm(request.POST,instance=config)
        password_form = DevicePasswordForm(request.POST, instance=password)

        if device_form.is_valid() and password_form.is_valid() and config_form.is_valid():
            device_form.save()
            password_instance  = password_form.save(commit=False)
            config = config_form.save(commit=False)
            if password_form.cleaned_data['password']:
                password_instance.password = encrypt(password_form.cleaned_data['password'])

            password_instance .save()

            if request.FILES.get('config_file'):
                config.config_file = request.FILES['config_file']
            config.save()
            messages.success(request, "Device updated successfully.")
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to
            return redirect(reverse('dashboard:device_list', kwargs={'pk': device.organization.id})) 

        return render(request, self.template_name, {
            'device_form': device_form,
            'password_form': password_form,
            'device': device,
        })


class OrganizationDeviceDeleteView(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Device
    template_name = 'organization/delete.html'
    success_message = "Device deleted successfully"
    # success_url = reverse_lazy('dashboard:organization_list')  # Redirect to the organization list view after deletion


    # def get_success_url(self):
    #     print(self.object.id)
    #     obj = self.object.organization.id
        
    #     return redirect(reverse('dashboard:device_list', kwargs={'pk': }))

    def get_success_url(self):
        return reverse_lazy('dashboard:device_list', kwargs={'pk': self.object.organization_id})


class OrganizationDeviceDetailView(DetailView):
    model = Device
    template_name = 'device/detail.html'


class VpnListView(LoginRequiredMixin, ListView):
    model = Vpn
    template_name = 'vpn/list.html'
    context_object_name = 'vpns' 

    def get_queryset(self):
        print(Vpn.objects.filter(created_by=self.request.user))
        return Vpn.objects.filter(created_by=self.request.user)


class VpnCreateView(CreateView):
    model = Vpn
    form_class = VpnForm
    template_name = 'vpn/create.html'
    success_url = reverse_lazy('dashboard:vpn_list')  # Adjust to your success URL

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the current user to the form
        return kwargs

    def form_valid(self, form):
        password = encrypt(form.cleaned_data.get('password'))
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



class AjaxPostView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        password_id = request.POST.get("password_id", None)

        if not password_id:
            return JsonResponse({"error": "No data provided"}, status=400)

        try:
            pass_obj = DevicePassword.objects.get(id=int(password_id))
        except DevicePassword.DoesNotExist:
            return JsonResponse({"error": "Password record not found"}, status=404)

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=5)

        PasswordOTP.objects.create(
            user=request.user,
            device_password=pass_obj,
            otp_code=otp,
            expires_at=expires_at
        )

        # Send OTP email

        send_otp_email.delay(request.user.email, otp, expires_at.strftime("%H:%M:%S"))
        # send_mail(
        #     subject="Your OTP Code",
        #     message=f"Your OTP code is: {otp}. It will expire at {expires_at.strftime('%H:%M:%S')}.",
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=[request.user.email],
        #     fail_silently=False
        # )

        return JsonResponse({"message": "OTP sent to your email.", "otp_required": True})

# class AjaxPostView(LoginRequiredMixin, View):
#     @method_decorator(csrf_exempt)  # Use if CSRF token is not included in the request
#     def post(self, request, *args, **kwargs):
#         # Extract data from POST request
#         print(request.POST,'here')
#         some_data = request.POST.get("password_id", None)
        
#         if some_data:
#             pass_obj = DevicePassword.objects.get(id=int(some_data))
#             print(decrypt(pass_obj.password))
#             data = {"message": f"{decrypt(pass_obj.password)}"}
#             return JsonResponse(data)
        
#         return JsonResponse({"error": "No data provided"}, status=400)

#     def get(self, request, *args, **kwargs):
#         return JsonResponse({"error": "GET method not allowed"}, status=405)
    

class VerifyOTPView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        print('post')
        otp_input = request.POST.get("otp")
        password_id = request.POST.get("password_id")
        # otp_entry = PasswordOTP.objects.filter(
        #         user=request.user,
        #         device_password_id=password_id,
        #         otp_code=otp_input,
        #         is_used=False
        #     ).latest('created_at')
        # print(otp_entry)

        try:
            otp_entry = PasswordOTP.objects.filter(
                user=request.user,
                device_password_id=password_id,
                otp_code=otp_input,
                is_used=False
            ).latest('created_at')
            print(otp_entry.is_expired())

        except PasswordOTP.DoesNotExist:
            print('error')
            return JsonResponse({"error": "Invalid OTP"}, status=400)

        if otp_entry.is_expired():
            return JsonResponse({"error": "OTP expired"}, status=400)

        otp_entry.is_used = True
        otp_entry.save()

        decrypted_pass = decrypt(otp_entry.device_password.password)
        return JsonResponse({"password": decrypted_pass})


class CustomPageNotFoundView(TemplateView):
    template_name = "404.html"

    # This is needed because handler404 passes `request` and `exception`
    def get(self, request, exception=None, *args, **kwargs):
        stars = []
        for _ in range(20):  # 20 stars
            stars.append({
                "top": random.randint(0, 100),
                "left": random.randint(0, 100),
                "size": random.randint(2, 5),
                "delay": round(random.uniform(0, 2), 2),
            })
        context = self.get_context_data(**kwargs)
        context["title"] = "Page Not Found"
        context["message"] = "Oops! Looks like you're lost in space."
        context["stars"] = stars
        return self.render_to_response(context, status=404)
