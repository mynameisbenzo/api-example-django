from django.shortcuts import redirect
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from django.template.defaulttags import register
from django.shortcuts import render_to_response
from django.http import JsonResponse

from drchrono.endpoints import DoctorEndpoint, AppointmentEndpoint, AppointmentProfileEndpoint, PatientEndpoint

from datetime import datetime

import sys
sys.path.insert(0, '..')
from users.models import Doctor

###########################
# template tags
###########################
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def patient_full_name(dictionary):
    middle_name = ""
    if dictionary.get("middle_name"):
        middle_name = " " + dictionary.get("middle_name")
    return str(dictionary.get("first_name")) + middle_name \
            + " " + str(dictionary.get("last_name"))

# get patient info
def get_patient_info(request):
    oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
    access_token = oauth_provider.extra_data['access_token']
    patient = request.GET.get('patient', None)
    if not patient:
        return JsonResponse({})
    api = PatientEndpoint(access_token)
    return JsonResponse(api.fetch(id=patient))

class DoctorLogin(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """
    template_name = 'doctor_login.html'

class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """
    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens. This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def get_doctor_details(self):
        """
        Use the token we have stored in the DB to make an API request and get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)

        # Grab the first doctor from the list; normally this would be the whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_appointments(self):
        access_token = self.get_token()
        api = AppointmentEndpoint(access_token)
        dt = datetime.now()
        today = dt.strftime("%m-%d-%Y")
        return api.list(date=today)


    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.get_doctor_details()
        appointments = self.get_appointments()
        doctor = Doctor.objects.find_or_create(doctor_details)
        kwargs['doctor'] = doctor
        kwargs['appointments'] = appointments
        kwargs['doctor_is_in'] = Doctor.objects.doctor_in_office()

        return kwargs

class PatientSignIn(TemplateView):
    template_name = 'patient_login.html'
