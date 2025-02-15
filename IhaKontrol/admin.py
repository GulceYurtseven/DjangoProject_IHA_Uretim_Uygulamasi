from django.contrib import admin
from .models import Team, Profile, Aircraft, Aircraft_produced, Part
#test için admin paneli
admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Aircraft)
admin.site.register(Aircraft_produced)
admin.site.register(Part)
