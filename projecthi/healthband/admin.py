from django.contrib import admin
from .models import Patient, Provider, BloodType, Allergy

class PatientModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user", "pid"]
    list_display_links = ["user"]
    search_fields = ["user", "pid"]
    class Meta:
        model = Patient

class ProviderModelAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "user", "hospitalName"]
    list_display_links = ["user"]
    search_fields = ["user", "hospitalName"]
    class Meta:
        model = Provider

# Register your models here.
admin.site.register(Patient, PatientModelAdmin)
admin.site.register(Provider, ProviderModelAdmin)
admin.site.register(BloodType)
admin.site.register(Allergy)
