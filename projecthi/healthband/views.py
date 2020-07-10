import qrcode
import StringIO

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db import models
from .models import Patient, Provider, BloodType, Allergy, PrivacySettings
from .query_fhir import PatientInfo, helper
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .forms2 import RegistrationForm, LoginForm, providerRegistrationForm
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext

def UserRegistration(request, pid=None, f=None, l=None):
    patientId = request.session.get('pid')
    firstName = request.session.get('f')
    lastName = request.session.get('l')
#    bloodType = request.session.get('b')
    print(patientId)
    if request.user.is_authenticated():
        return signinform(request)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
            user.first_name = firstName
            user.last_name = lastName
            # adding Patient group
            # TODO for provider use
            # user.groups.add(Group.objects.get(name='Provider'))
            user.groups.add(Group.objects.get(name='Patient'))
            user.save()

            patient = Patient(pid=patientId, user=user)
            patient.save()
            settings = PrivacySettings(patient = patient,
                           dob_public = False,
                           dob_private = False,
                           address_public = False,
                           address_private = False,
                           condition_public = False,
                           condition_private = False,
                           meds_public = False,
                           meds_private = False,
                           observation_public = False,
                           observation_private = False,
                           encounter_public = False,
                           encounter_private = False,
                           med_dispense_public = False,
                           med_dispense_private = False,
                           med_order_public = False,
                           med_order_private = False,
                           operation_def_public = False,
                           operation_def_private = False,
                           procedure_public = False,
                           procedure_private = False)
            settings.save()
            return signinform(request)
        else:
            print(form.errors)
            return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        return render_to_response('register.html', {'form': form} , context_instance=RequestContext(request))

