from django.contrib import admin
from .models import *
 
admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)
class EventInline(admin.TabularInline):
    model = Event
    extra = 3

class PartitAdmin(admin.ModelAdmin):
    inlines = [EventInline]

admin.site.register(Partit, PartitAdmin)