from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

STATE = (
('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),('DE','DE'),
('FL','FL'),('GA','GA'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),('IA','IA'),('KS','KS'),
('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),('MN','MN'),('MS','MS'),
('MO','MO'),('MT',"MT"),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),('NM','NM'),('NY','NY'),
('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),('RI','RI'),('SC','SC'),
('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),('WA','WA'),('WV','WV'),
('WI','WI'),('WY','WY'),)

# group + Rh factor
class BloodType(models.Model):
    gr = models.CharField(max_length=2)
    rh_f = models.CharField(max_length=1)
    __unicode__ = lambda self: self.gr + ' ' + self.rh_f


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    pid = models.IntegerField(default=0, unique=True)
    blood_type = models.ForeignKey(BloodType, null=True)
    __unicode__ = lambda self: str(self.pid)

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    hospitalName = models.CharField('Hospital Name', max_length=50, default='')
    hospitalAddress = models.CharField('Address', max_length=50, default='')
    hospitalCity = models.CharField('City', max_length=30, default='')
    hospitalState = models.CharField('State', max_length=2, choices=STATE, default='')
    hospitalZip = models.CharField('Zip Code', max_length=5, default='')
    hContactPhone = models.CharField('Phone Number', max_length=10, default='')
    __unicode__ = lambda self: str(self.hospitalName)

# allergy
# type, description
class Allergy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    allergyType = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=255, null=True, default='')
    __unicode__ = lambda self: self.allergyType


# use these settings for calling QueryFHIR when displaying info
class PrivacySettings(models.Model):
    # patient
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    # persional info
    dob_public = models.BooleanField(default=False)
    dob_private = models.BooleanField(default=False)
    address_public = models.BooleanField(default=False)
    address_private = models.BooleanField(default=False)
    # conditions
    condition_public = models.BooleanField(default=False)
    condition_private = models.BooleanField(default=False)
    # blood type
    blood_type_public = models.BooleanField(default=False)
    blood_type_private = models.BooleanField(default=False)
    # allergy
    allergy_public = models.BooleanField(default=False)
    allergy_private = models.BooleanField(default=False)
    # medications
    meds_public = models.BooleanField(default=False)
    meds_private = models.BooleanField(default=False)
    # observations
    observation_public = models.BooleanField(default=False)
    observation_private = models.BooleanField(default=False)
    # encounters
    encounter_public = models.BooleanField(default=False)
    encounter_private = models.BooleanField(default=False)
    # medication dispense
    med_dispense_public = models.BooleanField(default=False)
    med_dispense_private = models.BooleanField(default=False)
    # medication order
    med_order_public = models.BooleanField(default=False)
    med_order_private = models.BooleanField(default=False)
    # operation definition
    operation_def_public = models.BooleanField(default=False)
    operation_def_private = models.BooleanField(default=False)
    # procedure
    procedure_public = models.BooleanField(default=False)
    procedure_private = models.BooleanField(default=False)
