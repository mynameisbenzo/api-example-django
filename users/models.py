# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DoctorManager(models.Manager):
    # check if doctor is in the office
    def doctor_in_office(self):
        if self.filter(in_office=True):
            return True
        else:
            return False

    # find or create a doctor logging in
    def find_or_create(self,data):
        doctor = None
        try:
            doctor = self.get(pk=data['id'])
        except:
            doctor = Doctor()
            doctor.last_name = data["last_name"]
            doctor.first_name = data["first_name"]
            doctor.suffix = data["suffix"]
            doctor.specialty = data["specialty"]
            doctor.is_account_suspended = data["is_account_suspended"]
            doctor.group_npi_number = data["group_npi_number"]
            doctor.npi_number = data["npi_number"]
            doctor.timezone = data["timezone"]
            doctor.office_phone = data["office_phone"]
            doctor.home_phone = data["home_phone"]
            doctor.email = data["email"]
            doctor.drchrono_id = data["id"]

        doctor.in_office = True
        doctor.save()
        return doctor

class Doctor(models.Model):
    in_office = models.BooleanField(default=False)

    # api response fields
    last_name = models.CharField(max_length=200, default="")
    first_name = models.CharField(max_length=200, default="")
    suffix = models.CharField(max_length=5, default="", null=True)
    group_npi_number = models.CharField(max_length=20, default="", null=True)
    npi_number = models.CharField(max_length=20, default="", null=True)
    timezone = models.CharField(max_length=50, default="", null=True)
    specialty = models.CharField(max_length=25, default="")
    is_account_suspended = models.BooleanField(default=False)
    office_phone = models.CharField(max_length=20, default="")
    home_phone = models.CharField(max_length=20, default="")
    email = models.CharField(max_length=50, default="")
    drchrono_id = models.IntegerField(default=0, primary_key=True)

    objects = DoctorManager()

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)
# implement appointment/patient models
#
# class Appointment(models.Model):
#     scheduled_time = models.CharField(default="", max_length=50)
#     duration = models.IntegerField(default=0)
#     status = models.CharField(default="", max_length=15)
#     drchrono_id = models.IntegerField(default=0, primary_key=True)
#     patient_id = models.IntegerField(default=0)
#     reason = models.CharField(default="", max_length=250)
#
# class Patient(models.Model):
#     first_name = models.CharField(default="", max_length=50)
#     middle_name = models.CharField(null=True, default=None, max_length=50)
#     last_name = models.CharField(default="", max_length=50)
#     drchrono_id = models.IntegerField(default=0, primary_key=True)
