from django.db import models
from . import models
import httplib2, json, string, requests
from .models import PrivacySettings

PATIENT = r'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Patient?_id={pid}&_format=json'
PATIENT_BY_NAME = r'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Patient?family={fam}&given={given}&_format=json'
CONDITION = r"http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Condition?"
MEDICATION = r'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Medication?'
MEDICATION_ORDER = r'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/MedicationOrder?'
OBSERVATION = r'http://polaris.i3l.gatech.edu:8080/gt-fhir-webapp/base/Observation?'

class helper(object):
    def get_pid(self, given, family, dob, street, city, state, postalCode):
        try:
            r = requests.get(PATIENT_BY_NAME.replace("{fam}", family).replace("{given}", given))
            patientList = json.loads(r.text)
            print(patientList)
            if (len(patientList['entry']) > 1):
                for p in patientList['entry']:
                    #compare DOB
                    if p['resource']['birthDate'] == dob:
                        #compare address
                        fhir_addr = p['resource']['address']
                        # note, could be multiple addresses, looking at home address only
                        for addr in fhir_addr:
                            print(addr)
                            if addr['use'] == 'home':
                                # compare address here
                                if (addr['city'].upper() == city.upper() and 
                                    addr['line'][0].upper() == street.upper() and 
                                    addr['postalCode'] == postalCode and 
                                    addr['state'].upper() == state.upper()):
                                    return p['resource']['id']
            elif (len(patientList['entry'])) == 1:
                return patientList['entry'][0]['resource']['id']
    
            return -1
        except:
            return -1
    
    def get_patient_req(self, pid):
        r = requests.get(PATIENT.replace("{pid}", str(pid)))
        #print(r.text)
        return json.loads(r.text)
        
class PatientInfo(object):
    def __init__(self, pid, mode='public'):
        is_patient_mode = True if mode == 'patient' else False
        is_private_mode = True if mode == 'private' else False
        is_public_mode = True if mode == 'public' else False
        # getting settings object for patient pid
        self.settings = PrivacySettings.objects.filter(patient__pid=pid).first()
        
        # patient's basic info
        h = helper()
        self.pat_content = h.get_patient_req(pid)
        self.first_name = self.get_first_name()
        self.last_name = self.get_last_name()
        self.full_name = " ".join([self.first_name, self.last_name])
        self.gender = self.get_gender()
        
        # patient's address
        if is_patient_mode or (is_public_mode and self.settings.address_public) or (is_private_mode and self.settings.address_private):
            patient = self.pat_content
            try:
                line = str(patient['entry'][0]['resource']['address'][0]['line'][0])
                city = str(patient['entry'][0]['resource']['address'][0]['city'])
                state = str(patient['entry'][0]['resource']['address'][0]['state'])
                postalCode = str(patient['entry'][0]['resource']['address'][0]['postalCode'])
                self.address = " ".join([line, city, state, postalCode])
            except:
                self.address = ''
        else:
            self.address =  ''

        # patient's dob
        if is_patient_mode or (is_public_mode and self.settings.dob_public) or (is_private_mode and self.settings.dob_private):
            patient = self.pat_content
            try:
                self.dob = str(patient['entry'][0]['resource']['birthDate'])
            except:
                self.dob = ''
        else:
            self.dob = ''
        
        # patient's conditions
        if is_patient_mode or (is_public_mode and self.settings.condition_public) or (is_private_mode and self.settings.condition_private):
            r = requests.get(CONDITION.replace("?", "?patient={}".format(pid)))
            self.cond_content = json.loads(r.text)
            self.cond_confirmed, self.cond_unconfirmed = self.get_conditions()
        else:
            self.cond_confirmed = {}, {}

        # patient's medications ordered
        if is_patient_mode or (is_public_mode and self.settings.meds_public) or (is_private_mode and self.settings.meds_private):
            r = requests.get(MEDICATION_ORDER.replace("?", "?patient={}".format(pid)))
            self.med_content = json.loads(r.text) 
            self.meds = self.get_meds()
        else:
            self.meds = {}

    # getting patient's first and last name and middle initial if any
    def get_first_name(self):
        patient = self.pat_content
        try:
            first = str(patient['entry'][0]['resource']['name'][0]['given'][0]).strip()
            try:
                middle = str(patient['entry'][0]['resource']['name'][0]['given'][1]).strip()
                return " ".join([first, middle])
            except:
                pass
            return first
        except:
            return "No record found for patient"

    def get_last_name(self):
        patient = self.pat_content
        try:
            return str(patient['entry'][0]['resource']['name'][0]['family'][0]).strip()
        except:
            return "No record found for patient"

    # patient's gender
    def get_gender(self):
        patient = self.pat_content
        try:
            return str(patient['entry'][0]['resource']['gender'])
        except:
            return "No record found for patient"
        
    # getting condition w/ snomed code from condition id
    def get_condition_id(self, condition_id):
        resp, content = httplib2.Http().request(string.replace(CONDITION, "?", "/{}?".format(condition_id)))
        condition = json.loads(content)
        try:
            return str(condition['code']['text'])
        except KeyError:
            return "No conditions found for condition id: {}".format(condition_id)

    # getting a list of confirmed conditions per patient from patient id
    def get_conditions(self):
        conditions = self.cond_content
        conf_cond = list()
        unconf_cond = list()
        try:
            if conditions['total'] > 0:
                for i, val in enumerate(conditions['entry']):
                    if val['resource']['verificationStatus'] == 'confirmed':
                        cond = {}
                        cond['condition'] = str(val['resource']['code']['text'])
                        cond['status'] = 'confirmed'
                        if 'severity' in val['resource']:
                            cond['severity'] = str(val['resource']['severity']['text'])
                        if 'onsetDateTime' in val['resource']:
                            cond['onset'] = str(val['resource']['onsetDateTime'])
                        conf_cond.append(cond)
                    else:
                        cond = {}
                        cond['condition'] = str(val['resource']['code']['text'])
                        cond['status'] = 'unconfirmed'
                        if 'severity' in conditions['entry'][i]['resource']:
                            cond[i]['severity'] = str(val['resource']['severity']['text'])
                        if 'onsetDateTime' in val['resource']:
                            cond['onset'] = str(val['resource']['onsetDateTime'])
                        unconf_cond.append(cond)
                return conf_cond, unconf_cond
        except KeyError:
            print("No conditions found for patient")
            return dict(), dict()
           

    # getting a list of all medication orders for a patient by patient id
    def get_meds(self):
        meds = self.med_content
        meds_prescribed = list()
        try:
            if meds['total'] > 0:
                for i, val in enumerate(meds['entry']):
                    prescribed = {}
                    prescribed['medication'] = str(val['resource']['medicationReference']['display'])
                    if 'dateWritten' in val['resource']:
                        prescribed['datePrescribed'] = str(val['resource']['dateWritten'])
                    if 'prescriber' in meds['entry'][i]['resource']:
                        prescribed['prescriber'] = str(meds['entry'][i]['resource']['prescriber']['reference'])
                    meds_prescribed.append(prescribed)
                return meds_prescribed
        except KeyError:
            print("No prescriptions found for patient")
            return dict()