def providerRegistration(request):
    if request.user.is_authenticated():
        return signinform(request)
    if request.method == 'POST':
        form = providerRegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            first_name= form.cleaned_data['first_name']
            last_name= form.cleaned_data['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.groups.add(Group.objects.get(name='Provider'))
            user.save()
            print "user saved"

            provider = form.save(commit=False)
            provider.save()
            provider.user = user
            provider.save()
            print "provider saved"
            user = authenticate(username=username, password=password)
            login(request, user)
            return index(request)
        else:
            print(form.errors)
            return render(request, 'registration/providerRegistration.html', {'form': form})
    else:
        form = providerRegistrationForm()
        return render(request, 'registration/providerRegistration.html', {'form': form})


def index(request):
    template = loader.get_template('main/index.html')
    if request.user.is_authenticated:
        context = {'username' : request.user.username.title()}
    return HttpResponse(template.render(context, request))

#def signin(request):
#    template = loader.get_template('main/signin.html')
#    context = {
#               }
#    return HttpResponse(template.render(context, request))

def submitLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if (user is not None):
        if (user.is_active):
            login(request, user)
            #success page
            if user.groups.filter(name='Patient').exists():
                patient = Patient.objects.filter(user=user).first()
                print("logged in patient pid "+str(patient.pid))
                return viewPatient(request, patient.pid, "")
            elif user.groups.filter(name='Provider').exists():
                provider = Provider.objects.filter(user=user).first()
                print("logged in provider" + provider.hospitalName)
        else:
            #disabled account page
            print("disabled account")
            return signinformwitherror(request, "Disabled Account")
    else:
        #invvalid login
        print("invalid login")
        return signinformwitherror(request, "Invalid Login")

def signinform(request):
    logout(request)
    template = loader.get_template('registration/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def signinformwitherror(request, msg):
    template = loader.get_template('registration/login.html')
    context = {
               "error_msg": msg}
    return HttpResponse(template.render(context, request))

def logoutuser(request):
    logout(request)
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required
def loggedin(request):
    patient = Patient.objects.filter(user=request.user).first()
    if patient == None:
        print ('error')
        context = {'error' : 'You are not a valid patient.'}
        #TODO create error html
        return render(request, 'patient/error.html')
    context = {'patient' : patient}
    return render(request, 'patient/settings.html')

@login_required(login_url='/healthband/signinform')
def patient(request):
    pid = request.GET.get('pid', -1)
    return viewPatient(request, pid, "")

@login_required(login_url='/healthband/signinform')
def viewPatient(request, pid, msg):
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Patient').exists():
            template = loader.get_template('patient/settings.html')
            h = helper()
            p = h.get_patient_req(pid)
            print ('pid is ' + str(pid))
            print ('printing p')
            print(p)
            print (p.keys())
            privacySettings = PrivacySettings.objects.filter(patient__pid = pid).first()
            if (None != privacySettings):
                print("retrieved pid "+str(privacySettings.patient.pid))
                print("retrieved " +str(privacySettings.dob_public))
            else:
                privacySettings = PrivacySettings(patient = Patient.objects.filter(pid=pid).first(),
                                   dob_public = False,
                                   dob_private = False,
                                   address_public = False,
                                   address_private = False,
                                   condition_public = False,
                                   condition_private = False,
                                   meds_public = False,
                                   meds_private = False,
                                   observation_public = False,
                                   observation_private = False,
                                   encounter_public = False,
                                   encounter_private = False,
                                   med_dispense_public = False,
                                   med_dispense_private = False,
                                   med_order_public = False,
                                   med_order_private = False,
                                   operation_def_public = False,
                                   operation_def_private = False,
                                   procedure_public = False,
                                   procedure_private = False)


            ## QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=0,
            )
            qr.add_data('http://127.0.0.1:8000/healthband/viewpatientdata/?pid=' + str(pid))
            qr.make(fit=True)

            img = qr.make_image()

            buffer = StringIO.StringIO()
            img.save(buffer, 'PNG')
            image64 = buffer.getvalue().encode('base64')
            buffer.close()
            print(image64)

            context = {
                    'pid' : pid,
                    'first_name' : p['entry'][0]['resource']['name'][0]['given'][0],
                    'last_name' : p['entry'][0]['resource']['name'][0]['family'][0],
                    'dob' : p['entry'][0]['resource']['birthDate'],
                    'gender' : p['entry'][0]['resource']['gender'],
                    'street' : p['entry'][0]['resource']['address'][0]['line'][0],
                    'city' : p['entry'][0]['resource']['address'][0]['city'],
                    'state' : p['entry'][0]['resource']['address'][0]['state'],
                    'postalCode' : p['entry'][0]['resource']['address'][0]['postalCode'],
                    'public_dob' : "checked" if privacySettings.dob_public else "",
                    'public_address' : "checked" if privacySettings.address_public else "",
                    'public_condition' : "checked" if privacySettings.condition_public else "",
                    'public_meds' : "checked" if privacySettings.meds_public else "",
                    'public_observation' : "checked" if privacySettings.observation_public else "",
                    'public_encounter' : "checked" if privacySettings.encounter_public else "",
                    'public_med_dispense' : "checked" if privacySettings.med_dispense_public else "",
                    'public_med_order' : "checked" if privacySettings.med_order_public else "",
                    'public_operation_def' : "checked" if privacySettings.operation_def_public else "",
                    'public_procedure' : "checked" if privacySettings.procedure_public else "",
                    'private_dob' : "checked" if privacySettings.dob_private else "",
                    'private_address' : "checked" if privacySettings.address_private else "",
                    'private_condition' : "checked" if privacySettings.condition_private else "",
                    'private_meds' : "checked" if privacySettings.meds_private else "",
                    'private_observation' : "checked" if privacySettings.observation_private else "",
                    'private_encounter' : "checked" if privacySettings.encounter_private else "",
                    'private_med_dispense' : "checked" if privacySettings.med_dispense_private else "",
                    'private_med_order' : "checked" if privacySettings.med_order_private else "",
                    'private_operation_def' : "checked" if privacySettings.operation_def_private else "",
                    'private_procedure' : "checked" if privacySettings.procedure_private else "",
                    'msg': msg,
                    'image64': image64
                    }
            return HttpResponse(template.render(context, request))
        else:
            return index(request)
    else:
        return index(request)

def viewPatientData(request):
    patientId = int(float(request.GET.get('pid', -1)))
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Patient').exists():
            return viewPatientDataByPidAndMode(patientId, "patient", request)
        elif request.user.groups.filter(name="Provider").exists():
            return viewPatientDataByPidAndMode(patientId, "private", request)
        else:
            return viewPatientDataByPidAndMode(patientId, "public", request)
    else:
        return viewPatientDataByPidAndMode(patientId, "public", request)

def viewPatientDataByPidAndMode(patientId, mode, request):
    patientInfo = PatientInfo(pid=patientId, mode=mode)
    template = loader.get_template('views.html')
    context = {
               "patient_info":patientInfo
               }
    return HttpResponse(template.render(context, request))

def regform(request):
    template = loader.get_template('patient/regform.html')
    context = {
               }
    return HttpResponse(template.render(context, request))

def regformwitherror(request, msg):
    template = loader.get_template('patient/regform.html')
    context = {
               "error_msg" : msg
               }
    return HttpResponse(template.render(context, request))

def register(request):
    print (RequestContext(request))
    firstName = request.POST['firstName']
    lastName = request.POST['lastName']
    gender = request.POST['genderRadios']
    dob = request.POST['dob']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    postalCode = request.POST['postalCode']
#    bloodType = request.POST['BloodType']

    h = helper()
    patientId = h.get_pid(firstName, lastName, dob, address, city, state, postalCode)
    #print(patientId)
    if (-1 != patientId):
        template = loader.get_template('register.html')
        p = h.get_patient_req(patientId)
#        print(p['entry'][0]['resource'])
        form = RegistrationForm()
        request.session['pid'] = patientId
        request.session['f'] = firstName
        request.session['l'] = lastName
#        request.session['b'] = bloodType
        return redirect('/healthband/register2')
    else:
        return regformwitherror(request, "Unable to look up patient information.")

@login_required(login_url='/healthband/signinform')
def saveSettings(request):
    if request.user.groups.filter(name='Patient').exists():
        postedPID = request.POST['pid']
        p = Patient.objects.filter(pid = postedPID).first()
        public = request.POST.getlist('public')
        public_dob = 'dob' in public
        public_address = 'address' in public
        public_condition = 'condition' in public
        public_encounters = 'encounters' in public
        public_medication = 'medication' in public
        public_medDispense = 'medDispense' in public
        public_medOrder = 'medOrder' in public
        public_observation = 'observation' in public
        public_operationDef = 'operationDef' in public
        public_procedure = 'procedure' in public
        private = request.POST.getlist('private')
        private_dob = 'dob' in private
        private_address = 'address' in private
        private_condition = 'condition' in private
        private_encounters = 'encounters' in private
        private_medication = 'medication' in private
        private_medDispense = 'medDispense' in private
        private_medOrder = 'medOrder' in private
        private_observation = 'observation' in private
        private_operationDef = 'operationDef' in private
        private_procedure = 'procedure' in private
        settings = PrivacySettings.objects.filter(patient__pid = p.pid).first()
    else:
        return regformwitherror(request, "User does not have permission to update settings.")

    if (None != settings):
           settings.dob_public = public_dob
           settings.dob_private = private_dob
           settings.address_public = public_address
           settings.address_private = private_address
           settings.condition_public = public_condition
           settings.condition_private = private_condition
           settings.meds_public = public_medication
           settings.meds_private = private_medication
           settings.observation_public = public_observation
           settings.observation_private = private_observation
           settings.encounter_public = public_encounters
           settings.encounter_private = private_encounters
           settings.med_dispense_public = public_medDispense
           settings.med_dispense_private = private_medDispense
           settings.med_order_public = public_medOrder
           settings.med_order_private = private_medOrder
           settings.operation_def_public = public_operationDef
           settings.operation_def_private = private_operationDef
           settings.procedure_public = public_procedure
           settings.procedure_private = private_procedure
    else:
        settings = PrivacySettings(patient = p,
                               dob_public = public_dob,
                               dob_private = private_dob,
                               address_public = public_address,
                               address_private = private_address,
                               condition_public = public_condition,
                               condition_private = private_condition,
                               meds_public = public_medication,
                               meds_private = private_medication,
                               observation_public = public_observation,
                               observation_private = private_observation,
                               encounter_public = public_encounters,
                               encounter_private = private_encounters,
                               med_dispense_public = public_medDispense,
                               med_dispense_private = private_medDispense,
                               med_order_public = public_medOrder,
                               med_order_private = private_medOrder,
                               operation_def_public = public_operationDef,
                               operation_def_private = private_operationDef,
                               procedure_public = public_procedure,
                               procedure_private = private_procedure)
    settings.save()
    return viewPatient(request, postedPID, "Save Successful")
